from general import *
from spider import Spider
import time
from domain import *

def get_frequnt_number(record_file):
    number_lis = ['9177407950',
             '9177407959',
             '9177408750',
             '7694871296',
             '5186737084',
             '8002752273',
             '7624998626',
             '8006927753',
             '9177407951',
             '3178650151']
    return number_lis

def get_url(number_lis):
    preurl = "https://800notes.com/Phone.aspx/"
    for number in number_lis:
        formatted = number[:3] + "-" + number[3:6] + "-" + number[6:]
        print(formatted)
        base_page = preurl + formatted
        to_end = True
        target = base_page
        while to_end:
            try:
                specider.crawl_page("thread1",target,count =1)
            except Exception as e:
                print(str(e))
                to_end = True
        print("Comments under " + str(number) + " has all been collected.")




class specider(Spider):

    def __init__(self,project_name, base_url, domain_name, use_proxy = False):
        specider.project_name = project_name
        specider.base_url = base_url
        specider.domain_name = domain_name
        # Spider.queue_file = Spider.project_name + '/queue.csv'
        # Spider.crawled_file = Spider.project_name + '/crawled.csv'
        specider.use_proxy = use_proxy
        self.boot()
        # self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(specider.project_name)
        create_data_files(specider.project_name, Spider.base_url)
        # Spider.queue = file_to_set(Spider.queue_file)
        # Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url,count,total = 1, proxy_lis=[]):
        count = count
        if count > total:
            print("Info under " + page_url  + " has all been collected")
            return 0
        else:
            if count != 1:
                target = page_url + "/" + str(count)
                print(thread_name + ' now crawling ' + target)
                html_string = specider.gather_html_string(target, proxy_lis)
                if html_string == "":
                    time.sleep(1)
                else:
                    if (specider.phone_num(page_url)):
                        data = specider.gather_info(html_string)
                        specider.store_info(data, specider.phone_num(page_url))
                    time.sleep(0.7)
                count += 1
            else:
                crawl_page(thread_name, page_url, count, total=1, proxy_lis=[])

    @staticmethod
    def gather_html_string(page_url, proxy_lis=[]):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
            # page = request.Request(page_url, headers=headers)
            # response = request.urlopen(page)
            # if 'text/html' in response.getheader('Content-Type'):
            #     html_bytes = response.read()
            #     html_string = html_bytes.decode("utf-8")
            #     return html_string
            # return ''
            if (specider.use_proxy):
                username = proxy_lis[0]
                password = proxy_lis[1]
                url = proxy_lis[2]
                proxies = {"http": "http://{}:{}@{}".format(username, password, url)}
                # proxies = {"http": "http://username:password@proxy_ip:proxy_port"}
                response = requests.get(page_url, proxies=proxies, headers=headers, timeout=5)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            else:
                response = requests.get(page_url, headers=headers, timeout=5)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
        except Exception as e:
            print(str(e))
            return ''

    # def gather_info(html_string):
    #     # Remain the same


PROJECT_NAME = 'target800'
HOMEPAGE = 'https://800notes.com/Phone.aspx/1-866-236-7606'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.csv'
CRAWLED_FILE = PROJECT_NAME + '/crawled.csv'
USE_PROXY = False
# DB_FILE = PROJECT_NAME + "_info.db"
NUMBER_OF_THREADS = 1
# queue = Queue()
specider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, USE_PROXY)

get_url(get_frequnt_number("whatever"))
