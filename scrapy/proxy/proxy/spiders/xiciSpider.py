# -*- coding: utf-8 -*-
import scrapy


class XicispiderSpider(scrapy.Spider):
    name = 'xiciSpider'
    # allowed_domains = ['www.xicidaili.com']
    # start_urls = ['http://www.xicidaili.com/']

    start_list = []
    for i in range(1, 10):
        url = 'http://www.xicidaili.com/nn/%s' % str(i)
    start_list.append(url)
    start_urls = start_list

    def start_requests(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36"
        headers = {'User-Agent': user_agent}
        for url in self.start_list:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        ip_list = response.xpath('//*[@id="ip_list"]//tr')
        with open('proxy_data2.txt', "a") as wd:
            for index, port in enumerate(ip_list):
                if index != 0:
                    ip_address = port.xpath('td[2]/text()').extract_first() + ":" + port.xpath('td[3]/text()').extract_first()
                    print(ip_address)
                    wd.write(ip_address + "\n")

