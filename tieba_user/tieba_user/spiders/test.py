# #!/usr/bin/env python
# # -*- coding：utf-8 -*-
from lxml import  etree
import requests
import re
#
#
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'cookie': 'TIEBA_USERTYPE=5e2d54c3743bfa394dd403ae; bdshare_firstime=1504967610363; FP_LASTTIME=1510495331224; BAIDUID=D40E33930F8AA455DFD43F5BB642B2CF:FG=1; PSTM=1535337133; BIDUPSID=5EB6976EB15A5D70F1DACF6196643EFE; MCITY=-%3A; __cfduid=dde06645292e63db3dd473db8a82193e41551972209; TIEBAUID=898e9f1e66a1c5044701e20b; BDUSS=xjZkNPZHNWajhGN2stQm9HUGZVTk5tQUNDVHpjMWFJaGNvM2ZaMlFoQmdoN0ZjQVFBQUFBJCQAAAAAAAAAAAEAAAD9w04xxOPO0tPAuuO1xMrE0dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGD6iVxg-olcR2; STOKEN=32d53c49cc4863d9f7a3f5de770ff47203b2a560a0de9d5acc09185c90df0bab; showCardBeforeSign=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1552608845,1552712273,1552736353,1552790937; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; BL_D_PROV=; BL_T_PROV=; LONGID=827245565; Cuid=D40E33930F8AA455DFD43F5BB642B2CF%3AFG%3D1; Appid=tieba; Appkey=appkey; DeviceType=20; Extension-Version=2.2; LCS-Header-Version=1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1552792428',
    'Upgrade-Insecure-Requests': '1'
}
if __name__ == '__main__':
    url = 'http://tieba.baidu.com/i/i/fans?u=fdc3e4bda0e68891e6b0b8e68192e79a84e8aa93e8a8804e31?t=1447344722'
    url1  = 'http://tieba.baidu.com/home/main?un=%E6%A2%A6%E9%AD%87%E7%A9%BA%E6%B4%9Eio&id=d1a4e6a2a6e9ad87e7a9bae6b49e696fa12f&fr=home'

    r = requests.get(url1, headers=headers)
    text = r.text
    html = etree.HTML(text)
    id = html.xpath('//*[@id="ihome_nav_wrap"]/ul/li[1]/div/p/a/@href')
    d = id[0].split('&')[-1][3:]

    t = html.xpath('//h1[contains(text(),"关注的人")]/span[@class="concern_num"]/a/@href')
    t = t[0].split('?')[2][:-8]

    new_url = "http://tieba.baidu.com/i/i/concern?u={0}".format(d)
    print(new_url)

    a = requests.get(new_url, headers=headers).text
    h = etree.HTML(a)
    a1 = h.xpath('//span[@class="name"]/a//text()')
    print(a1)
    # print(a.text)
