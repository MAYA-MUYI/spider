#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: jinri.py
@time: 2019/9/5 15:26
@desc:
'''

import requests
import os
import time

headers = {
    'authority': 'www.toutiao.com',
    'method': 'GET',
    'path': '/api/search/content/?aid=24&app_name=web_search&offset=100&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1556892118295',
    'scheme': 'https',
    'accept': 'application/json, text/javascript',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


def get_html(url):
    return requests.get(url, headers=headers).json()


def get_values_in_dict(list):
    result = []
    for data in list:
        result.append(data['url'])
    return result


def parse_data(url):
    text = get_html(url)
    for data in text['data']:
        if 'image_list' in data.keys():
            title = data['title'].replace('|', '')
            img_list = get_values_in_dict(data['image_list'])
        else:
            continue
        if not os.path.exists('街拍/' + title):
            os.makedirs('街拍/' + title)

        for index, pic in enumerate(img_list):
            with open('街拍/{}/{}.jpg'.format(title, index + 1), 'wb') as f:
                f.write(requests.get(pic).content)
        print("Download {} Successful".format(title))


def get_num(num):
    if isinstance(num, int) and num % 20 == 0:
        return num
    else:
        return 0


def main(num):
    for i in range(0, get_num(num) + 1, 20):
        url = 'https://www.toutiao.com/api/search/content/?aid={}&app_name={}&offset={}&format={}&keyword={}&' \
              'autoload={}&count={}&en_qc={}&cur_tab={}&from={}&pd={}&timestamp={}'.format(24, 'web_search', i,
              'json', '街拍', 'true', 20, 1, 1, 'search_tab', 'synthesis', str(time.time())[:14].replace('.', ''))
        parse_data(url)


if __name__ == '__main__':
    main(40)
