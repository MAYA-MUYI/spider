#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 2372836278@qq.com
@software: Pycharm
@file: word_cloud.py
@time: 2018/12/18 20:04
@desc:
'''
#导入wordcloud模块和matplotlib模块
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread
import codecs
import json
import csv
import pandas as pd


with open('comments.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    result = []
    for row in f_csv:
        if row:
            # print(row[4])
            result.append(row[2])


text = "".join(result)


#读入背景图片

bg_pic = imread('cloud.jpg')

#生成词云

wordcloud = WordCloud(mask=bg_pic,background_color='white',scale=1.5, font_path = 'msyh.ttf').generate(text)

image_colors = ImageColorGenerator(bg_pic)
#显示词云图片

plt.imshow(wordcloud)
plt.axis('off')
plt.show()


#保存图片

wordcloud.to_file('词云.jpg')
