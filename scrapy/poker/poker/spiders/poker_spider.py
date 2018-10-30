# -*- coding: utf-8 -*-
import scrapy
from poker.items import PokerItem
import time

class PokerSpiderSpider(scrapy.Spider):
    name = 'poker_spider'
    allowed_domains = ['thepokerlogic.com']
    # start_urls = ['http://thepokerlogic.com/glossary?']
    start_urls = ['http://thepokerlogic.com/glossary']

    def parse(self, response):

        href_list = response.xpath('//div[@class="content_list"]/div/a/@href').extract()
        for list in href_list:
            yield scrapy.Request(url="http://thepokerlogic.com"+list, callback=self.parse_tag)

    def parse_tag(self, response):
            item = PokerItem()
            item['title'] = response.xpath('//div[@class="glossary-detail"]/h2/text()').extract_first()
            item['describe_title'] = response.xpath('//div[@class="detail-describe"]/h3/text()').extract_first()
            item['describe_content'] = response.xpath('normalize-space(//div[@class="describe-content"]/p/text())').extract_first()
            item['illustrate_title'] = response.xpath('//div[@class="detail-illustrate"]/h4/text()').extract_first()
            item['illustrate_content'] = response.xpath('//div[@class="illustrate-content"]/p/text()').extract_first()
            item['relevant_title'] = response.xpath('//div[@class="detail-relevant"]/h4/text()').extract_first()
            relevant_content_a = response.xpath('//div[@class="relevant-content"]/a/text()').extract_first()
            relevant_content_p = response.xpath('//div[@class="relevant-content"]/p/text()').extract_first()
            if not relevant_content_a:
                item['relevant_content'] = relevant_content_p
            else:
                item['relevant_content'] = relevant_content_a

            item['study_title'] = response.xpath('//div[@class="detail-study"]/h4/text()').extract_first()
            study_content_a = response.xpath('//div[@class="study-content"]/a/text()').extract()
            study_content_p = response.xpath('//div[@class="study-content"]/p/text()').extract()
            if not study_content_a:
                item['study_content'] = study_content_p
            else:
                item['study_content'] = study_content_a
            url_title = response.xpath('//div[@class="glossary-detail-content"]//a/text()').extract()
            if url_title == '无' or url_title is None:
                url_link = ''
            else:
                url_link = response.xpath('//div[@class="glossary-detail-content"]//a/@href').extract()
            item['url'] = dict(zip(url_title, url_link))

            return item