#!/usr/bin/python
#-*-coding:utf-8 -*-
import csv
import re
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']


import codecs
import json
def show():
    f = codecs.open('positions.json', 'r', encoding='utf-8')
    plt.figure(figsize=(10, 6))
    x = []  # 存放x轴数据
    y = []
    tmp_x = []
    # result = ''.join(re.findall(r'[A-Za-z]', st))
    for line in f.readlines():
        data = json.loads(line, encoding='utf-8')
        position_name = data['position_name']
        if position_name.count(''.join(re.findall(r'[A-Za-z]', position_name)).lower()) ==1:
            if len(position_name)<=9:
                x.append(data["position_name"])
                y.append(data["salary"])

    plt.bar(x, y, label="salary")
    plt.title("各岗位工资梯度")
    plt.legend()
    plt.xlabel('x轴-position')
    plt.ylabel('y轴-sarly')
    plt.show()

if __name__ == '__main__':
    show()