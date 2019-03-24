# #!/usr/bin/env python
# # -*- coding：utf-8 -*-
# '''
# @author: maya
# @contact: 1278077260@qq.com
# @software: Pycharm
# @file: test.py
# @time: 2019/3/23 16:01
# @desc:
# '''
#
# import requests
# import re
# from lxml import  etree
#
# if __name__ == '__main__':
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
#     }
#     url = 'https://www.lagou.com/jobs/5727841.html'
#     text = requests.get(url, headers=headers).text
#     field_pattern = re.compile('<i class="icon-glyph-fourSquare"></i>(.*?)<span', re.S)
#     financing_pattern = re.compile('<i class="icon-glyph-trend"></i>(.*?)<span', re.S)
#     size_pattern = re.compile('<i class="icon-glyph-figure"></i>(.*?)<span', re.S)
#     url_pattern = re.compile('<i class="icon-glyph-home"></i>.*?<a.*?>(.*?)</a>.*?<span', re.S)
#
#     area = re.findall(field_pattern, text)[0].strip()
#     fin_stats = re.findall(financing_pattern, text)[0].strip()
#     size = re.findall(size_pattern, text)[0].strip()
#     company_url = re.findall(url_pattern, text)[0].strip()
#
#
#     print("area:", area)
#     print("fin_stats:", fin_stats)
#     print("size:", size)
#     print("url:", company_url)