#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: aqiyi.py.py
@time: 2019/1/18 18:52
@desc:
'''
import requests
from lxml import etree


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
}
def getHtml(url):
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        return r.content
    except:
        return ""

def download(num = 0):
    print("********     开始下载    ********")
    while True:
        url = 'http://acfun.iqiyi-kuyun.com/20181213/HvdhFyz7/1000kb/hls/3A1XxdV7816{}.ts'.format(numFormat(num))
        print("开始下载第{}段：{}".format(num, url.split('/')[-1]))
        response = getHtml(url)
        title_url = 'https://www.iqiyi.com/v_19rre80q80.html#vfrm=2-4-0-1'
        title = etree.HTML(getHtml(title_url)).xpath('//span[@id="widget-videotitle"]/text()')[0]
        if response:
            with open(title+'.ts', 'ab') as f:
                f.write(requests.get(url, headers=headers).content)
            num += 1
        else:
            print("下载结束")
            break


def numFormat(num):
    if len(str(num)) == 1:
        num = '00'+ str(num)
    elif len(str(num)) == 2:
        num = '0' + str(num)
    return num

if __name__ == '__main__':
    download()