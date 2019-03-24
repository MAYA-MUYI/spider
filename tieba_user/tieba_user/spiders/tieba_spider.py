# -*- coding: utf-8 -*-
import scrapy
from tieba_user.items import TiebaUserItem


class TiebaSpiderSpider(scrapy.Spider):
    name = 'tieba_spider'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=python&pn=1']


    def parse(self, response):
        href_list = response.xpath('//span[starts-with(@class,"member")]/div/a/@href').extract()
        for href in href_list:
            yield scrapy.Request(url="http://tieba.baidu.com" + href, callback=self.parse_tag)
        next_link = response.xpath('//div[@class="tbui_pagination tbui_pagination_left"]/ul/li/a[@class="next_page"]/@href').extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request(url="http://tieba.baidu.com" + next_link, callback=self.parse)

    def parse_tag(self, response):
        item = TiebaUserItem()
        item['nickname'] = response.xpath('//div[@class="userinfo_title"]/span/text()').extract_first()
        if response.xpath('//div[@class="userinfo_userdata"]/span[@class="user_name"]/text()').extract_first():
            item['username'] = response.xpath('//div[@class="userinfo_userdata"]/span[@class="user_name"]/text()').extract_first()[4:]
        item['attention'] = response.xpath('//div[@class="ihome_forum_group ihome_section clearfix"]/div[@class="clearfix u-f-wrap"]/a//text()').extract()
        if response.xpath('//span[@class="user_name"]//span[2]/text()'):
            item['age'] = response.xpath('//span[@class="user_name"]//span[2]/text()').extract_first()[3:]

        if response.xpath('//span[@class="user_name"]//span[4]/text()'):
            item['post_number'] = response.xpath('//span[@class="user_name"]//span[4]/text()').extract_first()[3:]

        return item




