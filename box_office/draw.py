#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: draw.py
@time: 2019/3/11 22:16
@desc:
'''
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simhei']

#柱状图
def draw_bar(filename):
    data = pd.read_csv(filename, encoding='gbk')
    total = data.groupby(data['movie_type'])['total'].sum()
    total.plot(kind='bar')
    plt.legend()

    # 添加网格
    plt.grid(linestyle='--', alpha=0.5)

    plt.xlabel("电影类别")
    plt.ylabel("总票房数量")
    plt.title("各类型电影总票房数")

    plt.show()

#散点图
def draw_scatter(filename):
    data = pd.read_csv(filename, encoding='gbk')
    plt.title('总票房和平均票价的关系')
    plt.xlabel('平均票价')
    plt.ylabel('总票房（万）')
    plt.scatter(data.price_average, data.total, color='b', linestyle='--', label='上海')
    plt.show()

#折线图
def draw_plot(filename):
    data = pd.read_csv(filename, encoding='gbk')
    total = data.query('movie_type == "剧情"').head(5).groupby('movie_name')['total'].sum()

    total.plot()
    plt.legend()

    # 添加网格
    plt.grid(linestyle='--', alpha=0.5)

    plt.xlabel("电影")
    plt.ylabel("总票房数量")
    plt.title("剧情类型电影前五票房曲线")

    plt.show()

#饼图
def draw_pie(filename):
    data = pd.read_csv(filename, encoding='gbk')
    total = data.groupby(data['movie_type'], ).size().sort_values(ascending=False).head(5)
    print(total)
    print(total.index)
    plt.title("电影票房前五的类型分布")
    plt.pie(total, autopct='%.2f%%', labels=total.index)
    plt.axis('equal')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    filename = 'box_office.csv'
    # draw_bar(filename)
    # draw_scatter(filename)
    # draw_plot(filename)
    # draw_pie(filename)