import requests
import time

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    while retry_count > 0:
        try:
            print(proxy)
            html = requests.get('https://800notes.com/Phone.aspx/1-866-236-7606', proxies={"http": "http://{}".format(proxy)},headers = headers, timeout = 5)
            # 使用代理访问
            # print("can be used")
            print(html.status_code)
            if(html.status_code == 520):
                delete_proxy(proxy)
                print("should be deleted")
                time.sleep(1)
            html.raise_for_status()
            print(html.text)
            return html
        except Exception as e:
            print(str(e))
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    delete_proxy(proxy)
    print("denied")
    return None

while True:
    getHtml()