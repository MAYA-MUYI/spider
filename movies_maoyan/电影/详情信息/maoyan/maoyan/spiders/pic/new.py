
#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: new.py
@time: 2019/5/30 18:30
@desc:
'''
import requests
from lxml import etree

url = "https://maoyan.com/films/78304"
headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
            'Referer': 'https://maoyan.com/'
        }
r = requests.get(url, headers=headers).text
html = etree.HTML(r)
# print(r)
url_list = html.xpath('//div[@class="img1"]/img/@data-src')
print(url_list)