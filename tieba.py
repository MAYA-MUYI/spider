#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: tieba.py
@time: 2019/1/4 12:28
@desc:
'''

import requests
import re
import os
import time
import random
from bs4 import BeautifulSoup



class Tool():
    removeImg = re.compile('<img.*?>|｛7｝|&nbsp;') # 去除img标签，1-7位空格，&nbsp;
    removeAddr = re.compile('<a.*?>|</a>') # 删除超链接标签
    replaceLine = re.compile('<tr>|<div>|</div>|</p>') # 把换行的标签换位\n
    replaceTD = re.compile('<td>') # 把表格制表<td>换为\t
    replaceBR = re.compile('<br><br>|<br>|</br>|</br></br>') # 把换行符或者双换行符换为\n
    removeExtraTag = re.compile('.*?') # 把其余标签剔除
    removeNoneLine = re.compile('\n+') # 把多余空行删除

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = re.sub(self.removeNoneLine, "\n", x)
        return x.strip() # 把strip()前后多余内容删除

class Spider():
    def __init__(self):
        self.tool = Tool()

    # 获取源码
    def getSource(self, url):
        user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                       'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                       'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                       'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                       'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
        # user_agent在一堆范围中随机获取
        # random.randint()获取随机数，防止网站认出是爬虫而访问受限
        index = random.randint(0, 9)
        user_agent = user_agents[index]
        headers = {'User_agent': user_agent}
        html = requests.get(url, headers=headers)
        return html.text

    # 获取帖子标题
    def getTitle(self, url):
        result = self.getSource(url)
        pattern = re.compile('<h1.*?title.*?>(.*?)</h1>', re.S)
        items = re.search(pattern, result)
        print('这篇帖子标题为：', self.tool.replace(items.group(1)))

    # 获取帖子总页数
    def getPageNumber(self, url):
        result = self.getSource(url)
        pattern = re.compile('<ul.*?l_posts_num.*?<span class="red">(.*?)</span>', re.S)
        items = re.search(pattern, result).group(1)
        print('帖子共有', items, '页')
        return items

    def getContent(self, url):
        result = self.getSource(url)
        pattern = re.compile('<a data-field.*?p_author_name.*?">(.*?)</a>.*?<div id="post_content_.*?>(.*?)</div>',
                                 re.S)
        items = re.findall(pattern, result)
        # 获取楼层数可以直接用循环，省去正则匹配的麻烦
        number = 1
        for item in items:
            # item[0]为楼主，item[1]为发言内容，使用\n换行符打出内容更干净利落
            # item[1]中可能有img链接，用自定义Tool工具清洗
            print('\n', number, '楼', '\n楼主：', item[0], '\n内容:', self.tool.replace(item[1]))
            time.sleep(0.01)
            number += 1

        # 获取晒图,清洗获得链接并保存入list
    def getImage(self, url):
        result = self.getSource(url)
        soup = BeautifulSoup(result, 'lxml')
        # 此处用BeautifulSoup显然更高效
        # find_all()返回一个list,find()返回一个元素
        # 注意class属性和python内置的重合，所以加_变成class_
        items = soup.find_all('img', class_="BDE_Image")
        images = []
        number = 0
        for item in items:
            print('发现一张图，链接为:', item['src'])
            images.append(item['src'])
            number += 1
        if number >= 1:
            print('\n', '共晒图', number, '张，厉害了我的哥！！！')
        else:
            print('喏，没有图......')
        return images

    # 创建目录
    def makeDir(self, path):
        self.path = path.strip()
        # E = os.path.exists(os.path.join(os.getcwd(), self.path))
        E = os.path.exists(self.path)
        if not E:
            # 创建新目录,若想将内容保存至别的路径（非系统默认），需要更环境变量
            # 更改环境变量用os.chdir()
            # os.makedirs(os.path.join(os.getcwd(), self.path))
            os.mkdir(self.path)
            # os.chdir(os.path.join(os.getcwd(), self.path))
            print('正在创建名为', self.path, '的文件夹')
            return self.path
        else:
            print('名为', self.path, '的文件夹已经存在...')
            return False

    def saveImage(self, detailURL, name):
        try:
            data = requests.get(detailURL, timeout=10).content
            # 保存文件，一定要用绝对路径      `
            # 所以设置self.path，是为了方便后面函数无障碍调用
        except requests.exceptions.ConnectionError:
            print('下载图片失败')
            return None
        fileName = name + '.' + 'jpg'
        fileName = os.path.join(self.path, name+'.jpg')
        f = open(fileName, 'wb')
        f.write(data)
        f.close()
        print('成功保存图片', fileName)

    def getAllPage(self):
        self.siteURL = 'http://tieba.baidu.com/p/5862596971'
        # 获取帖子标题
        self.getTitle(self.siteURL)
        # 获取帖子页数
        numbers = self.getPageNumber(self.siteURL)
        for page in range(1, int(numbers) + 1):
            # 格式化索引链接
            self.url = self.siteURL + '?pn=' + str(page)
            print('\n\n', '正准备获取第', page, '页的内容...')
            # 获取评论
            print('\n', '正准备获取评论...')
            self.getContent(self.url)
            # 每一页创建一个文件
            self.makeDir(path='page' + str(page))
            # 获取图片
            print('\n', '正准备获取图片...')
            images = self.getImage(self.url)
            print('\n', '正准备保存图片...')
            number = 1
            # 保存图片，先从之前的list中找链接
            for detailURL in images:
                name = 'page' + str(page) + '_'+'num' + str(number)
                self.saveImage(detailURL, name)
                time.sleep(0.1)
                number += 1

            print('\n\n', '完成第', page, u'页')
        print('\n\n', '恭喜，圆满成功！')

if __name__ == '__main__':
    spider = Spider()
    spider.getAllPage()
