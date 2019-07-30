import threading
import time
from queue import Queue
from spider import Spider
from domain import *
from general import *
import pandas as pd

PROJECT_NAME = '800notes'
HOMEPAGE = 'https://800notes.com/Phone.aspx/1-866-236-7606'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.csv'
CRAWLED_FILE = PROJECT_NAME + '/crawled.csv'
USE_PROXY = False
# DB_FILE = PROJECT_NAME + "_info.db"
NUMBER_OF_THREADS = 1
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, USE_PROXY)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()
    pass


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()





create_workers()
crawl()
