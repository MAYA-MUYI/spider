# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import os
from maoyan.items import MaoyanItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com']
    date_reg_exp = re.compile('\d{4}[-/]\d{2}[-/]\d{2}')

    def pic_format(self, src):
        (filename, extension) = os.path.splitext(src)
        if extension == '.jpg' or extension == '.png':
            pass
        else:
            src = src.split(extension[:3])[0] + extension[:3]
        return src

    def download(self, name, src):
        for data in src.items():
            with open('pic/' + name + '_' + data[0], 'wb') as f:
                f.write(requests.get(data[1]).content)

    def parse(self, response):
        movie_list = response.xpath('//dd//div[@class="movie-item"]/a/@href').extract()
        for url in movie_list:
            yield scrapy.Request("https://maoyan.com" + url, callback=self.parse_tag)

    def parse_tag(self, response):
        item = MaoyanItem()
        item['movie_name'] = response.xpath('//h3[@class="name"]/text()').extract_first()
        item['ellipsis'] = response.xpath('//div[@class="ename ellipsis"]/text()').extract()
        time_str = ''.join(response.xpath('//li[@class="ellipsis"]//text()').extract())
        item['time'] = self.date_reg_exp.findall(time_str)[0]
        if response.xpath('//i[@class="imax3d"]'):
            item['vision'] = "3DIMAX"
        elif response.xpath('//i[@class="m3d"]'):
            item['vision'] = "3D"
        else:
            item['vision'] = ""
        yield item




