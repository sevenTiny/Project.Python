# coding:utf-8
import sys
import requests
from bs4 import BeautifulSoup


class LssdjtCrawler():

    def __getLssdjtHtml(self):
        url = 'https://www.lssdjt.com'

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding

        if(response.status_code != 200):
            return ''

        html = response.text

        return html

    def getEventList(self):

        html = self.__getLssdjtHtml()

        if html.strip() == '':
            return []

        soup = BeautifulSoup(html, "html.parser")

        liarray = soup('li', attrs={'class': 'gong'})

        list = []

        for li in liarray:
            title = li.text

            img = ''
            a = li.findAll('a')
            rel = a[0].get('rel')
            if rel is not None:
                img = rel[0]

            list.append({
                'title': title,
                'imgUrl': img
            })

        return list