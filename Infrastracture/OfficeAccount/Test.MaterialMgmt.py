from MaterialMgmt import MaterialMgmt
import json


# 新增图文消息
def add_news():
    materialMgmt = MaterialMgmt()

    content = '<div id="wrap"><div id="header"><h1>html在线工具</h1></div><div id="main"><dl><dt>v1.0</dt><dd>2011-06-05 Html工具上线</dd><dt>v1.1</dt><dd>2012-01-14 修复美化功能，增加压缩</dd><dt>v1.2</dt><dd>2012-07-20 增加清除链接功能</dd><dt>v1.3</dt><dd>2014-08-05 修改 html 压缩引擎</dd><dt>v1.4</dt><dd>2014-08-09 增加转换为js变量的功能</dd><dt>v1.5</dt><dd>2020-11-21 增加内联css功能</dd></dl></div><div id="footer">This is just an example.</div></div>'

    # date 参数参考：https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html
    data = {
        "articles": [
            {
                "title": '测试图文消息',
                "thumb_media_id": 'wtRD-hkcDxLQTNW6np17fN5vO-P6g6hI559pqbIAmtU',
                "author": '7tiny',
                "digest": '图文消息的摘要',
                "show_cover_pic": 1,
                "content": content,
                "content_source_url": 'www.baidu.com',
                "need_open_comment": 1,
                "only_fans_can_comment": 1
            }
            # 若新增的是多图文素材，则此处应还有几段articles结构
        ]
    }

    media_id = materialMgmt.add_news(data)

    print(str(media_id))

# 开发者可以分类型获取永久素材的列表
# https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_materials_list.html


def batchget_material():

    data = {
        "type": 'image',  # 素材的类型，图片（image）、视频（video）、语音 （voice）、图文（news）
        "offset": 0,  # 从全部素材的该偏移位置开始返回，0表示从第一个素材 返回
        "count": 20  # 返回素材的数量，取值在1到20之间
    }

    materialMgmt = MaterialMgmt()

    result = materialMgmt.batchget_material(data)

    # print(json.dumps(result, ensure_ascii=False))
    print('1')


try:
    batchget_material()

except Exception as e:
    print(str(e))
