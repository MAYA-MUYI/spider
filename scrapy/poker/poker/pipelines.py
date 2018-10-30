# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json

class PokerPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='poker_new')
        cur = conn.cursor()
        sql = "insert into poker_info(title, describe_title, describe_content, illustrate_title, illustrate_content, relevant_title, relevant_content, study_title, study_content, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        title = item['title']
        describe_title = item['describe_title']
        describe_content = item['describe_content']
        illustrate_title = item['illustrate_title']
        illustrate_content = item['illustrate_content']
        relevant_title = item['relevant_title']
        relevant_content = item['relevant_content']
        study_title = item['study_title']
        study_content = item['study_content']
        url = json.dumps(item['url'], ensure_ascii=False)
        values = (title, describe_title, describe_content, illustrate_title, illustrate_content, relevant_title, relevant_content,study_title, study_content, url)
        cur.execute(sql, values)
        conn.commit()
        return item
