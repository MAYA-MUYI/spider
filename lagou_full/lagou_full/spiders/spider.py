# -*- coding: utf-8 -*-
import scrapy
from lagou_full.items import LagouFullItem
import re



class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    def parse(self, response):
        #对8个主大类分类
        main_cates = response.xpath('//div[@class="menu_sub dn"]')
        for main_cate in main_cates:
            cate_name = main_cate.xpath('./dl/dt/span/text()').extract_first()
            cate_url = main_cate.xpath('./dl/dd/a/@href').extract_first()
            meta = {'cate_name': cate_name}
            yield scrapy.Request(url=cate_url, callback=self.parse_job_list, dont_filter=True, meta=meta)

    def parse_job_list(self, response):
        positions = response.xpath('//ul[@class="item_con_list"]/li')
        for position in positions:
            position_url = position.xpath('.//a[@class="position_link"]/@href').extract_first()
            yield scrapy.Request(url=position_url, callback=self.parse_job_detail, meta=response.meta)


        # 提取出下一页的url
        next_page_url = response.xpath(
            '//div[@class="pager_container"]/a[contains(text(), "下一页")]/@href').extract_first()

        if next_page_url != "javascript:;":
            # 解析下一页, 指定dont_filter=True, 就可以实现增量爬虫了.
            yield scrapy.Request(url=next_page_url, dont_filter=True, callback=self.parse_job_list, meta=response.meta)



    def parse_job_detail(self, response):
        job_name = response.xpath('//div[@class="job-name"]/span[@class="name"]/text()').extract_first()

        # 工作简介
        salary_range = response.xpath('//dd[@class="job_request"]/p/span[1]/text()').extract_first().replace('/',
                                                                                                             '').strip()
        working_city = response.xpath('//dd[@class="job_request"]/p/span[2]/text()').extract_first().replace('/',
                                                                                                             '').strip()
        experience_required = response.xpath('//dd[@class="job_request"]/p/span[3]/text()').extract_first().replace('/',
                                                                                                                    '').strip()
        education_required = response.xpath('//dd[@class="job_request"]/p/span[4]/text()').extract_first().replace('/',
                                                                                                                   '').strip()
        job_type = response.xpath('//dd[@class="job_request"]/p/span[5]/text()').extract_first().replace('/',
                                                                                                         '').strip()
        position_label = ','.join(response.xpath('//ul[contains(@class, "position-label")]/li/text()').extract())
        publish_time = response.xpath('//p[@class="publish_time"]/text()').extract_first().split('\xa0')[0]

        # 工作详情
        job_advantage = response.xpath('//dd[@class="job-advantage"]/p/text()').extract_first()
        job_detail = '\n'.join(response.xpath('//div[@class="job-detail"]/p//text()').extract()).replace('\xa0', '')
        # job_detail = response.xpath('normalize-space(//div[@class="job-detail"]/p//text())').extract()
        # 工作详细地址
        working_city_temp = response.xpath('//div[@class="work_addr"]/a[1]/text()').extract_first()
        working_district_temp = response.xpath('//div[@class="work_addr"]/a[2]/text()').extract_first()
        working_address_temp = ''.join(response.xpath('//div[@class="work_addr"]/text()').extract()).replace('-',
                                                                                                             '').strip()
        working_address = "{}-{}-{}".format(working_city_temp, working_district_temp, working_address_temp)

        # 公司信息

        company_lagou_url = response.xpath('//dl[@class="job_company"]/dt/a/@href').extract_first()

        company_name = response.xpath('//dl[@class="job_company"]/dt/a/div/h2/em/text()').extract_first().strip()
        #公司领域
        field_pattern = re.compile('<i class="icon-glyph-fourSquare"></i>(.*?)<span', re.S)
        company_field = re.findall(field_pattern, response.body.decode('utf-8'))[0].strip()
        #company_field = ''.join(response.xpath('//ul[@class="c_feature"]/li[@class="icon-glyph-fourSquare"]/text()').extract()).strip()

        #融资情况
        financing_pattern = re.compile('<i class="icon-glyph-trend"></i>(.*?)<span', re.S)
        financing_status = re.findall(financing_pattern, response.body.decode('utf-8'))[0].strip()
        # financing_status = ''.join(response.xpath('//ul[@class="c_feature"]/li[@class="icon-glyph-trend"]/text()').extract()).strip()

        #公司成员数量
        size_pattern = re.compile('<i class="icon-glyph-figure"></i>(.*?)<span', re.S)
        company_size = re.findall(size_pattern, response.body.decode('utf-8'))[0].strip()
        # company_size = ''.join(response.xpath('//ul[@class="c_feature"]/li[@class="icon-glyph-figure"]/text()').extract()).strip()

        #公司主页
        url_pattern = re.compile('<i class="icon-glyph-home"></i>.*?<a.*?>(.*?)</a>.*?<span', re.S)
        company_url = re.findall(url_pattern, response.body.decode('utf-8'))[0].strip()
        # company_url = ''.join(response.xpath('//ul[@class="c_feature"]/li[@class="icon-glyph-home"]//a/@href').extract()).strip()

        # print("*" * 50)
        # print(job_name, salary_range, working_city, experience_required, education_required, job_type, position_label,
        #       publish_time, sep='\n')
        # print("*" * 50)
        # print(job_advantage, job_detail, working_address, sep='\n')
        # print("*" * 50)
        # print(company_lagou_url, company_name, company_field, financing_status, company_size, company_url, sep='\n')
        # print("*" * 50)

        item = LagouFullItem(
            cate_name=response.meta.get("cate_name"),
            job_name=job_name,
            salary_range=salary_range,
            working_city=working_city,
            experience_required=experience_required,
            education_required=education_required,
            job_type=job_type,
            position_label=position_label,
            publish_time=publish_time,
            job_advantage=job_advantage,
            job_detail=job_detail,
            working_address=working_address,
            company_lagou_url=company_lagou_url,
            company_name=company_name,
            company_field=company_field,
            financing_status=financing_status,
            company_size=company_size,
            company_url=company_url
        )

        yield item
