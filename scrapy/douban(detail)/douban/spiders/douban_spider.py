import scrapy
from douban.items import DoubanItem
import re


class DoubanSpiderSpider(scrapy.Spider):

    name = 'douban_spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/编程']

    def parse(self, response):
        href_list = response.xpath("//*[@id='subject_list']/ul/li/div[@class='info']/h2/a/@href").extract()
        for list in href_list:
            yield scrapy.Request(url=list, callback=self.parse_tag)
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://book.douban.com" + next_link, callback=self.parse)

    def parse_tag(self, response):
        douban_item = DoubanItem()
        douban_item['book_name'] = response.xpath("//*[@id='wrapper']/h1/span/text()").extract_first()
        douban_item['star'] = response.xpath("//div[@class='rating_self clearfix']/strong/text()").extract_first()
        info = response.xpath("//div[@id='info']/text()").extract()
        douban_item['price'] = re.search(r'\d{2}\.\d{2}', str(info)).group(0)
        douban_item['cod'] = re.search(r'\d{13}', str(info)).group(0)
        content= response.xpath("normalize-space(//div[@id='link-report']//div[@class='intro']/p/text())").extract_first()
        douban_item['content'] = "".join(content)
        author = response.xpath("normalize-space(//*[@id='content']/div/div[1]/div[3]/div[2]/div/div//p/text())").extract_first()
        douban_item['author'] = "".join(author)
        # douban_item['content_sum'] = response.xpath("//div[@id='link-report']//div[@class='intro']/p/text()").extract()
        # douban_item['author_sum'] = response.xpath("//*[@id='content']/div/div[1]/div[3]/div[2]/div/div//p/text()").extract()
        yield douban_item