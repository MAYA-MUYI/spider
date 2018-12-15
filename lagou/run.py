#!/usr/bin/python
#-*-coding:utf-8 -*-
import json
import codecs
import msvcrt


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
        print(" ***对不起，暂无相关职位，建议核实搜索项或者查看其它职位信息***")
    print("")


def is_quit():
    print(" **********   按任意键结束  **********")
    msvcrt.getch()


def main():
    get_data(position)


if __name__ == '__main__':
    position = input("***** 请输入职位：*****\n")
    print(" **********  以下是相关职位信息   **********")
    main()
    is_quit()