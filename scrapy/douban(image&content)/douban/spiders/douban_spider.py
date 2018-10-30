import scrapy

from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/编程']

    #def start_requests(self):
     #   return scrapy.Request(self.start_urls[0],callback=self.parse)

    def parse(self, response):
        book_list = response.xpath("//div[@class='article']/div[@id='subject_list']/ul/li")
        for i_item in book_list:
            douban_item = DoubanItem()
            book_name = i_item.xpath("normalize-space(.//div[@class='info']/h2/a/text())").extract_first()
            douban_item['book_name'] = "".join(book_name)
            author = i_item.xpath(".//div[@class='pub']/text()").extract_first()
            # douban_item['author'] = i_item.xpath(".//div[@class='pub']/text()").extract_first()
            douban_item['author'] = "".join(author).replace('\n','').split('/')[1]
            douban_item['star'] = i_item.xpath(".//span[@class='rating_nums']/text()").extract_first()
            douban_item['image_urls'] = i_item.xpath(".//div[@class='pic']/a/img/@src").extract()
            yield douban_item
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        print(next_link)
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://book.douban.com"+next_link, callback=self.parse)


        # for i in range(1,11):
        #     next_link = 'https://book.douban.com/tag/编程?start={}'.format(i*20)
        #     print(next_link)
        #     yield scrapy.Request(next_link,callback=self.parse)
