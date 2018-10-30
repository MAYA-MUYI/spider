# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
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

        # try:
        #     conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='douban')
        #     cur = conn.cursor()
        #     sql = "insert into book_home(image_path) values (%s)"
        #     i = item['image_paths']
        #     values = (i)
        #     cur.execute(sql, values)
        #     print(sql)
        # except Exception:
        #     print("Erro")
        # finally:
        #     conn.commit()
        # return item

        conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='douban')
        cur = conn.cursor()
        sql = "insert into book_home(book_name, author, star, image_path) values (%s, %s, %s, %s)"
        book_name = item['book_name']
        author = item['author']
        star = item['star']
        image_path = item['image_paths']
        values = (book_name, author, star, image_path)
        cur.execute(sql, values)
        # except Exception:
        # print("Error")
        # finally:
        conn.commit()
        return item

# class DoubanPipeline(object):
#     def process_item(self, item, spider):
#         conn = pymysql.connect(host="localhost", user="root", password="299521", port=3306, db='douban2')
#         cur = conn.cursor()
#         sql = "insert into book(book_name, author, star) values (%s, %s, %s)"
#         author = item['author']
#         book_name =item['book_name']
#         star = item['star']
#         # author = item['author'].extract()
#         # talk = item['talk'].extract()
#         # score = item['score'].extract()
#         # values = (bname, score, author, talk )
#         values = (book_name, author, star)
#         cur.execute(sql, values)
#         conn.commit()
#         return item