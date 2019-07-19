# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import time
import re
import os
import logging
import requests
import json
from twisted.internet import defer
from twisted.internet.defer import DeferredLock
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError, ConnectionDone
logger = logging.getLogger(__name__)



# 从2个不同的api中获取代理
def get_random_ip():
    mogu_api = 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=04756895ae5b498bb9b985798e990b9f&count=1&expiryDate=0&format=1&newLine=2'

    # '{"code":"3001","msg":"提取频繁请按照规定频率提取!"}'
    # '{"code":"0","msg":[{"port":"35379","ip":"117.60.2.113"}]}'

    xdaili_api = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=9b3446e17b004293976e09a081022d73&orderno=YZ20188178415lSPZWO&returnType=2&count=1'

    # '{"ERRORCODE":"10055","RESULT":"提取太频繁,请按规定频率提取!"}'
    # '{"ERRORCODE":"0","RESULT":[{"port":"48448","ip":"115.203.196.254"}]}'

    api_list = [mogu_api, xdaili_api]
    # 打乱api_list的顺序, 以免列表中第1个代理使用的次数过多
    random.shuffle(api_list)

    for api in api_list:
        response = requests.get(api)
        js_str = json.loads(response.text)
        # 如果正确提取到了ip地址
        if js_str.get('code') == '0' or js_str.get('ERRORCODE') == '0':
            # 从中取出ip
            for i, j in js_str.items():
                if j != '0':
                    # proxies = {
                    #     "http": "http://{}:{}".format(j[0].get('ip'), j[0].get('port')),
                    #     "https": "https://{}:{}".format(j[0].get('ip'), j[0].get('port'))
                    #     }
                    proxies = "https://{}:{}".format(j[0].get('ip'), j[0].get('port'))
                    logger.info("从 {} 获取了一个代理 {}".format(re.split(r'.c', api)[0], proxies))
                    # print("从{}获取了一个代理{}".format(re.split(r'.c', api)[0], proxies))
                    return proxies
            break
        else:
            # print("提取太频繁, 等待中...")
            logger.info("api {} 提取太频繁, 等待中".format(api))
            time.sleep(random.randint(5, 10))


def get_random_ua():
    # 从本地读取useragent并随机选择
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file = os.path.join(project_path, "fake_useragent.json")
    with open(json_file, "r") as f:
        ua_list = json.load(f)
        user_agent = random.choice(ua_list)
        # print("当前的user-agent是:%s" % user_agent)
        logger.info("随机获取了一个ua {}".format(user_agent))
        return user_agent


class RandomUAIPDownloaderMiddleware(object):
    def __init__(self, ua=''):
        # 初始时从api获取代理地址, 并给所有代理都设置为这个代理
        super(RandomUAIPDownloaderMiddleware, self).__init__()
        self.user_agent = get_random_ua()
        self.proxy = get_random_ip()
        self.exception_list = (
        defer.TimeoutError, TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError,
        ConnectionDone)
        # 设置一个过期的代理集合
        self.blacked_proxies = set()
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        # 把更新代理的操作都放在process_request中进行. 这样, 不论是第一次的请求, 还是
        # 判断request中使用的代理, 如果它不等于当前的代理, 就把它设置为当前的代理
        if request.meta.get('proxy') != self.proxy and self.proxy not in self.blacked_proxies:
            request.headers.setdefault('User-Agent', self.user_agent)
            request.meta["proxy"] = self.proxy
            pass

    def process_response(self, request, response, spider):
        # 如果返回的response状态不是200，或者出现了验证码, 就重新获取代理.
        if response.status != 200 or "verify" in response.url:
            logger.warning("Proxy {}, 链接 {} 出错, 状态码为 {}".format(request.meta['proxy'], request.url, response.status))
            self.lock.acquire()
            # 如果失效的代理不在代理黑名单中, 表示这是这个代理地址第一次失效, 就执行更新代理的操作.
            if request.meta.get('proxy') not in self.blacked_proxies:
                # 如果代理过期, 就把它添加到代理黑名单列表中
                self.blacked_proxies.add(self.proxy)
                print('\n\n')
                print(self.blacked_proxies)
                print('\n\n')
                self.user_agent = get_random_ua()
                self.proxy = get_random_ip()

            self.lock.release()
            request.meta["proxy"] = None
            request.headers.setdefault('User-Agent', None)
            return request.replace(dont_filter=True)


    def process_exception(self, request, exception, spider):

        if isinstance(exception, self.exception_list):
            logger.warning("Proxy {} 链接出错 {}".format(request.meta['proxy'], exception))
            self.lock.acquire()
            # 如果失效的代理不在代理黑名单中, 表示这是这个代理地址第一次失效, 就执行更新代理的操作.
            if request.meta.get('proxy') not in self.blacked_proxies:
                # 如果代理过期, 就把它添加到代理黑名单列表中
                self.blacked_proxies.add(self.proxy)
                print('\n\n')
                print(self.blacked_proxies)
                print('\n\n')
                self.user_agent = get_random_ua()
                self.proxy = get_random_ip()

            self.lock.release()
            request.meta["proxy"] = None
            request.headers.setdefault('User-Agent', None)

        return request.replace(dont_filter=True)

class LagouFullSpiderMiddleware(object):
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


class LagouFullDownloaderMiddleware(object):
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
