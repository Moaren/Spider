from urllib import request
from link_finder import LinkFinder
from domain import *
from general import *
import time
from bs4 import BeautifulSoup
# from sql_helper import sql_helper
import json
import requests
import shutil


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            html = requests.get('https://www.example.com', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    return None

class Spider:

    project_name = ''
    # db_file = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    use_proxy = ''

    def __init__(self,project_name, base_url, domain_name, use_proxy = False):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.csv'
        Spider.crawled_file = Spider.project_name + '/crawled.csv'
        Spider.use_proxy = use_proxy
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            if len(Spider.crawled) % 5000 == 0:
                Spider.backup_csv()
            html_string = Spider.gather_html_string(page_url)
            if html_string == "":
                Spider.update_files()
                time.sleep(1)
            else:
                links = Spider.gather_links(html_string,page_url)
                Spider.add_links_to_queue(links)
                if(Spider.phone_num(page_url)):
                    data = Spider.gather_info(html_string)
                    Spider.store_info(data,Spider.phone_num(page_url))
                Spider.queue.remove(page_url)
                Spider.crawled.add(page_url)
                Spider.update_files()
                time.sleep(0.7)

    # Get the HTML text from a certain page
    @staticmethod
    def gather_html_string(page_url):
        html_string = ''
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
            # page = request.Request(page_url, headers=headers)
            # response = request.urlopen(page)
            # if 'text/html' in response.getheader('Content-Type'):
            #     html_bytes = response.read()
            #     html_string = html_bytes.decode("utf-8")
            #     return html_string
            # return ''
            if(Spider.use_proxy):
                retry_count = 5
                proxy = get_proxy()
                while retry_count > 0:
                    try:
                        response = requests.get(page_url, proxies={"http": "http://{}".format(proxy)},headers=headers,timeout=5)
                        if(response.status_code == "502"):
                            delete_proxy(proxy)
                        response.raise_for_status()
                        response.encoding = 'utf-8'
                        return response.text
                    except Exception:
                        retry_count -= 1
                delete_proxy(proxy)
                return ""
            else:
                response = requests.get(page_url,headers=headers,timeout=5)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
        except Exception as e:
            print(str(e))
            return ''

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(html_string,page_url):
        try:
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def gather_info(html_string):
        soup = BeautifulSoup(html_string, 'lxml')
        # print("This is \n" + soup.prettify())
        result = []
        for comment in soup.find_all("li",class_ = "oos_contlet"):
            try:
                # print(comment)
                datetime = comment.find("time").text
                #                 # print(datetime)
                content = comment.find("div",class_ = "oos_contletBody").text
                # print(content)
                call_type, caller = "", ""
            except AttributeError: # If the oos_contlet object is an advertisement picture
                continue

            try:
                call_details = comment.find("ul",class_ = "callDetails")
                for i in call_details.find_all("li"):
                    try:
                        if("Call type" in i.text):
                            call_type = i.text.split('Call type: ')[1]
                        if("Caller" in i.text):
                            caller = i.text.split('Caller: ')[1]
                    except IndexError:
                        pass
            except AttributeError:
                pass

            is_reply = False # Judge whether the comment is the reply to another person
            user_info = comment.find("div",class_ = "oos_pc").text
            if "replies to" in user_info:
                is_reply = True

            # print(user_info)
            result.append({
            "datetime": datetime,
            "content": content,
            "caller": caller,
            "call_type": call_type,
            "is_reply":is_reply,
            })
        # print(result)
        return result



    @staticmethod
    def phone_num(page_url):
        if("https://800notes.com/Phone.aspx/" in page_url and "#" not in page_url):
            number =  page_url.split('/')[4]
            valid_char = ['0','1','2','3','4','5','6','7','8','9','-']
            for i in number:
                # If the formate is not *-****-***
                if(i not in valid_char):
                    return None
            return number
        return None

    @staticmethod
    def store_info(data,number):
        file_name = Spider.project_name + '.csv'
        csv_file = Spider.project_name + "/" + file_name
        for comment in data:
            comment['content'] = comment['content'].replace(' ', "")
            comment['phone_number'] = number
        # print(data)
        if not os.path.isfile(csv_file):
            df = pd.DataFrame(data, columns=['datetime', 'content', 'caller', 'call_type','phone_number','is_reply'])
            df.to_csv(csv_file, index=False,header = False,encoding='utf-8')
            print(number + "'s info has been stored")
        else:
            df = pd.DataFrame(data, columns=['datetime', 'content', 'caller', 'call_type','phone_number',"is_reply"])
            df.to_csv(csv_file, index=False, mode="a",header=False,encoding='utf-8')
            print(number + "'s info has been updated")

    @staticmethod
    def backup_csv():
        Spider.queue_file = Spider.project_name + '/queue.csv'
        Spider.crawled_file = Spider.project_name + '/crawled.csv'
        file_name = Spider.project_name + '.csv'
        csv_file = Spider.project_name + "/" + file_name
        # queue_df = pd.read_csv(Spider.queue_file,encoding = 'ISO-8859-1')
        # crawled_df = pd.read_csv( Spider.crawled_file,encoding = 'ISO-8859-1')
        # csv_df = pd.read_csv(csv_file,encoding = 'ISO-8859-1')

        directory = Spider.project_name + "/" + time.strftime("%m%d%H%M", time.localtime())

        if not os.path.exists(directory):
            os.makedirs(directory)

        shutil.copy(Spider.queue_file, directory + '/queue.csv')
        shutil.copy(Spider.crawled_file, directory + '/crawled.csv')
        shutil.copy(csv_file, directory + "/" + file_name)

        print(directory + ": The files have been backed up")


# url = "https://800notes.com/Phone.aspx/1-240-273-1357"
# Spider.crawl_page("test_bs4", url)

# url = "https://800notes.com/Phone.aspx/1-240-273-1357/2"
# Spider.crawl_page("test_bs4", url)

# print(Spider.phone_num("https://800notes.com/Phone.aspx/1-240-273-1357/2"))