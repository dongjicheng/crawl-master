#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocess.scrapy_redis.spiders import ClusterRunner,ThreadFileWriter, ThreadMonitor


class shoujiguishudirunner(ClusterRunner):
    def __init__(self, *args, **kwargs):
        super(shoujiguishudirunner, self).__init__(*args, **kwargs)

    def init_start_urls(self):
        self.redis.delete(self.start_urls_redis_key)
        self.redis.delete(self.items_redis_key)
        buffer = []
        buffer_size = 1024
        for i, seed in enumerate(open("shoujiguishudi/resource/buyer_phone.3")):
            seed = seed.strip()
            url = "http://shouji.xpcha.com/{0}.html".format(seed)
            data = {"url": url, "meta": {"_seed": seed}}
            buffer.append(str(data))
            if len(buffer) % buffer_size == 0:
                self.redis.sadd(self.start_urls_redis_key, *buffer)
                buffer = []
        if buffer:
            self.redis.sadd(self.start_urls_redis_key, *buffer)

    def get_thread_writer(self):
        thread_writer = ThreadFileWriter(redis_key=self.items_redis_key, bar_name=self.items_redis_key,
                                         out_file="shoujiguishudi/result/shoujiguishudi.txt",
                                       table_header=["_seed","_status","phonenumber", "province", "city", "company"])
        thread_writer.setDaemon(False)
        return thread_writer

    def get_thread_monitor(self):
        thread_monitor = ThreadMonitor(redis_key=self.start_urls_redis_key, bar_name=self.start_urls_redis_key)
        thread_monitor.setDaemon(True)
        return thread_monitor


if __name__ == '__main__':
    runner = shoujiguishudirunner(spider_name="shoujiguishudi", spider_num=16)
    runner.run()
    # r1 = set()
    # for i in open("shoujiguishudi/resource/buyer_phone.3"):
    #     r1.add(i.strip())
    # r2 = set()
    # for i in open("shoujiguishudi/result/shoujiguishudi.txt"):
    #     r2.add(i.split("\t")[0])
    #
    # print(r1-r2)