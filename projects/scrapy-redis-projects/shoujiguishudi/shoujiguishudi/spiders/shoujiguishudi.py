#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from scrapy.item import Item, Field

from multiprocess.scrapy_redis.spiders import JiChengSpider




class ShoujiSpider(JiChengSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'shoujiguishudi'
    pro_city_pattern = re.compile(r'<dd><span>号码归属地：</span>(.*?) (.*?)</dd>')
    telcompany_pattern = re.compile(r'<dd><span>手机卡类型：</span>(.*?)</dd>')

    def parse(self, response):
        if response._status == 0 and response.text:
            pro_city = self.pro_city_pattern.findall(response.text)
            tel_compay = self.telcompany_pattern.findall(response.text)
            yield {"phonenumber": response.meta["_seed"], "province": pro_city[0][0],
                   "city": pro_city[0][0] if pro_city[0][1] == "" else pro_city[0][1],
                   "company": tel_compay[0]}
        else:
            yield {}

