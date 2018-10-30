# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    #allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/编程']

    def parse(self, response):
        # item = DoubanItem()
        # book_list = response.xpath("//div[@class='article']//table")
        # for i_item in book_list:
        #     item['image_urls'] = i_item.xpath(".//tr/td/a/img/@src").extract()
        #     # print(item['image_paths'])
        #     yield item

        book_list = response.xpath("//div[@class='article']/div[@id='subject_list']/ul/li")
        for i_item in book_list:
            douban_item = DoubanItem()
            douban_item['image_urls'] = i_item.xpath(".//div[@class='pic']/a/img/@src").extract()
            yield douban_item
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://book.douban.com" + next_link, callback=self.parse)