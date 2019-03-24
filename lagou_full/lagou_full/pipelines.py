# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.exceptions import DropItem
from scrapy import log
import pymysql


class LagouFullPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='lagou')
        cur = conn.cursor()
        sql = """insert into positions(cate_name, job_name, salary_range, working_city, experience_required, education_required,
              job_type,position_label,publish_time, job_advantage,  job_detail, working_address, company_lagou_url,
              company_name, company_field, financing_status,company_size, company_url ) 
              values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cate_name = item['cate_name']
        job_name = item['job_name']
        salary_range = item['salary_range']
        working_city = item['working_city']
        experience_required = item['experience_required']
        education_required = item['education_required']
        job_type = item['job_type']
        position_label = item['position_label']
        publish_time = item['publish_time']
        job_advantage = item['job_advantage']
        job_detail = item['job_detail']
        working_address = item['working_address']
        company_lagou_url = item['company_lagou_url']
        company_name = item['company_name']
        company_field = item['company_field']
        financing_status = item['financing_status']
        company_size = item['company_size']
        company_url = item['company_url']
        values = (cate_name, job_name, salary_range, working_city, experience_required, education_required, job_type,
                  position_label, publish_time, job_advantage,  job_detail, working_address, company_lagou_url,
                  company_name, company_field, financing_status, company_size, company_url)
        cur.execute(sql, values)
        conn.commit()
        return item
