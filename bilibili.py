#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: bilibili.py
@time: 2018/12/18 12:52
@desc:
'''
import requests
import re
import json
from lxml import etree
from requests import RequestException

class bilibili():
    def __init__(self):
        self.getHtmlHeaders={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7'
        }

        self.downloadVideoHeaders={
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av26522634',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

    def getHtml(self, url):
        try:
            response = requests.get(url=url, headers=self.getHtmlHeaders)
            print(response.status_code)
            if response.status_code == 200:
                # print(response.text)
                return response
        except RequestException:
            print('请求Html错误:')


    def parseHtml(self, response):
        html = etree.HTML(response.text)
        video_title = html.xpath('//div[@id="viewbox_report"]/h1/span/text()')[0]
        # 用正则、json得到视频url;
        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        result = re.findall(pattern, response.text)[0]
        temp = json.loads(result)
        # temp['durl']是一个列表，里面有很多字典
        video_url = temp['data']['durl']
        for item in temp['data']['durl']:
            if 'url' in item.keys():
                video_url = item['url']
        # print(video_url)
        return {
            'title': video_title,
            'url': video_url
        }

    def download_video(self, video):
        title = re.sub(r'[\/:*?"<>|]', '-', video['title'])  # 去掉创建文件时的非法字符
        url = video['url']
        filename = title + '.flv'
        print("*******  start   ********")
        print("正在下载视频：%s" % title)
        with open(filename, "wb") as f:
            f.write(requests.get(url=url, headers=self.downloadVideoHeaders, stream=True, verify=False).content)
            f.flush()
        print("**************************")
        print("下载完成")
        print("******** end ********")

    def run(self, url):
        self.download_video(self.parseHtml(self.getHtml(url)))


if __name__ == '__main__':
    url = "https://www.bilibili.com/video/av38926293?spm_id_from=333.334.b_62696c695f646f756761.3"
    bilibili().run(url)