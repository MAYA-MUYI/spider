#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: test.py
@time: 2019/3/15 11:37
@desc:
'''

import requests
from lxml import etree
from requests import RequestException
import hashlib


class LagouSpider:

    def __init__(self):
        self.getHtmlHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Host': 'www.lagou.com',
            'cookie': 'user_trace_token=20181205153237-2fb5c5de-ddba-45ae-a4e5-1d3f994363da; _ga=GA1.2.1973907981.1543995170; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221677d489b4c51b-01ad0f1ff9cf7e-7d113749-1049088-1677d489b4e157%22%2C%22%24device_id%22%3A%221677d489b4c51b-01ad0f1ff9cf7e-7d113749-1049088-1677d489b4e157%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LGUID=20181205153247-f6746e6e-f85f-11e8-8ce2-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAGGABCBEC1D512B5ADA6A74D03F8164FE28C737; _gid=GA1.2.876365574.1552956398; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552804970,1552810275,1552829496,1552956398; LGSID=20190319084635-724708a3-49e0-11e9-a330-5254005c3644; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; BL_D_PROV=; BL_T_PROV=; TG-TRACK-CODE=index_navigation; _gat=1; _putrc=D253F09634921DCE123F89F2B170EADC; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73051; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=e286d9ac1ea09ca9d4fd281b28b7b778328ec85baeb7940884f05d6125f7d04d; SEARCH_ID=4073b2204b6347d6977a59e980553647; LGRID=20190319093733-912e1a6a-49e7-11e9-aaa2-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552959457',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

    def getHtml(self, url):
        try:
            response = requests.get(url=url, headers=self.getHtmlHeaders)
            # print(response.status_code)
            # if response.status_code == 200:
                # print(response.text)
            return response.text
        except RequestException:
            print('请求Html错误:')

    def parseHtml(self, response):
        html = etree.HTML(response)
        job_urls = html.xpath('//div[@class="menu_sub dn"]/dl/dd/a/@href')
        job_names = html.xpath('//div[@class="menu_sub dn"]/dl/dd/a/text()')
        with open('jobs_list.txt', 'w') as f:
            for job in job_urls:
                f.write(job + '\n')




    def run(self, url):
        self.parseHtml(self.getHtml(url))









if __name__ == '__main__':
    url = 'https://www.lagou.com/'
    LagouSpider().run(url)

