import os, sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastracture.download_helper import download_helper
from infrastracture.requests_helper import requests_helper
import sys, os

HOST = 'https://www.ximalaya.com'


def getTracksList(albumId, pageNum):
    url = f'{HOST}/revision/album/v1/getTracksList?albumId={albumId}&pageNum={pageNum}'
    res = requests_helper.get(url).json()

    if res['ret'] != 200:
        print(f'request:[{url}] got error:{res}')
        return []

    result = res['data']['tracks']

    pageSize = int(res['data']['pageSize'])
    trackTotalCount = int(res['data']['trackTotalCount'])

    if pageSize * pageNum < trackTotalCount:
        result.extend(getTracksList(albumId, pageNum + 1))

    return result


def getAudio(id, ptype):
    url = f'{HOST}/revision/play/v1/audio?id={id}&ptype={ptype}'
    res = requests_helper.get(url).json()

    if res['ret'] != 200:
        print(f'request:[{url}] got error:{res}')
        return None

    return res['data']


if __name__ == '__main__':

    tracksList = getTracksList(2672407, 1)

    print(f'get list success! total:{len(tracksList)}')

    for item in tracksList:

        time.sleep(0.5)

        print(f'{item["index"]}-{item["title"]}')

        autio = getAudio(item['trackId'], 1)

        src = str(autio['src'])

        ext = src.split('.')[-1]

        savePath = os.path.join('temp', str(item["albumTitle"]),
                                f'{str(item["title"])}.{ext}')

        download_helper.download(src, savePath)
