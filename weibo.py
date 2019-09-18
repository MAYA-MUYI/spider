#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: weibo.py
@time: 2019/9/5 14:26
@desc:
'''
import requests
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/74.0.3729.169 Safari/537.36',
    'referer': 'https://m.weibo.cn/u/2028810631?uid=2028810631&luicode=1000'
               '0011&lfid=100103type%3D17%26q%3D%E6%96%B0%E9%97%BB'
}


def get_html(url):
    return requests.get(url, headers=headers).text


def parse_data(url):
    text = json.loads(get_html(url))
    datas = text['data']['cards']
    result = []
    for data in datas:
        result.append([
            data['mblog']['created_at'],
            re.sub('(<.*?>)', '', data['mblog']['text'])
        ]
        )
    return result


def write_data(result):
    for data in result:
        with open('weibo.txt', 'a', encoding='utf-8') as f:
            f.write(data[0] + ':' + data[1] + '\n')



def main(num):
    for i in range(1, num + 1):
        url = 'https://m.weibo.cn/api/container/getIndex?uid=2028810631&luicode=10000011&lfid=100103type%3D17%26q%3D%' \
              'E6%96%B0%E9%97%BB&type=uid&value=2028810631&containerid=1076032028810631&page={}'.format(i)
        write_data(parse_data(url))
        print("完成第{}页".format(i))



if __name__ == '__main__':
    main(10)
