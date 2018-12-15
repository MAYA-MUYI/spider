#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8

#导入wordcloud模块和matplotlib模块
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread
import codecs
import json


#读取一个txt文件
f = codecs.open('positions.json', 'r', encoding='utf-8')
lines = f.readlines()
result = []
for line in lines:
    line = json.loads(line)['positionAdvantage']
    result.append(line)

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

wordcloud.to_file('test.jpg')
