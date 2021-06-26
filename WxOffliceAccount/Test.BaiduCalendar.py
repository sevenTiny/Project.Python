from BaiduCalendar import BaiduCalendar
import json


def getEventList():
    baiduCalendar = BaiduCalendar()

    result = baiduCalendar.getEventList()

    print(result)

try:
    getEventList()

except Exception as e:
    print(str(e))
