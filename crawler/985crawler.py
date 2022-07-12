# #引入代码
import sys
import os
from sys import path
from numpy import double

from requests.api import head
path.append(os.getcwd())  # NOQA: E402

from Infrastracture import json_helper, requests_helper
import json
import os
import requests
import pymongo
import pandas as pd
import numpy as np


def get_score_line(year, school_id, province_id):
    url = 'https://static-data.eol.cn/www/2.0/schoolprovinceindex/' + str(year)+'/'+str(school_id) + '/' + str(province_id) + '/1/1.json'

    res = requests.get(url, headers=requests_helper.get_request_header())
    res = res.content.decode('unicode_escape')

    if res != None and res != '""':
        res_json = json.loads(res)
        return res_json['data']['item']

    return None


def get_schools():
    # 获取高校数据（内部参数需要调整，已经写入数据库，无需每次执行这个）
    result = []
    for page_index in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=1&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page=' + \
            str(page_index) + \
            '&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=200&sort=view_total&top_school_id=[100,934,936,3486,86,35,124,504,108]&type=&uri=apidata/api/gk/school/lists'

        res = requests.post(url, headers=requests_helper.get_request_header(), json={
            "access_token": "",
            "admissions": "",
            "central": "",
            "department": "",
            "dual_class": "",
            "f211": 1,
            "f985": "",
            "is_doublehigh": "",
            "is_dual_class": "",
            "keyword": "",
            "nature": "",
            "page": page_index,
            "province_id": "",
            "ranktype": "",
            "request_type": 1,
            "school_type": "",
            "size": 200,
            "sort": "view_total",
            "top_school_id": "[100,934,936,3486,86,35,124,504,108]",
            "type": "",
            "uri": "apidata/api/gk/school/lists"
        })

        if res != None:
            print(str(res))
            res = res.json()
            if int(res['data']['numFound']) > 0:
                for item in res['data']['item']:
                    result.append(item)
    return result


def __get_mongo_collection(db, collection):
    myclient = pymongo.MongoClient('mongodb://dev:dev123456@192.168.31.135:39911')
    mydb = myclient[db][collection]
    return mydb


def set_school_to_db():
    db = __get_mongo_collection('GaoKao', 'School')
    schools = get_schools()
    re = db.insert_many(schools)
    print('success add:' + str(re.inserted_ids))


def set_score_line_to_db(province_id):
    # 拿到所有高校id
    db = __get_mongo_collection('GaoKao', 'School')
    all = [x for x in db.find({})]

    db = __get_mongo_collection('GaoKao', 'ScoreLine')
    for item in all:
        for y in ['2020', '2019', '2018', '2017', '2016', '2015']:
            print(item['name'] + y+':')
            # 获取某省分数线
            score_line = get_score_line(y, item['school_id'], str(province_id))

            if score_line != None and len(score_line) > 0:
                re = db.insert_many(score_line)
                print('success add:' + str(re.inserted_ids))


def analysis_score_line(province_id):
    # 拿到所有高校id
    schools_db = __get_mongo_collection('GaoKao', 'School')
    schools = [x for x in schools_db.find({}, {'school_id': 1, 'name': 1, 'f985': 1, 'f211': 1, 'dual_class_name': 1})]

    query = {'province_id': str(province_id)}
    db = __get_mongo_collection('GaoKao', 'ScoreLine')
    scores = [x for x in db.find(query, {'average': 0, 'first_km': 0, 'xcelevel_name': 0, 'max': 0, 'sg_fxk': 0, 'sg_sxk': 0,
                                         'sg_type': 0, 'sg_name': 0, 'sg_info': 0, 'xclevel_name': 0, 'zslx': 0, 'xclevel': 0})]

    # 汇总各高校每年的情况
    result = []
    for item in schools:
        current_school = [x for x in scores if x['school_id'] == str(item['school_id'])]
        current_school = sorted(current_school, key=lambda i: i['year'], reverse=True)  # 按年排序
        obj = {
            '校名': item['name'],
        }

        # 处理985/211/双一流显示
        obj['985'] = '985' if item['f985'] == 1 else ''
        obj['211'] = '211' if item['f211'] == 1 else ''
        obj['双一流'] = '双一流' if item['dual_class_name'] == '双一流' else ''

        obj['平均超线'] = None
        obj['平均录取名次'] = None

        # 当前高校每年数据
        current_every_year = {
            'rather': [],
            'min_section': []
        }

        # 处理学校各年分数线
        for y in current_school:
            year = y['year']
            local_batch_name = y['local_batch_name']
            # 2015年前的数据量太少不统计了
            if int(year) <= 2015:
                continue
            # 只统计本科
            if year+'批次' in obj and '本科一批' not in local_batch_name:
                continue

            proscore = y['proscore'] if y['proscore'] != '-' else ''  # 省线
            min = y['min']  # 省线
            rather = double(min)-double(proscore) if proscore != None and proscore != '' and min != None and min != '-' else 0
            obj[year+'批次'] = local_batch_name
            obj[year+'一本线'] = proscore if proscore != '-' else ''
            obj[year+'最低分'] = min if min != '-' else ''
            obj[year+'超线'] = rather if rather > 0 else ''
            obj[year+'录取名次'] = int(y['min_section']) if y['min_section'] != None else ''

            # 超线统计
            if obj[year+'超线'] != '':
                current_every_year['rather'].append(obj[year+'超线'])
            if obj[year+'录取名次'] != '':
                current_every_year['min_section'].append(obj[year+'录取名次'])

        # 求平均值
        avg_line = np.mean(current_every_year['rather'])
        obj['平均超线'] = int(avg_line) if avg_line > 0 else None
        avg_section = np.mean(current_every_year['min_section'])
        obj['平均录取名次'] = int(avg_section) if avg_section > 0 else None

        result.append(obj)

    df = pd.DataFrame(result).sort_values(by='平均超线', ascending=False)
    df.to_excel('../高校历年_' + province_id+'.xlsx', index=False)


try:
    # set_score_line_to_db('62')
    # 山西=14,甘肃=62
    analysis_score_line('14')
    analysis_score_line('62')

    print('成功！')

except Exception as e:
    print('失败！！！')
    print(str(e))
    raise e


# https://gkcx.eol.cn/school/661/provinceline
