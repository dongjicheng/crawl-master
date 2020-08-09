# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import logging
# -*- coding: utf-8 -*-
import random

from fake_useragent import UserAgent
from scrapy.item import Item

class ExceptionCheckSpider(object):

    def __init__(self, settings):
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))

    #捕捉parse代码异常
    def process_spider_exception(self, response, exception, spider):
        self.logger.info(exception)
        yield {"_seed": response.meta["_seed"], "_status": 3}

    def process_spider_input(self, response, spider):
        if response._status == 0 and response.text:
            return None
        else:
            raise Exception("failed task!")

    def process_spider_output(self, response, result, spider):
        for r in result:
            if isinstance(r, (dict, Item)):
                r.update({"_seed": response.meta["_seed"], "_status": response._status})
            yield r

    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        return logging.LoggerAdapter(logger, {'spidermiddleware': self})

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
