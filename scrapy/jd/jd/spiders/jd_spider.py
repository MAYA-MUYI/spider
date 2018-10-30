# -*- coding: utf-8 -*-
import scrapy
from jd.items import JingdongItem


class JdSpiderSpider(scrapy.Spider):
    name = 'jd_spider'
    allowed_domains = ['www.jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=ipad&enc=utf-8&page={}'.format(str(i) for i in range(1,101 ))]


    def parse(self, response):
        lists = response.xpath('//li[@class="gl-item"]/div')
        for list in lists:
            item = JingdongItem()
            item['name'] = list.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()').extract_first()
            item['shop'] = list.xpath('.//div[@class="p-shop"]/span/a/text()').extract_first()
            item['icon'] = list.xpath('.//div[@class="p-icons"]/i[@class="goods-icons J-picon-tips J-picon-fix"]/text()').extract_first()
            item['price'] = list.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            yield item




