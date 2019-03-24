# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouFullItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #分类名称
    cate_name = scrapy.Field()
    #职位名称
    job_name = scrapy.Field()
    #工资范围
    salary_range = scrapy.Field()
    #工作城市
    working_city = scrapy.Field()
    #经验要求
    experience_required = scrapy.Field()
    #教育要求
    education_required = scrapy.Field()
    #工作类型
    job_type = scrapy.Field()
    #职位标签
    position_label = scrapy.Field()
    #更新时间
    publish_time = scrapy.Field()
    #职位优势
    job_advantage = scrapy.Field()
    #职位详情
    job_detail = scrapy.Field()
    #工作地址
    working_address = scrapy.Field()
    #公司招聘链接
    company_lagou_url = scrapy.Field()
    #公司名字
    company_name = scrapy.Field()
    #公司领域
    company_field = scrapy.Field()
    #融资情况
    financing_status = scrapy.Field()
    #公司成员数量
    company_size = scrapy.Field()
    #公司职位链接
    company_url = scrapy.Field()

    pass
