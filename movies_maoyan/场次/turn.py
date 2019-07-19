#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: turn.py
@time: 2019/6/2 16:10
@desc:
'''
import requests
import re
import json
from lxml import etree

'''
    movie_session = [不同电影的场次数据
        {movie_name: ...
         result:[每一天的场次数据
            {
                date: ...
                session_result:[当天的场次数据
                    {},
                    {}....
                ]        
            }
         ]
        }
    ]：每部电影的数据
'''

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Referer": "https://maoyan.com/xseats/201906020127664?movieId=246061&cinemaId=17372",
    "Host": "maoyan.com",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
}
movie_result = []

def getCinemas(urls):
    cinemas = []
    for url in urls:
        html = etree.HTML(getHtml(url))
        cinemas.extend(html.xpath('//div[@class="cinema-info"]/a/@href'))
    return cinemas


def getUrls(urls):
    url_list = []
    cinemas = getCinemas(urls)
    for cinema in cinemas:
        cinema_url = "http://maoyan.com" + cinema
        url_list.append(cinema_url)
    return url_list


def getHtml(url):
    return requests.get(url, headers=headers).text


#给出当天的xpath对象获取对应日期的场次数据
def getToday(today, time_list, num):
    result = []
    session_result = []
    session_list = today.xpath('.//table/tbody/tr')
    # 当天每个场次
    for session in session_list:
        begin_time = session.xpath('.//span[@class="begin-time"]/text()')[0]
        end_time = session.xpath('.//span[@class="end-time"]/text()')[0]
        lang = session.xpath('.//span[@class="lang"]/text()')[0]
        hall = session.xpath('.//span[@class="hall"]/text()')[0]
        session_result.append({
            "date": re.findall('\d+', time_list[num])[0] + '-' + re.findall('\d+', time_list[num])[1],
            "begin_time": begin_time,
            "end_time": end_time,
            "lang": lang,
            "hall": hall
        })
    result.append({
        "date": re.findall('\d+', time_list[num])[0] + '-' + re.findall('\d+', time_list[num])[1],
        "session_result": session_result
    })
    return result


def parse_tag(html, days):
    movie_session = []
    movie_name = html.xpath('//h3[@class="movie-name"]/text()')[0]
    time_list = html.xpath('//div[@class="show-list active"]//div[@class="show-date"]/span/text()')[1:]
    for day in days:
        result = getToday(day, time_list)
        movie_session.append({
            "movie_name": movie_name,
            "result": result
        })
    return movie_session

def test(text):
    movies_session = []mo'v'
    result = []
    tmp_result = []
    html = etree.HTML(text)
    cinema_name = html.xpath('//h3[@class="name text-ellipsis"]/text()')[0]
    movies_list = html.xpath('//div[contains(@class, "show-list")]')

    #每一部电影数据
    for movie in movies_list:
        tmp_result.append(get_MovieData(movie)[0])
    with open('files/' + cinema_name + '.json', 'a+', encoding='utf-8') as f:
        f.write(json.dumps(tmp_result, ensure_ascii=False, indent=2))


def get_MovieData(movie):
    movie_session = []
    result = []
    movie_name = movie.xpath('.//h3[@class="movie-name"]/text()')[0]
    if movie.xpath('.//span[@class="score sc"]/text()'):
        star = movie.xpath('.//span[@class="score sc"]/text()')[0]
    else:
        star = '暂无评分'

    time_list = movie.xpath('.//div[@class="show-date"]/span/text()')[1:]
    #所有场次天数
    days = movie.xpath('.//div[contains(@class, "plist-container")]')
    for day in days:
        result.append(getToday(day, time_list, days.index(day)))
        # print(movie_result)
    movie_session.append({
        "movie_name": movie_name,
        "star": star,
        "result": result
    })

    return movie_session


def parse(text):
    html = etree.HTML(text)
    movie_session = []
    result = []
    session_result = []

    list = html.xpath('//div[@class="show-list active"]')
    movie_name = html.xpath('//h3[@class="movie-name"]/text()')[0]
    star = html.xpath('//span[@class="score sc"]/text()')[0]
    time_list = html.xpath('//div[@class="show-list active"]//div[@class="show-date"]/span/text()')[1:]#6月2， 6月3
    days = html.xpath('//div[@data-index="0"]//div[contains(@class, "plist-container")]')
    for day in days:
        print(json.dumps(getToday(day, time_list, days.index(day)), ensure_ascii=False))


if __name__ == '__main__':
    urls = [
        "https://maoyan.com/cinemas?districtId=3799",
        "https://maoyan.com/cinemas?districtId=3798",
        "https://maoyan.com/cinemas?areaId=-1&districtId=3802",
    ]
    cinemas = getUrls(urls)
    for url in cinemas:
        test(requests.get(url, headers=headers).text)
