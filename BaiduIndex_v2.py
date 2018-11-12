# -*- coding: utf-8 -*-
# @File    : BaiduIndex_v2.py
# @Author  : LVFANGFANG
# @Time    : 2018/11/6 0006 0:25
# @Desc    :
import math

import requests


def search(keyword, days=30):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Cookie': 'PSTM=1510239545; BIDUPSID=C408A63BA03GDGDG8FA66527FA108F531; __cfduid=dbf3906eacc8e3fd98a895c9b068c959c1516637265; BAIDUID=26294E8ECCD5DD9557067AB82EA4E0AC:FG=1; bdshare_firstime=1533800099604; MCITY=-%3A; H_PS_PSSID=1450_21117_27376_27509; BDORZ=FFFB88E999055A3FR900C64834BD6D0; BDRCVFR[08EbrmKd5E_]=aeXf-1x8UdYcs; delPer=0; BDUSS=2NVOWdkV0NCOXdJDLORTI3MHV1VzJOYzg3cExxcFpXTFBtNDJxMmp2Z01LeFZFZzFjQVFBQUFBJCQAAAAAAAAAAAEAAACP8PIteG5iY25iAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFWF5VtVheVbY; PSINO=7; BDSFRCVID=peAsJeCCxG37sLJ7T8vThmbW28FOeQZRddMu3J; H_BDCLCKID_SF=tJDoogC2tKt3qncdq45HMt00qxby26n2HGReaJ5nJDoWMUTMjT_b-U_VhPFHbUJm5mnZQKo-QpP-HqTD0h3YX4Ci0-r8bPQEyJRqKl0MLnclbb0xynoDMnIdgdfgnMBMPeamOnan6_LIFKMCDlej85D5PyMxAX5to05TIX3b7EfhnfftO_bf--DRvWWJ0ft6b20CrA2CoM0hOqshcRDR5xy5K_ytjTQUrwaHvTa4TM54cAh-QHQT3mMlQbbN3i-4jWMe7qWb3cgrgtegt6me65WeaDHt6tsKKJ03bk8KRREJt5kq4bohjPhM-QeBtQm05bxoMcqWKLbeh7O54nWMnkFhMjjhJQDtGTjbhDbWDFabnO1hnofq4D_MfOtetJyaR3T_P5bWJ5TEPnjDp6GLPRWWtc8ajjgLDJOQpnaQfcD8UPCMDF5y6TXjHAjJT0HJb33LPbMHtbHjtTph4JK5t_HMxrK2D62aKDshfTo-hcqEIL4h-cIyb3yjngdsgrnWJTutHT3ob6l3DTcDUbSj4QoQMDTKPoqqpTH-5QDKDovLp5nhMJFXj7JDMP0-lDe-b3y523iob6vQpnVjxtuDjREh40822Ta54cbb4o2WbCQbIJzqpcNLUbWQTJWKPvZtMFLQ2Ju5fTObDnP8n5hWl5fbMu0DPCEJ6n0aDn-XTrtKRTffjrnhPF326QQKP6-3MJO3bAfQhRFJhIBsljHeqPajf_zXUoIXqjb5gjtohFLtCvEDRbN2KTD-tFO5eT22-usfIJWQhOWsI86KUvkjUFPjecRJpR0WK3l2b5lyfofeh6GDUC0DjPthxO-hI6aKC5bL6rJabC3qb5qKU6qLUtbQN-fbM7ZJaPOLfbSaRoRhCnDXPoGWlDOb-ctJMIEK5r2SC8aJK-23J; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1541425553,1541596213,1541606217,1541768576; bdindexid=tggt06ld2g6i5e47coaa26ugm5; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1547760583',
               'Host': 'index.baidu.com',
               'Referer': 'http://index.baidu.com/v2/main/index.html',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    url1 = 'http://index.baidu.com/api/SearchApi/index'
    params1 = {'word': keyword,
               'area': '0',
               'days': days}
    response = requests.get(url1, params=params1, headers=headers)
    jsondata = response.json()
    uniqid = jsondata['data']['uniqid']
    alldata = jsondata['data']['userIndexes'][0]['all']['data']
    print(uniqid)
    print(alldata)

    url2 = 'http://index.baidu.com/Interface/api/ptbk'
    params2 = {'uniqid': uniqid}
    response2 = requests.get(url2, params=params2, headers=headers)
    data = response2.json()['data']
    print(data)

    decrypt(data, alldata)


def decrypt(t, e):
    mid = math.ceil(len(t) / 2)
    n = {t[i]: t[i + mid] for i in range(mid)}
    s = [n[j] for j in e]
    print(s)
    print(len(s))
    print(''.join(s))
    return ''.join(s).split(',')


if __name__ == '__main__':
    search('深圳交警')
