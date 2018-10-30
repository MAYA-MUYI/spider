# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):

    # two items: url and name of image
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
