# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import DropItem
import pymysql
from scrapy import log


class DoubanPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='douban')
        cur = conn.cursor()
        sql = "insert into book_detail(book_name, star, price, cod, content, author) values (%s, %s, %s, %s, %s, %s)"
        book_name = item['book_name']
        star = item['star']
        price = item['price']
        cod = item['cod']
        content = item['content']
        author = item['author']
        values = (book_name, star, price, cod, content, author)
        cur.execute(sql, values)
        conn.commit()
        return item
