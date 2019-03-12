#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 2372836278@qq.com
@software: Pycharm
@file: chart.py
@time: 2018/12/18 19:33
@desc:
'''
import csv
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pylab import *

# 读取商品的评论信息
df = pd.read_csv('comments.csv', encoding='utf-8')
# 设置字体，避免中文出现乱码
# rcParams['font.family'] = "Source Han Serif CN"
mpl.rcParams['font.sans-serif'] = ['SimHei']

# df['顾客会员等级'].replace('PLUS会员[试用]', 'PLUS会员', inplace=True)
labels = list(set(df.顾客会员等级))
sizes = [list(df.顾客会员等级).count(level) for level in list(set(df.顾客会员等级))]
userLevelDataFrame = pd.DataFrame(numpy.array([labels, sizes]).T, columns=['会员级别', '人数'])

#调节图形大小，宽，高
plt.figure(figsize=(12,9))
#定义饼状图的外侧显示的文本标签，标签是列表
labels = sorted(list(set(df.顾客会员等级)))
# 定义饼图的颜色
colors = ['red', 'blue', 'yellow', 'cyan', 'purple', 'orange']
#sizes：设置每个标签在饼图中占多大，本例子是绘制会员分配的饼图
sizes = [list(df.顾客会员等级).count(level) for level in labels]
#将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
explode = (numpy.array([0.02 for i in range(len(labels))]))
#labeldistance，饼图外侧文本的位置离中心点有多远，1.1指1.1倍半径的位置，1表示在饼图的边上，<1表示文字在饼图内
#autopct，圆里面的文本格式，%.2f%%表示小数有两位的浮点数
#shadow，饼是否有阴影
#startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
#pctdistance，百分比的text离圆心的距离
plt.pie(sizes,explode=explode,labels=labels,colors=colors,
        labeldistance = 1.1,autopct = '%.2f%%',shadow = False,
        startangle = 90,pctdistance = 0.6)

# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
# 绘制图例,loc用于设置图例的位置，upper right表示图例位于右上方
plt.legend(loc='upper left')
plt.title('购买商品的会员分配图')
plt.show()

# 缺失值处理
df = df.fillna('不详')

# 根据购物平台的名称，已经购买次数构造一个DataFrame
userClientCol = ['购物平台', '次数']
# 注意：需数组转置
userClientDataFrame = pd.DataFrame(numpy.array([list(set(df.购物使用的平台)), [list(df.购物使用的平台).count(level) for level in list(set(df.购物使用的平台))]]).T, columns=userClientCol)

plt.figure(figsize=(12,9),dpi=120)
labels = list(userClientDataFrame['购物平台'])
plt.bar(range(len(labels)),userClientDataFrame['次数'],tick_label=labels)
plt.title('购物使用的平台')
plt.show()


xs = []
ys = {}
y = []
z = []

#读取数据构造列表

with open('comments.csv', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        result = []
        for row in f_csv:
                if row:
                        # print(row[4])
                        xs.append(row[3][:9])

for x in xs:
        if x in ys:
                ys[x] += 1
        else:
                ys[x] = 1
# z保存所有评论的时间——删除重复项直接用set构造
z = list(set(xs))
# y保存评论次数——直接count获取重复次数即可
for i in ys.values():
        y.append(i)

plt.figure()
plt.plot(z, y)
# 标题——各时间段对应评论次数
plt.title("index for time")
plt.legend()
# x轴——评论时间
plt.xlabel('x-comment_time')
# y轴——次数
plt.ylabel('y-index')
plt.show()
