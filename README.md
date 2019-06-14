![](http://i.imgur.com/wYi2CkD.png)


# Overview

This is an open source, multi-threaded website crawler written in Python. There is still a lot of work to do, so feel free to help out with development.

***

Note: This is part of an open source search engine. The purpose of this tool is to gather links **only**. The analytics, data harvesting, and search algorithms are being created as separate programs. 

### Proxy Usage
To add proxys, a few modifictaions need to be done in main.py
1. At the initialization part, change USE_PROXY to True and NUMBER_OF_THREADS to the number of threads you want to add
```python
USE_PROXY = False 
# DB_FILE = PROJECT_NAME + "_info.db"
NUMBER_OF_THREADS = 1
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, USE_PROXY)
```
2. In create_workers function, add the proxy's username, password and url in proxys. The format is as below.
	- ps: currently I just assume each
```python
def create_workers():
    # With proxy
    proxys = [
        # proxy_lis1,
        # proxy_lis2,
        # ...
    ] #format: proxy_list = ["username","password","url(xxx.xxx.xxx.xxx:port)"] All the info required for one proxy
    # Each proxy will be assigned to one thread. So len(proxys) should be equal to NUMBER_OF_THREADS
```

### Links

- [Support thexnewboston](https://www.patreon.com/thenewboston)
- [thenewboston.com](https://thenewboston.com/)
- [Facebook](https://www.facebook.com/TheNewBoston-464114846956315/)
- [Twitter](https://twitter.com/bucky_roberts)
- [Google+](https://plus.google.com/+BuckyRoberts)
- [reddit](https://www.reddit.com/r/thenewboston/)


