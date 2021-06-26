from LssdjtCrawler import LssdjtCrawler
import json


def getEventList():
    lssdjtCrawler = LssdjtCrawler()

    result = lssdjtCrawler.getEventList()

    print(result)

try:
    getEventList()

except Exception as e:
    print(str(e))
