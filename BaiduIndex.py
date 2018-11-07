# -*- coding: utf-8 -*-
# @File    : BaiduIndex.py
# @Author  : LVFANGFANG
# @Time    : 2018/8/14 0011 10:48
# @Desc    : 百度指数
import datetime
import json
import logging
import random
import re
import time
import urllib
from collections import defaultdict
from io import BytesIO

import pytesseract
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BaiduIndex:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.login()

    def login(self):
        self.driver.get('http://index.baidu.com/?from=pinzhuan#/')
        # 添加登录cookies
        with open('cookie_dict.json') as f:
            cookies = json.load(f)
        for c in cookies:
            self.driver.add_cookie(c)

    def search(self, keyword):
        WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.ID, 'index-login-block')))
        self.searchurl = 'http://index.baidu.com/?tpl=trend&word={}'.format(urllib.parse.quote(keyword, encoding='GBK'))
        self.driver.get(self.searchurl)
        res = self.driver.execute_script('return PPval.ppt')
        res2 = self.driver.execute_script('return PPval.res2')
        res3 = self.get_res3(res, res2, keyword)
        data_list = []
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for k in res3:
            index = self.get_view(res, res2, res3[k])
            logger.info(keyword + ' ' + k + ' ' + index)
            data_list.append({'search': 'baidu', 'value': index, 'dateInfo': k, 'keyword': keyword})
        if not data_list:
            logger.warning('未更新')

    def get_headers(self):
        cookie = self.driver.get_cookies()
        cookiestr = ';'.join(item for item in [i['name'] + '=' + i['value'] for i in cookie])
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': cookiestr,
            'Host': 'index.baidu.com',
            'Referer': self.searchurl,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        return headers

    def get_res3(self, res, res2, keyword):
        startdate = datetime.date.today() - datetime.timedelta(days=30)
        enddate = datetime.date.today() - datetime.timedelta(days=1)
        url = 'http://index.baidu.com/Interface/Search/getSubIndex/'
        params = {
            'res': res,
            'res2': res2,
            'type': '0',
            'startdate': startdate.strftime('%Y-%m-%d'),
            'enddate': enddate.strftime('%Y-%m-%d'),
            'forecast': '0',
            'word': keyword}
        headers = self.get_headers()
        response = requests.get(url, params=params, headers=headers)
        result = {}
        if response.json()['status'] == '0':
            data = response.json()['data']['all']
            res3 = data[0]['userIndexes_enc'].split(',')
            date_list = [startdate.strftime('%Y-%m-%d')]
            while startdate < enddate:
                startdate += datetime.timedelta(days=1)
                date_list.append(startdate.strftime('%Y-%m-%d'))
            result = dict(zip(date_list, res3))
        return result

    def get_view(self, res, res2, res3):
        url = 'http://index.baidu.com/Interface/IndexShow/show/'
        params = {
            'res': res,
            'res2': res2,
            'classType': '1',
            'res3[]': res3,
            'className': 'view-value',
            str(int(time.time() * 1000)): ''}
        headers = self.get_headers()
        response = requests.get(url, params=params, headers=headers)
        if response.json()['status'] != '0':
            return None
        code = response.json()['data']['code'][0]
        background_url = 'http://index.baidu.com' + re.findall('background:url\(\\"(.+?)\\"\)', code)[0]
        # print(background_url)
        image = self.download_img(background_url)

        region = defaultdict(list)
        result = re.findall(
            '<span\s+class="imgval"\s+style="width:(\d+)px;"><div\s+class="imgtxt"\s+style="margin-left:-(\d+)px;"></div></span>',
            code)
        for i in result:
            region['width'].append(int(i[0]))
            region['margin_left'].append(int(i[1]))

        image = Image.open(BytesIO(image))
        hight = image.size[1]
        target = Image.new('RGB', (sum(region['width']), hight))
        for i in range(len(region['width'])):
            img = image.crop((region['margin_left'][i], 0, region['margin_left'][i] + region['width'][i], hight))
            target.paste(img, (sum(region['width'][0:i]), 0, sum(region['width'][0:i + 1]), hight))

        text = pytesseract.image_to_string(target, lang='index').replace(',', '').replace(' ', '').strip()
        return text

    def download_img(self, url):
        headers = self.get_headers()
        headers['Accept'] = 'image/webp,image/apng,image/*,*/*;q=0.8'
        r = requests.get(url, headers=headers)
        return r.content

    def quit(self):
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('baiduindex.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    try:
        index = BaiduIndex()
        index.search('深圳交通')
        index.search('深圳交警')
        index.quit()
    except Exception as e:
        logger.exception(e)
