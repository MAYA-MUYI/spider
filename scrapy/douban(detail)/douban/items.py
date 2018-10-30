# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    book_name = scrapy.Field()
    star = scrapy.Field()
    price = scrapy.Field()
    cod = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
