#!/usr/bin/python
#-*-coding:utf-8 -*-
import json
import codecs


def get_data(position):
    result = []
    position = position.strip()
    f = codecs.open('positions.json', 'r', encoding='utf-8')
    for lines in f.readlines():
        line = json.loads(lines)
        # print(line)
        if (line['position_name'] == position):
            result.append(line)
    if result:
        for i in result:
            print(i)
    else:
        print("***对不起，暂无相关职位，建议核实搜索项或者查看其它职位信息***")


def main():
    get_data(position)

if __name__ == '__main__':
    position = input("请输入职位：\n")
    main()