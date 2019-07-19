# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    movie_name = scrapy.Field()
    duration = scrapy.Field()
    introduction = scrapy.Field()
    time = scrapy.Field()
    vision = scrapy.Field()
    ellipsis = scrapy.Field()
