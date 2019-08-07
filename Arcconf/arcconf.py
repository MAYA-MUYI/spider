#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@software: Pycharm
@file: arcconf.py
@time: 2019/8/6 16:30
@desc:
'''
import requests
from lxml import etree
from lxml.etree import tostring
import re
import os
import subprocess

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 '
                  'Safari/537.36',
    'upgrade-insecure-requests': '1',
}


def get_html(url):
    r = requests.get(url, headers=headers)
    return r.text


def get_order(rule):
    tmp = []
    if len(rule.xpath('./p')) > 1:
        for data in rule.xpath('./p'):
            tmp.append(" ".join(data.xpath('.//text()')))
    else:
        tmp.append(" ".join(rule.xpath('./p//text()')))
    return tmp


def get_data_html(text):
    text = re.sub('</strong>', '', re.sub('<strong.*?>', '', re.sub('</em>', '', re.sub('<em.*?>', '', text))))
    html = etree.HTML(text)
    title = re.findall('<h4.*?>(.*?)</h4>', text)#列表
    order = []
    order_divs = html.xpath('//h5[contains(text(), "命令格式")]/parent::div')
    for div in order_divs:
        order.append(get_order(div))
    function = re.findall('<h5.*?>命令功能</h5>.*?<p.*?>(.*?)</p>', text)#列表
    tabs_html = html.xpath('//table[@class="idp-ltr-html-tb-normal"]')
    tabs = [tostring(data).decode() for data in tabs_html]
    tutor_divs = html.xpath('//h5[contains(text(), "使用指南")]/parent::div')
    tutor = []#保存使用指南的嵌套列表
    for div in tutor_divs:
        tutor.append(get_tutor(div))
    exams = []
    exams_title = []
    exams_html = html.xpath('//h5[contains(text(), "使用实例")]/parent::div')
    for exam in exams_html:
        tmp_title, tmp = get_exams(exam)
        exams_title.append(tmp_title)
        exams.append(tmp)
    return title, function, order, tabs, tutor, exams_title, exams


def dir_init(dir, path='.'):
    if dir not in os.listdir(path):
        os.mkdir(dir)
    os.chdir(dir)
    subprocess.Popen('gitbook init', shell=True)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("# Operations Notes\n")
        f.write("\n")
        f.write(">用以记录运维学习过程中的工作记录以及命令操作")
    with open('SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write("# CATALOG —— Operations Notes\n")
        f.write("\n")
        f.write("* [简介](README.md)\n")
        f.write("\n")
        f.write("* [Arcconf ](arcconf.md)\n")
    with open('arcconf.md', 'w', encoding='utf-8') as f:
        f.write("# Arcconf操作指南\n")
        f.write("\n")
        f.write(">记录Arcconf的命令操作\n")





def write_md(url):
    title, function, order, tabs, tutor, exams_title, exams = get_data_html(get_html(url))
    # 准备目录文件
    with open('SUMMARY.md', 'a', encoding='utf-8') as f:
        for title_ in title:
            f.write("  - [{}]({}.md)\n".format(title_, title_.replace('/', '_')))

    for title__ in list(enumerate(title)):
        with open(title__[1].replace('/', '_') + '.md', 'a', encoding='utf-8') as f:
            # title__[0]是位置，title__[1]是名称
            f.write("# {}\n".format(title__[1]))
            f.write("\n")
            f.write("## 命令功能\n")
            f.write(">{}\n".format(function[title__[0]]))
            f.write("\n")
            f.write("## 命令格式\n")
            if len(order[title__[0]]) == 1:
                for data in order[title__[0]]:
                    f.write("`{}`\n".format(data))
            else:
                f.write("~~~\n")
                for data in order[title__[0]]:
                    f.write("{}\n".format(data))
                f.write("~~~\n")
            f.write("\n")
            f.write("## 参数说明\n")

            title, line, body = get_data(tabs[title__[0]])
            result = [" | ".join(data) for data in body]
            f.write("| " + "| ".join(title) + "|" + "\n")
            f.write("| " + " | ".join(line) + "|" + "\n")
            for data in result:
                f.write("| " + data + "|" + "\n")
            # write_data(tabs[title__[0]], title__[1] + ".md")
            f.write("\n")
            f.write("使用指南\n")
            for data in tutor[title__[0]]:
                f.write("- {}\n".format(data))
            f.write("\n")
            f.write("使用实例\n")
            f.write("~~~\n")
            if len(exams_title[title__[0]]) > 1:
                f.write("{}\n".format(str("&".join(exams_title[title__[0]]).replace("#", ""))))
            else:
                f.write("{}\n".format(str(exams_title[title__[0]][0])))
            for data in exams[title__[0]]:
                f.write("{}\n".format(data))
            f.write("~~~\n")
    subprocess.Popen('gitbook serve', shell=True)


def get_exams(div):
    tmp, tmp_title = [], []
    if div.xpath('./p[@id]'):
        tmp_title.extend(div.xpath('./p[@id]//text()'))
    if div.xpath('.//pre'):
        for pre in div.xpath('.//pre'):
            single = pre.xpath('./text()')
            tmp.append("".join(single))
    return tmp_title, tmp


def get_tutor(div):
    tmp = []
    if div.xpath('.//p[@id]'):
        tmp.extend(div.xpath('.//p[@id]//text()'))
    if div.xpath('.//div[@class="idp-ltr-html-noticebody"]'):
        tmp.extend(div.xpath('.//div[@class="idp-ltr-html-noticebody"]/p//text()'))
    return tmp


def get_data(table):
    html = etree.HTML(table)
    body = []
    head = html.xpath('//table/thead/tr')
    # 获取表头
    title = [th.xpath('.//p//text()') for th in head][0]
    # #根据表头长度确定符号线
    line = ["----"] * len(title)
    # 获取表格内容并用嵌套的列表保存
    tbody = html.xpath('//table/tbody/tr')
    for tr in tbody:
        body.append(list_format(tr, len(title)))
    return title, line, body


def list_format(rule, num):
    tmp = []
    for i in range(num):
        try:
            data = rule.xpath('./td/p//text()')[i]
            tmp.append(data)
        except:
            data = " ".join(rule.xpath('./td[{}]/ul/li//text()'.format(i+1)))
            tmp.append(data)
    return tmp


def print_data(table):
    title, line, body = get_data(table)
    # 用"|"分隔获取到的数据并依次打印
    result = [" | ".join(data) for data in body]
    print("| " + "| ".join(title) + "|")
    print("| " + " | ".join(line) + "|")
    for data in result:
        print("| " + data + "|")


def write_data(table, filename):
    title, line, body = get_data(table)
    result = [" | ".join(data) for data in body]
    with open(filename.replace('/', '_'), 'a', encoding='utf-8') as f:
        f.write("| " + "| ".join(title) + "|" + "\n")
        f.write("| " + " | ".join(line) + "|" + "\n")
        for data in result:
            f.write("| " + data + "|" + "\n")


def main():
    url = "https://support.huawei.com/enterprise/zh/doc/EDOC1000004345/b4d43c54#ZH-CN_TOPIC_0096572531"
    # get_data_html(get_html(url))
    dir_init("Arcconf")
    write_md(url)



if __name__ == '__main__':
    main()