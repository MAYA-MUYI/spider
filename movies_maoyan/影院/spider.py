# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import os
import random
from maoyan.items import MaoyanItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/cinemas?areaId=-1&districtId=3798']
    price_range = [24, 28, 29, 30, 34, 40, 47]

    def parse(self, response):
        cinema_list = response.xpath('//div[@class="cinema-cell"]/div[@class="cinema-info"]/a/@href').extract()
        for cinema in cinema_list:
            yield scrapy.Request("https://maoyan.com" + cinema, callback=self.parse_tag)


    def parse_tag(self, respnse):
        item = MaoyanItem()
        item['cinema_name'] = respnse.xpath('//h3[@class="name text-ellipsis"]/text()').extract_first()
        item['price'] = random.choice(self.price_range)
        item['address'] = respnse.xpath('//div[@class="address text-ellipsis"]/text()').extract_first()
        item['city'] = respnse.xpath('normalize-space(///div[@class="city-name"]/text())').extract_first()
        yield item

