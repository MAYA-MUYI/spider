# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import DropItem
import pymysql
from scrapy import log


class MaoyanPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='api')
        cur = conn.cursor()
        '''
         movie_name = scrapy.Field()
    duration = scrapy.Field()
    introduction = scrapy.Field()
    time = scrapy.Field()
    vision = scrapy.Field()
    ellipsis = scrapy.Field()
        '''
        sql = "insert into movie_detail(movie_name, duration, ellipsis, introduction, time, vision) values (%s, %s, %s, %s, %s, %s)"
        movie_name = item['movie_name']
        ellipsis = item['ellipsis']
        time = item['time']
        vision = item['vision']
        duration = item['duration']
        introduction = item['introduction']
        values = (movie_name, duration, ellipsis, introduction, time, vision)
        cur.execute(sql, values)
        conn.commit()
        return item