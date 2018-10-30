# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import pymysql





class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        try:
            conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='douban')
            cur = conn.cursor()
            sql = "insert into paths(images_paths) values (%s)"
            i = item['image_paths']
            values = (i)
            cur.execute(sql, values)
            print(sql)
        except Exception:
            print("Erro")
        finally:
            conn.commit()
        return item






