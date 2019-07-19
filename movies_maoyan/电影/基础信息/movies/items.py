# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    '''
    影院基本信息
    '''
    # movie_name = scrapy.Field()
    # ellipsis = scrapy.Field()
    # time = scrapy.Field()
    # vision = scrapy.Field()

    '''
    影院信息
    '''
    cinema_name = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    city = scrapy.Field()


