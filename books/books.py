#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: tqdm.py
@time: 2019/8/20 14:08
@desc:
'''
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'upgrade-insecure-request': '1',
    'referer': 'https://www.rzlib.net/b/73/73530/',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
}

def get_html(url):
    return requests.get(url, headers=headers)\
        .text.replace('如果您觉得《周睿道德天书》还不错的话，请粘贴以下网址分享给你的QQ、'
                      '微信或微博好友，谢谢支持！', '').replace('（ 本书网址：https://www.'
                                                   'rzlib.net/b/73/73530/ ）', '')


def get_data(url):
    html = etree.HTML(get_html(url))
    title = html.xpath('//h1/text()')[0].replace('.', '_')
    content_url = get_url(url)
    content_html = etree.HTML(get_html(content_url)).xpath('//body//text()')
    content = ["".join(data.split()) for data in content_html]
    return title, content


def get_url(url):
    return "https://www.rzlib.net/b/txtt5552/" + url.split('/')[-2] + "/" + url.split('/')[-1]


def write_data(url):
    title, content = get_data(url)
    with open('books/' + title + '.txt', 'w', encoding='utf-8') as f:
        f.write(title.replace('_', '. ') + '\n')
        for data in content:
            if data != "":
                f.write('  ' + data + '\n')
    with open('books/books.txt', 'a', encoding='utf-8') as p:
        p.write(title.replace('_', '. ') + '\n')
        for data in content:
            if data != "":
                p.write('  ' + data + '\n')
        p.write('\n')



def get_total(index_utl):
    html = etree.HTML(get_html(index_utl))
    urls = html.xpath('//div[@class="ListChapter"][2]/ul/li/a/@href')
    for url in urls:
        write_data("https://www.rzlib.net" + url)
        print("第{}章已完成写入".format(urls.index(url) + 1))


if __name__ == '__main__':
    get_total("https://www.rzlib.net/b/73/73530/")
