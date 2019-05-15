from urllib import request
from link_finder import LinkFinder
from domain import *
from general import *
import time
from bs4 import BeautifulSoup


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
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
        # if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            # print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            html_string = Spider.gather_html_string(page_url)
            # Spider.add_links_to_queue(Spider.gather_links(html_string,page_url))
            Spider.gather_info(html_string)
            # Spider.queue.remove(page_url)
            # Spider.crawled.add(page_url)
            # Spider.update_files()
            time.sleep(0.1)

    # Get the HTML text from a certain page
    @staticmethod
    def gather_html_string(page_url):
        html_string = ''
        try:
            # proxy = {'http': '35.233.137.170:80'}
            # proxyHeader = request.ProxyHandler(proxy)
            # opener = request.build_opener(proxyHeader)
            # request.install_opener(opener)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
            page = request.Request(page_url, headers=headers)
            response = request.urlopen(page)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                return html_string
            return ''
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
        print("This is \n" + soup.prettify())
        for comment in soup.find_all("li",class_ = "oos_contlet"):
            datetime = comment.find("time").text
            print(datetime)
            content = comment.find("div",class_ = "oos_contletBody").text
            print(content)
            call_details = comment.find("ul",class_ = "callDetails")
            for i in call_details.find_all("li"):
                print(i.text)


url = "https://800notes.com/Phone.aspx/1-484-661-4706"
Spider.crawl_page("test_bs4", url)