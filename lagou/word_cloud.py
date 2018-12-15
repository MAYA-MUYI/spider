#!/usr/bin/python
#-*-coding:utf-8 -*-
# import pandas as pd
import matplotlib.pyplot as plt
# import statsmodels.api as sm
from wordcloud import WordCloud
from scipy.misc import imread
import jieba
import json
from pylab import mpl
import codecs


f = codecs.open('positions.json', 'r', encoding='utf-8')
lines = f.readlines()
result = []
for line in lines:
    line = json.loads(line)['positionAdvantage']
    result.append(line)
# text = ' '.join(jieba.cut(line))
text = "".join(result)
cut_text = ' '.join(jieba.cut(text))
color_mask = imread('cloud.jpg')  #设置背景图
cloud = WordCloud(
        font_path = 'msyh.ttf',
        background_color = 'white',
        mask = color_mask,
        max_words = 1000,
        max_font_size = 100
        )

word_cloud = cloud.generate(cut_text)
# 保存词云图片
word_cloud.to_file('word_cloud.jpg')
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
