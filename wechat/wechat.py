#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: wechat.py
@time: 2019/9/10 15:00
@desc:
'''
import time
import requests
import threading
import json
import random
import re
from selenium import webdriver


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class Public(metaclass=SingletonType):
    def __init__(self, search_key, token, cookie):
        self.search_key = search_key
        self.url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36'
        }
        self.data = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': '0.012103784566473319',
            'query': self.search_key,
            'count': '5'
        }

    def get_total(self):
        self.data['begin'] = 0
        content = requests.get(self.url, headers=self.headers, params=self.data).json()
        total = content['total']
        if total % 5:
            return int(total / 5) + 1
        else:
            return int(total / 5)

    def parse_public(self, num):
        self.data['begin'] = num
        content = requests.get(self.url, headers=self.headers, params=self.data).json()
        return content

    def get_data(self):
        for num in range(0, self.get_total() + 1, 5):
            for data in self.parse_public(num)['list']:
                yield {
                    "name": data['nickname'],
                    "id": data['fakeid'],
                    'number': data['alias']
                }
            time.sleep(random.randint(1, 3))


class Articls(metaclass=SingletonType):
    def __init__(self, token, fakeid, cookie, search_key=""):
        self.search_key = search_key
        self.url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        self.headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36',
            'host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
        self.data = {
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "action": "list_ex",
            "count": "5",
            "query": self.search_key,
            "fakeid": fakeid,
            "type": "9",
        }

    def parse_articles(self, num):
        self.data['begin'] = num
        content = requests.get(self.url, headers=self.headers, params=self.data).json()
        return content

    def get_total(self):
        self.data['begin'] = 0
        content = requests.get(self.url, headers=self.headers, params=self.data).json()
        total = content['app_msg_cnt']
        if total % 5:
            return int(total / 5) + 1
        else:
            return int(total / 5)

    @staticmethod
    def convert_2_time(stamp):
        return time.strftime("%Y-%m-%d", time.localtime(stamp))


    def get_data(self):
        if self.get_total():
            for num in range(0, self.get_total() + 1, 5):
                for data in self.parse_articles(num)['app_msg_list']:
                    yield {
                        "title": data['title'],
                        "create_time": self.convert_2_time(data['create_time']),
                        # 摘要
                        'digest': data['digest'],
                        'link': data['link']
                    }
                time.sleep(random.randint(1, 3))
        else:
            print("No search item")
            exit()



def write_data(result, filename):
    for data in result:
        print(data)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')


def login(username, passwd):
    cookies = {}
    driver = webdriver.Chrome()  # 谷歌驱动
    driver.get('https://mp.weixin.qq.com/')

    # 用户名
    driver.find_element_by_xpath('//input[@name="account"]').clear()
    driver.find_element_by_xpath('//input[@name="account"]').send_keys(username)
    driver.find_element_by_xpath('//input[@name="password"]').clear()
    driver.find_element_by_xpath('//input[@name="password"]').send_keys(passwd)
    # 登录
    driver.find_element_by_xpath('//a[@class="btn_login"]').click()
    time.sleep(20)
    # 获取cookie
    driver.get('https://mp.weixin.qq.com/')
    time.sleep(5)
    cookie_items = driver.get_cookies()
    for cookie_item in cookie_items:
        cookies[cookie_item['name']] = cookie_item['value']
    with open('cookie.txt', 'w') as f:
        f.write(json.dumps(cookies))
    driver.close()


def get_cookie_token():
    url = 'https://mp.weixin.qq.com'
    header = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36',
        'host': 'mp.weixin.qq.com',
    }

    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    response = requests.get(url=url, cookies=cookies)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    result = []
    for k, v in cookies.items():
        result.append(k + '=' + v)
    return "; ".join(result), token


if __name__ == '__main__':
    login('你的账号', '你的密码')
    cookies, token = get_cookie_token()

    # 获取公众号信息
    public_result = Public('NBA', token, cookies).get_data()
    write_data(public_result, 'publics2.txt')

    # 获取文章信息
    article_result = Articls(token, 'MjM5ODEwODcyMA==', cookies).get_data()
    write_data(article_result, 'articles.txt')


