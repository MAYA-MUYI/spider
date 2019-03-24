# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class TiebaUserSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TiebaUserDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        request.cookie = {
            'TIEBA_USERTYPE=5e2d54c3743bfa394dd403ae; bdshare_firstime=1504967610363; FP_LASTTIME=1510495331224; BAIDUID=D40E33930F8AA455DFD43F5BB642B2CF:FG=1; PSTM=1535337133; BIDUPSID=5EB6976EB15A5D70F1DACF6196643EFE; MCITY=-%3A; __cfduid=dde06645292e63db3dd473db8a82193e41551972209; TIEBAUID=898e9f1e66a1c5044701e20b; BDUSS=xjZkNPZHNWajhGN2stQm9HUGZVTk5tQUNDVHpjMWFJaGNvM2ZaMlFoQmdoN0ZjQVFBQUFBJCQAAAAAAAAAAAEAAAD9w04xxOPO0tPAuuO1xMrE0dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGD6iVxg-olcR2; STOKEN=32d53c49cc4863d9f7a3f5de770ff47203b2a560a0de9d5acc09185c90df0bab; showCardBeforeSign=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1552608845,1552712273,1552736353,1552790937; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; BL_D_PROV=; BL_T_PROV=; LONGID=827245565; Cuid=D40E33930F8AA455DFD43F5BB642B2CF%3AFG%3D1; Appid=tieba; Appkey=appkey; DeviceType=20; Extension-Version=2.2; LCS-Header-Version=1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1552792428'
        }
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
