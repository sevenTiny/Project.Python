# coding:utf-8
import sys
import requests
import datetime
import time
import json
from bs4 import BeautifulSoup


class BaiduCalendar():

    def __getCalendarJson(self):

        month = datetime.datetime.now().strftime('%m')
        millis = int(round(time.time() * 1000))

        url = 'https://baike.baidu.com/cms/home/eventsOnHistory/' + \
            month + '.json?_='+str(millis)

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding

        if(response.status_code != 200):
            return ''

        txt = response.text

        return json.loads(txt, encoding='utf-8')

    # 去除html中的a标签
    def __removeA(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()

    def getEventList(self):

        jsonObj = self.__getCalendarJson()

        month = datetime.datetime.now().strftime('%m')
        monthday = datetime.datetime.now().strftime('%m%d')

        todayList = jsonObj[month][monthday]

        current = [x for x in todayList if x['cover'] == True]

        list = []

        for item in current:
            list.append({
                'year': item['year'].replace('\n', ''),
                'title': self.__removeA(item['title']).replace('\n', ''),
                'imgUrl': item['pic_share'],
                'desc': self.__removeA(item['desc']).replace('\n', '')
            })

        return list

    def request_download(self, img_url, img_save_path):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        r = requests.get(img_url, headers=headers, stream=True)
        with open(img_save_path, 'wb') as f:
            f.write(r.content)
