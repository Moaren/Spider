from urllib import request
from link_finder import LinkFinder
from domain import *
from general import *
import time
from bs4 import BeautifulSoup
# from sql_helper import sql_helper
import json
import requests


class Spider:

    project_name = ''
    # db_file = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self,project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.csv'
        Spider.crawled_file = Spider.project_name + '/crawled.csv'
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
                time.sleep(0.5)

    # Get the HTML text from a certain page
    @staticmethod
    def gather_html_string(page_url):
        html_string = ''
        try:
            # proxy = {'http': 'http://101.109.255.97:44377'}
            # proxyHeader = request.ProxyHandler(proxy)
            # opener = request.build_opener(proxyHeader)
            # request.install_opener(opener)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
            # page = request.Request(page_url, headers=headers)
            # response = request.urlopen(page)
            # if 'text/html' in response.getheader('Content-Type'):
            #     html_bytes = response.read()
            #     html_string = html_bytes.decode("utf-8")
            #     return html_string
            # return ''
            response = requests.get(page_url,headers=headers,timeout=5)
            response.raise_for_status() #返回的状态码不是200的时候，引发异常；只要在收到响应的时候调用这个方法，就可以避开状态码200以外的各种意外情况
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
                    if("Call type" in i.text):
                        call_type = i.text.split('Call type: ')[1]
                    if("Caller" in i.text):
                        caller = i.text.split('Caller: ')[1]
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


# url = "https://800notes.com/Phone.aspx/1-240-273-1357"
# Spider.crawl_page("test_bs4", url)

# url = "https://800notes.com/Phone.aspx/1-240-273-1357/2"
# Spider.crawl_page("test_bs4", url)

# print(Spider.phone_num("https://800notes.com/Phone.aspx/1-240-273-1357/2"))