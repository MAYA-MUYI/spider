#!/usr/bin/env python
# -*- coding：utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import csv

def chart():

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
    #z保存所有评论的时间——删除重复项直接用set构造
    z = list(set(xs))
    #y保存评论次数——直接count获取重复次数即可
    for i in ys.values():
        y.append(i)


    plt.figure()
    plt.plot(z, y)
    #标题——各时间段对应评论次数
    plt.title("index for time")
    plt.legend()
    #x轴——评论时间
    plt.xlabel('x-comment_time')
    #y轴——次数
    plt.ylabel('y-index')
    plt.show()


if __name__ == '__main__':
    chart()