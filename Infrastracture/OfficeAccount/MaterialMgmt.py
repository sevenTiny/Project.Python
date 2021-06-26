from OfficeAccount.AuthBase import AuthBase
import requests
import json


class MaterialMgmt(AuthBase):
    def __init__(self):
        super().__init__()

    # 新增永久图文素材
    # date 参数参考：https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html
    def add_news(self, data=None):
        url = 'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=' + \
            self.getAccessToken()

        headers = {'content-type': 'application/json; charset=utf-8'}

        response = requests.post(url, data=json.dumps(
            data, ensure_ascii=False).encode(), headers=headers).json()

        if 'errcode' in response:
            raise Exception(
                'addPermanentGraphicMaterial error:' + json.dumps(response))

        # 返回的即为新增的图文消息素材的media_id
        media_id = response['media_id']

        return media_id

    # 分类型获取永久素材的列表
    def batchget_material(self, data=None):
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=' + \
            self.getAccessToken()

        response = requests.post(url, json=data).json()

        if 'errcode' in response:
            raise Exception(
                'addPermanentGraphicMaterial error:' + json.dumps(response))

        return response

    # 上传图片并拿到mediaid
    def uploadimg(self, imgPath):
        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=' + \
            self.getAccessToken()

        files = {'media': open(imgPath, 'rb')}

        response = requests.post(url, files=files).json()

        if 'errcode' in response:
            raise Exception(
                'uploadimg error:' + json.dumps(response))

        return response['url']
