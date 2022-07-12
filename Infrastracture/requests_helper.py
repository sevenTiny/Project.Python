import random
import requests


class requests_helper:
    def __init__(self):
        pass

    HEADERS = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'
    }

    # 代理开关
    USE_PROXY = False
    # 代理地址
    PROXYS = [{
        "http": "http://103.148.72.126:80",
        "https": "https://197.255.209.34:8080",
    }]

    @staticmethod
    def get(url):
        return requests.get(url,
                            headers=requests_helper.HEADERS,
                            proxies=random.sample(requests_helper.PROXYS, 1)
                            if requests_helper.USE_PROXY else None)

    @staticmethod
    def post(url, json=None, data=None):
        return requests.post(url,
                             headers=requests_helper.HEADERS,
                             json=json,
                             data=data,
                             proxies=random.sample(requests_helper.PROXYS, 1)
                             if requests_helper.USE_PROXY else None)
