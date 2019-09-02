#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: house.py
@time: 2019/8/28 9:24
@desc:
'''

import requests
import xlwt
import math
from lxml import etree
import re
import pytesseract
from PIL import Image


def get_html(url, headers):
    return requests.get(url, headers=headers).text


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def house_zr(headers):
    index_url = 'http://cd.ziroom.com/z/'
    html = etree.HTML(get_html(index_url, headers))
    total = html.xpath('//div[@class="Z_pages"]/a[position()=last()-1]/text()')[0]
    result = []
    for num in range(1, int(total) + 1):
        result += get_this_page_zr('http://cd.ziroom.com/z/p{}/'.format(num), [])
        print('完成读取第{}页/自如网'.format(num))
    return result


def get_this_page_zr(url, tmp):
    html = etree.HTML(requests.get(url).text)
    divs = html.xpath('//div[@class="item"]')
    for div in divs:
        if div.xpath('./div[@class="info-box"]/h5/a/text()'):
            title = div.xpath('./div[@class="info-box"]/h5/a/text()')[0]
        else:
            continue
        link = 'http:' + div.xpath('./div[@class="info-box"]/h5/a/@href')[0]
        location = div.xpath('./div[@class="info-box"]/div[@class="desc"]/div[@class="location"]/text()')[0]
        area = div.xpath('./div[@class="info-box"]/div[@class="desc"]/div[contains(text(), "㎡")]/text()')[0]
        price_strings = div.xpath('./div[@class="info-box"]/div[@class="price"]/span[@class="num"]/@style')
        offset_list = []
        for data in price_strings:
            offset_list.append(re.findall('position: (.*?)px', data)[0])
        style_string = html.xpath('//div[@class="info-box"]/div[@class="price"]/span[@class="num"]/@style')[0]
        pic = "http:" + re.findall(r'background-image: url\((.*?)\);.*?', style_string)[0]
        price = get_price_zr(pic, offset_list)
        tag = '、'.join(div.xpath('./div[@class="info-box"]//div[@class="tag"]/span/text()'))
        tmp.append([
            title, tag, price, area, location, link
        ])
    return tmp


def get_this_page_gj(url, tmp):
    html = etree.HTML(requests.get(url).text)
    divs = html.xpath('//div[@class="f-list-item ershoufang-list"]')
    for div in divs:
        title = div.xpath('./dl/dd[@class="dd-item title"]/a/text()')[0]
        house_url = div.xpath('./dl/dd[@class="dd-item title"]/a/@href')[0]
        size = "、".join(div.xpath('./dl/dd[@class="dd-item size"]/span/text()'))
        address = '-'.join([
            data.strip() for data in divs[0].xpath('./dl/dd[@class="dd-item address"][1]//a//text()')
            if data.strip() != ''
        ]
        )
        agent_string = div.xpath('./dl/dd[@class="dd-item address"][2]/span/span/text()')[0]
        agent = re.sub(' ', '', agent_string)
        price = div.xpath('./dl/dd[@class="dd-item info"]/div[@class="price"]/span[@class="num"]/text()')[0]
        tmp.append([
            title, size, price, address, agent, house_url
        ])
    return tmp


def house_gj(headers):
    index_url = 'http://cd.ganji.com/zufang/'
    html = etree.HTML(get_html(index_url, headers))
    total = html.xpath('//div[@class="pageBox"]/a[position() = last() -1]/span/text()')[0]
    result = []
    for num in range(1, int(total) + 1):
        result += get_this_page_gj('http://cd.ganji.com/zufang/pn{}'.format(num), [])
        print('完成读取第{}页/赶集网'.format(num))
    return result


def get_price_zr(pic_url, offset_list):
    '''
        这里的index保存所有数字的下标值，等待图片解析完成获取对应下标的价格数字
    '''
    index, price = [], []
    with open('pic.png', 'wb') as f:
        f.write(requests.get(pic_url).content)
    code_list = list(pytesseract.image_to_string(Image.open('pic.png')))
    for data in offset_list:
        index.append(int(math.fabs(eval(data)/21.4)))
    for data in index:
        price.append(code_list[data])
    return "".join(price)



def write_excel(result_gj, result_zr):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('赶集', cell_overwrite_ok=True)
    sheet2 = f.add_sheet('自如', cell_overwrite_ok=True)
    row_zr = ["标题", "标签", "价格(元/月)", "大小", "位置", "网页链接"]
    row_gj = ["标题", "简介", "价格(元/月)", "位置", "中介", "网页链接"]
    num_gj, num_zr = 1, 1
    default_style = set_style('Times New Roman', 300, False)
    for i in range(0, len(row_gj)):
        sheet1.col(i).width = 256 * 50
        sheet1.write(0, i, row_gj[i], set_style('Times New Roman', 260, True))
    for i in range(0, len(row_zr)):
        sheet2.col(i).width = 256 * 50
        sheet2.write(0, i, row_zr[i], set_style('Times New Roman', 260, True))
    for data in result_gj:
        for i in range(0, len(row_gj)):
            sheet1.write(num_gj, i, data[i], default_style)
        num_gj += 1
    for data in result_zr:
        for i in range(0, len(row_zr)):
            sheet2.write(num_zr, i, data[i], default_style)
        num_zr += 1
    f.save('houses.xls')


def run():
    headers_gj = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }

    headers_zr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    result1 = house_gj(headers_gj)
    result2 = house_zr(headers_zr)
    write_excel(result1, result2)
    print("******** 完成 ********")


if __name__ == '__main__':
    run()
