#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: test.py
@time: 2019/5/30 16:37
@desc:
'''
import os
import requests
from lxml import etree


class Download():
    def __init__(self):
        self.getHtmlHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
            # 'Referer': 'https://maoyan.com/'
        }

    def getHtml(self, url):
        r = requests.get(url, self.getHtmlHeaders)
        return r.text

    def getInfo(self, text):
        html = etree.HTML(text)
        url_list = html.xpath('//div[@class="movie-item"]/a/@href')
        for _url in url_list:
            _html = etree.HTML(self.getHtml("https://maoyan.com" + _url))
            pic = self.pic_format("".join(_html.xpath('//div[@class="avatar-shadow"]/img/@src')))
            # timg = _html.xpath('//div[@class="img1"]/img/data-src')
            # print(pic)
            # print(timg)
            timg = self.pic_format("".join(_html.xpath('//div[@class="img1"]/img/@data-src')))
            stills1 = self.pic_format("".join(_html.xpath('//div[@class="img2"]/img/@data-src')))
            stills2 = self.pic_format("".join(_html.xpath('//div[@class="img3"]/img/@data-src')))
            stills3 = self.pic_format("".join(_html.xpath('//div[@class="img4"]/img/@data-src')))
            stills4 = self.pic_format("".join(_html.xpath('//div[@class="img5"]/img/@data-src')))
            name = _html.xpath('//h3[@class="name"]/text()')[0]
            pic_dic = {
                # "name": name,
                "pic": pic,
                "timg": timg,
                "stills1": stills1,
                "stills2": stills2,
                "stills3": stills3,
                "stills4": stills4,
            }
            # print(pic_dic)
            self.down(name, pic_dic)

    def down(self, name, dic):
        for data in dic.items():
            print("开始下载:" + name + '_' + data[0] + '.jpg')
            with open('pic/' + name + "_" + data[0] + '.jpg', 'wb') as f:
                f.write(requests.get(data[1], self.getHtmlHeaders).content)

    def pic_format(self, src):
        (filename, extension) = os.path.splitext(src)
        if extension == '.jpg' or extension == '.png':
            pass
        else:
            src = src.split(extension[:4])[0] + extension[:4]
        return src

    def run(self):
        url = "https://maoyan.com"
        self.getInfo(self.getHtml(url))

if __name__ == '__main__':
    m = Download()
    m.run()


