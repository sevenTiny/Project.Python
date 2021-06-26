from OfficeAccount.MaterialMgmt import MaterialMgmt
from Crawler.LssdjtCrawler import LssdjtCrawler
from Crawler.BaiduCalendar import BaiduCalendar
import datetime
import locale
import random
import requests
import os
import json

def handel():
    # 设置本地语言环境，避免日期中文转换失败
    # locale.setlocale(locale.LC_CTYPE, 'chinese')
    timeNow = datetime.datetime.now()
    todayNian = timeNow.strftime('%Y')+'年'
    todayYue = timeNow.strftime('%m')+'月'
    todayRi = timeNow.strftime('%d')+'日'
    todayChineseDateTime = todayNian+todayYue+todayRi

    # 发布
    content = '<section data-tools-id="92054"><section style="margin:0 auto"><section style="margin:0 auto"><section style="margin:0 15px 20px;border:3px solid #fff;border-radius:3px;box-sizing:border-box"><img style="display:block;max-width:100%;width:100%!important" src="https://mmbiz.qpic.cn/mmbiz_jpg/ibjeFnibJt8h9h98QfLCRMxr5xaicoaZKfFWbibXq8WUj02qJLZ8qEFpOc69KeEqWFOcOx7u1T9vJUEILESdC9Yu8A/640?wx_fmt=jpeg" data-tools-id="14224"></section><article>'

    materialMgmt = MaterialMgmt()

    # 1. 从百度百科获取历史上的今天的突出数据
    baiduCalendar = BaiduCalendar()
    todayTitleDataList = baiduCalendar.getEventList()

    for item in todayTitleDataList:
        time = item['year']+'年'+str(timeNow.month) + \
            '月'+str(timeNow.day)+'日'
        title = item['title']
        desc = item['desc']
        imgUrl = item['imgUrl']

        content = content+'<section style="margin:0 25px"><section style="margin-bottom:12px;display:flex;align-items:center;justify-content:center"><section style="padding:5px 8px;background-color:#bab8b8;margin-right:3px"><p style="margin:0 auto;text-align:center;letter-spacing:1.5px;font-size:15px;line-height:16px;color:#fff">'+time+'</p></section><section style="flex:1;height:1px;border-top:1px dashed #bab8b8"></section></section><p style="margin:0 5px 15px;text-align:justify;letter-spacing:1.5px;font-size:15px;line-height:24px">'+title + \
            '</p></section><section><section style="margin:2px auto 8px;display:flex;justify-content:center;align-items:center"><section style="display:flex;flex-direction:column;justify-content:center;align-items:center;width:100%;box-sizing:border-box"><section style="width:53px;flex-shrink:0;align-self:flex-end;margin-bottom:-30px;z-index:2"><span style="max-width: 100%;display: block;margin-top: 40px;"></span></section><section style="display:flex;flex-direction:column;justify-content:center;align-items:flex-start;align-self:flex-start;width:100%;box-sizing:border-box"><section style="width:80px;height:2px;background-image:linear-gradient(to right,#ffc691 0,rgba(255,255,255,.5) 100%);flex-shrink:0;margin:0 0 3px 6px"></section><section style="width:100%;height:2px;background-image:linear-gradient(to right,#ffc691 0,rgba(255,255,255,.5) 90%);flex-shrink:0"></section></section><section style="display:flex;flex-direction:row;justify-content:center;width:92%;box-sizing:border-box;z-index:1;margin:-15px 0"><section style="width:2px;background-image:linear-gradient(to bottom,#ffc691 0,rgba(255,255,255,.5) 90%);flex-shrink:0"></section><section style="width:100%;box-sizing:border-box;padding:30px 20px"><p style="margin:0;font-size:15px;color:#333;letter-spacing:1.5px;line-height:1.75">' + \
            desc+'</p></section><section style="width:2px;background-image:linear-gradient(to top,#ffc691 0,rgba(255,255,255,.5) 90%);flex-shrink:0"></section></section><section style="display:flex;flex-direction:column;justify-content:center;align-items:flex-end;align-self:flex-end;width:100%;box-sizing:border-box"><section style="width:100%;height:2px;background-image:linear-gradient(to left,#ffc691 0,rgba(255,255,255,.5) 90%);flex-shrink:0"></section><section style="width:80px;height:2px;background-image:linear-gradient(to left,#ffc691 0,rgba(255,255,255,.5) 100%);flex-shrink:0;margin:3px 6px 0 0"></section></section></section></section></section><p><br></p>'

        try:
            # 下载并上传图片
            imgFilePath = os.path.basename(imgUrl)
            print('download pic from:' + imgUrl)
            if os.path.exists(imgFilePath):
                os.remove(imgFilePath)

            baiduCalendar.request_download(imgUrl, imgFilePath)
            imgWxUrl = materialMgmt.uploadimg(imgFilePath)
            print('upload pic to:'+imgWxUrl)

            if os.path.exists(imgFilePath):
                os.remove(imgFilePath)

            # 添加图片占位显示
            if imgWxUrl is not None and imgWxUrl != '':
                content = content + '<section style="margin:0 15px 20px;border:3px solid #fff;border-radius:3px;box-sizing:border-box"><img style="display:block;max-width:100%;width:100%!important" src="' + \
                    imgWxUrl+'" data-tools-id="14224"></section><p><br></p>'
        except Exception as e:
            print('处理图片失败：'+json.dumps(e))

    # 从每日百度百科突出数据提取今日标题，默认为今日日期
    postTitle = todayChineseDateTime
    if len(todayTitleDataList) > 0:
        todayData = todayTitleDataList[0]
        time = todayData['year']+'年'+str(timeNow.month) + \
            '月'+str(timeNow.day)+'日'
        title = todayData['title']
        postTitle = time + ', ' + title

    # 2. 从历史上的今天站点获取历史上的今天数据
    lssdjtCrawler = LssdjtCrawler()
    historyList = lssdjtCrawler.getEventList()

    count = len(historyList)
    print(todayChineseDateTime+'共找到'+str(count)+'条今日历史')
    indexRange = range(0, count)
    # 最多显示数量
    queryCount = 15

    if count < queryCount:
        queryCount = count

    for index in sorted(random.sample(indexRange, queryCount)):
        item = historyList[index]
        text = str(item['title'])
        splitIndex = text.index('日 ')
        time = text[0:splitIndex+1]
        # time = time[0:time.index('年')+1]
        title = text[splitIndex+2:]

        content = content + '<section style="margin:0 25px"><section style="margin-bottom:12px;display:flex;align-items:center;justify-content:center"><section style="padding:5px 8px;background-color:#bab8b8;margin-right:3px"><p style="margin:0 auto;text-align:center;letter-spacing:1.5px;font-size:15px;line-height:16px;color:#fff">' + \
            time+'</p></section><section style="flex:1;height:1px;border-top:1px dashed #bab8b8"></section></section><p style="margin:0 5px 15px;text-align:justify;letter-spacing:1.5px;font-size:15px;line-height:24px">'+title+'</p></section>'

    content = content + '</article></section><p><br></p><p><br></p><section><section><section style="padding-right:10px;padding-left:10px;line-height:1.6;box-sizing:border-box"><p style="text-align:center"><em><span style="color:#7b0c00"><strong>-END-</strong></span></em></p><hr><p style="text-align:right"><br></p><p style="text-align:right"><br></p><p style="text-align:center"><img src="https://res.wx.qq.com/mpres/htmledition/images/icon/common/emotion_panel/smiley/smiley_66.png" width="20px" style="display:inline-block;vertical-align:text-bottom;width:20px!important;visibility:visible!important;max-width:100%;height:auto"></p><p style="text-align:center"><br></p><p style="text-align:center"><span style="color:#7a4442;font-size:14px">看完本文的你是否有所收获？</span></p><p style="text-align:center"><span style="color:#7a4442;font-size:14px">请转发给更多人关注</span></p><p style="text-align:center"><span style="color:#7a4442;font-size:14px">【今天你可能想知道】</span></p><p style="text-align:center"><span style="color:#7a4442;font-size:14px">提升知识~</span></p><p style="text-align:center"><img data-s="300,640" src="https://mmbiz.qpic.cn/mmbiz_png/ibjeFnibJt8h9h98QfLCRMxr5xaicoaZKfFzaIgg8icIrHnwUMWrd12eu29mG45lEO2FaecomVKtr6mTNENmfnhuuw/0?wx_fmt=png" data-type="jpeg" data-cropselx1="150" data-cropselx2="408" data-cropsely1="0" data-cropsely2="258" data-ratio="0.3310344827586207" data-w="1885" style="height:191px;width:578px"></p><p style="text-align:center"><span style="color:#888">长按关注，谢谢转发</span></p><p style="text-align:center"><span style="color:#888">学海无涯，别担心，有我陪着你~</span></p><p><br></p><p style="text-align:center"><span style="font-size:13px">点个“喜欢”，“薪想事成”。&nbsp;☟&nbsp;</span></p></section></section></section></section></section><p><br></p>'

    data = {
        "articles": [
            {
                "title": postTitle,
                "thumb_media_id": 'wtRD-hkcDxLQTNW6np17fCjXCgeEMG5CbMvPtG27rRw',
                "author": '7tiny',
                "digest": todayChineseDateTime,
                "show_cover_pic": 0,
                "content": content,
                "content_source_url": '',
                "need_open_comment": 1,
                "only_fans_can_comment": 1
            }
            # 若新增的是多图文素材，则此处应还有几段articles结构
        ]
    }

    media_id = materialMgmt.add_news(data)
    return media_id

try:
    media_id = handel()
    print(str(media_id))
    print('发送成功！')

except Exception as e:
    print('发送失败！！！')
    print(json.dumps(e, ensure_ascii=False))
