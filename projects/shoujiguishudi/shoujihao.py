#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from multiprocess.core.spider import SpiderManger, Seed
from multiprocess.core import HttpProxy
from multiprocess.tools import process_manger
from multiprocess.tools import stringUtils
import re
import sys
from fake_useragent import UserAgent
import random


class Phone(SpiderManger):
    def __init__(self, seeds_file, **kwargs):
        super(Phone, self).__init__(**kwargs)
        self.proxies = list(map(lambda x:("http://u{}:crawl@192.168.0.71:3128".format(x)), range(28)))
        self.ua = UserAgent()
        self.phone_regx = re.compile(r'^\d{11,11}$')
        self.phone_number_checker = stringUtils.check_legality(pattern=r'^\d{11,11}$')
        for seed in open(seeds_file):
            seed = seed.strip("\n")
            if(self.phone_number_checker(seed)):
                self.seeds_queue.put(Seed(seed, kwargs["retries"]))
            else:
                self.log.info("legal_format: " + seed)
        self.pro_city_pattern = re.compile(r'<dd><span>号码归属地：</span>(.*?) (.*?)</dd>')
        self.telcompany_pattern = re.compile(r'<dd><span>手机卡类型：</span>(.*?)</dd>')

    def make_request(self, seed):
        url = "http://shouji.xpcha.com/{0}.html".format(seed.value)
        request = {"url": url,
                   "proxies": {"http": random.choice(self.proxies)},
                   "headers": {"Connection": "close", "User-Agent": self.ua.chrome}}
        return request

    def parse_item(self, content, seed):
        pro_city = self.pro_city_pattern.findall(content)
        tel_compay = self.telcompany_pattern.findall(content)
        result = {"code": 0, "phonenumber": seed.value, "province": pro_city[0][0],"city":(
            pro_city[0][0] if pro_city[0][1] == "" else pro_city[0][1]),"company":tel_compay[0]}
        return [result]


class NewPhone(SpiderManger):
    def __init__(self, seeds_file, **kwargs):
        super(NewPhone, self).__init__(**kwargs)
        self.ua = UserAgent()
        self.phone_regx = re.compile(r'^\d{11,11}$')
        self.phone_number_checker = stringUtils.check_legality(pattern=r'^\d{11,11}$')
        for seed in open(seeds_file):
            seed = seed.strip("\n")
            if(self.phone_number_checker(seed)):
                self.seeds_queue.put(Seed(seed, kwargs["retries"]))
            else:
                self.log.info("legal_format: " + seed)
        self.pro_city_pattern = re.compile(r'<dd><span>号码归属地：</span>(.*?) (.*?)</dd>')
        self.telcompany_pattern = re.compile(r'<dd><span>手机卡类型：</span>(.*?)</dd>')

    def make_request(self, seed):
        url = "http://shouji.xpcha.com/{0}.html".format(seed.value)
        request = {"url": url,
                   "proxy": self.used_proxy,
                   "encoding": "utf-8",
                   "headers": {"Connection": "close", "User-Agent": self.ua.chrome}}
        return request

    def parse_item(self, content, seed):
        pro_city = self.pro_city_pattern.findall(content)
        tel_compay = self.telcompany_pattern.findall(content)
        result = {"code": 0, "phonenumber": seed.value, "province": pro_city[0][0],"city":(
            pro_city[0][0] if pro_city[0][1] == "" else pro_city[0][1]),"company":tel_compay[0]}
        return [result]


class NewPhone2(SpiderManger):
    def __init__(self, seeds_file, **kwargs):
        super(NewPhone2, self).__init__(**kwargs)
        self.proxies = HttpProxy.getHttpProxy()
        self.ua = UserAgent()
        self.phone_regx = re.compile(r'^\d{11,11}$')
        self.phone_number_checker = stringUtils.check_legality(pattern=r'^\d{11,11}$')
        for seed in open(seeds_file):
            seed = seed.strip("\n")
            if(self.phone_number_checker(seed)):
                self.seeds_queue.put(Seed(seed, kwargs["retries"]))
            else:
                self.log.info("legal_format: " + seed)
        self.pro_city_pattern = re.compile(r'<dd><span>号码归属地：</span>(.*?) (.*?)</dd>')
        self.telcompany_pattern = re.compile(r'<dd><span>手机卡类型：</span>(.*?)</dd>')

    def process(self, seed):
        url = "http://shouji.xpcha.com/{0}.html".format(seed.value)
        request = {"url": url,
                   "proxies": {"http": random.choice(self.proxies)},
                   "headers": {"Connection": "close", "User-Agent": self.ua.chrome}}
        content = self.do_request(request)
        if content:
            pro_city = self.pro_city_pattern.findall(content)
            tel_compay = self.telcompany_pattern.findall(content)
            result = {"code": 0, "phonenumber": seed.value, "province": pro_city[0][0], "city": (
                pro_city[0][0] if pro_city[0][1] == "" else pro_city[0][1]), "company": tel_compay[0]}
            self.write([result])
            seed.ok()


if __name__ == "__main__":
    process_manger.kill_old_process(sys.argv[0])
    import logging
    import pycurl
    config = {"job_name": "shoujiguishudi"
              , "spider_num": 23
              , "use_new_download_api": True
              , "retries": 3
              , "request_timeout": 10
              , "pycurl_config": {pycurl.CONNECTTIMEOUT: 2, pycurl.TIMEOUT: 10}
              , "complete_timeout": 1*60
              , "sleep_interval": 0
              , "rest_time": 0
              , "write_seed": True
              , "seeds_file": "resource/buyer_phone.3"
              , "mongo_config": {"addr": "mongodb://192.168.0.13:27017", "db": "jicheng", "collection": "shoujiguishudi"}
              , "log_config": {"level": logging.INFO, "filename": sys.argv[0] + '.logging', "filemode":'a', "format":'%(asctime)s - %(filename)s - %(processName)s - [line:%(lineno)d] - %(levelname)s: %(message)s'}
              , "proxies_pool": HttpProxy.getHttpProxy()
              , "use_proxy": True}
    config = {"job_name": "shoujiguishudi"
        , "spider_num": 23
        , "use_new_download_api": True
        , "retries": 3
        , "request_timeout": 10
        , "pycurl_config": {pycurl.CONNECTTIMEOUT: 2, pycurl.TIMEOUT: 10}
        , "complete_timeout": 1 * 60
        , "sleep_interval": 0
        , "rest_time": 0
        , "write_seed": True
        , "seeds_file": "resource/buyer_phone.3"
        , "mongo_config": {"addr": "mongodb://192.168.0.13:27017", "db": "jicheng", "collection": "shoujiguishudi"}
        , "log_config": {"level": logging.INFO, "filename": sys.argv[0] + '.logging', "filemode": 'a',
                         "format": '%(asctime)s - %(filename)s - %(processName)s - [line:%(lineno)d] - %(levelname)s: %(message)s'}
        , "proxies_pool": HttpProxy.getHttpProxy()
        , "use_proxy": True
        , "random_proxy": True}
    p = NewPhone2(**config)
    p.main_loop(show_process=True)
