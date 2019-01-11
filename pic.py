#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: pic.py
@time: 2018/12/19 16:13
@desc:
'''
import requests
import re
import time


class PicThousand():
    def __init__(self):
        self.getHtmlHeaders={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',

        }

    def getHtml(self, url):
        response = requests.get(url, self.getHtmlHeaders).text
        return response

    def getUrl(self, text):
        image_urls = re.compile('data-original="(.*?)"', re.S).findall(text)
        return image_urls

    def img_Download(self, url_list):
        for index in range(len(url_list)):
            url = url_list[index].replace('!qt324', '')
            self.getHtmlHeaders['Referer'] = url
            file_name = url.replace('!qt324', '').split('/')[-1]
            print("正在下载第%s张图片:%s" % (index + 1, file_name))
            response = requests.get(url, headers= self.getHtmlHeaders)
            with open('img/'+file_name, 'wb') as f:
                f.write(response.content)

    def run(self, url):
        text = self.getHtml(url)
        list = self.getUrl(text)
        self.img_Download(list)


if __name__ == '__main__':

    start = time.time()
    for n in range(0, 11):
        print("******** 正在下载第%s页的图片 ********" % (n+1))
        html_url = "http://www.58pic.com/tupian/jianshen-0-0-{}.html".format(n)
        PicThousand().run(html_url)
    end = time.time()
    print("******** 下载完成，共用时%.2f    ********" % (end-start))
