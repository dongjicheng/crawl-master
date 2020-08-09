# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

# -*- coding: utf-8 -*-
import random

from fake_useragent import UserAgent


class CustomHeadersDownLoadMiddleware(object):

    def __init__(self):
        self.user_agent = UserAgent()

    @classmethod
    def get_http_proxy(cls):
        proxies = []
        proxies.extend(map(lambda x: ("http://u{0}:crawl@192.168.0.71:3128".format(x)), range(28)))
        #proxies.extend(map(lambda x: ("http://u{1}:crawl@192.168.0.{0}:3128".format(x[0], x[1])),
        #                  itertools.product(range(72, 79), range(30))))
        random.shuffle(proxies)
        return proxies

    def process_request(self, request, spider):
        request.headers['user-agent'] = self.user_agent.chrome
        request.headers["Connection"] = "keep-alive"
        request.headers["accept-encoding"] = "gzip, deflate, br"
        request.headers["accept-language"] = "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4"
        request.headers["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp;q=0.8"
        request.headers["Accept-Charset"] = "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7"
        request.meta['proxy'] = random.choice(self.get_http_proxy())
        self.logger.info((request.headers,request.meta))

    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        return logging.LoggerAdapter(logger, {'middleware': self})


from scrapy.downloadermiddlewares.retry import RetryMiddleware

import logging

from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)


class NewRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            response._status = 0
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            ret = self._retry(request, reason, spider)
            if ret:
                return ret
            else:
                #重试次数达到状态
                response._status = 1
                return response
        response._status = 0
        return response


from scrapy.http import HtmlResponse


class ProcessAllExceptionMiddleware(object):
    def process_exception(self, request, exception, spider):
        response = HtmlResponse(url='', request=request)
        response._status = 2
        self.logger.debug('not contained exception: %s' % exception)
        return response

    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        return logging.LoggerAdapter(logger, {'middleware': self})
