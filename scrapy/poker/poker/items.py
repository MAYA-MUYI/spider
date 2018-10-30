# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PokerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    describe_title = scrapy.Field()
    describe_content = scrapy.Field()
    illustrate_title = scrapy.Field()
    illustrate_content = scrapy.Field()
    relevant_title = scrapy.Field()
    relevant_content = scrapy.Field()
    study_title = scrapy.Field()
    study_content = scrapy.Field()
    url = scrapy.Field()



