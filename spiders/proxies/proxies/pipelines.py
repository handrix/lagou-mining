# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import importlib
import json
import os
import uuid
from datetime import datetime, timedelta
import mongoengine
import redis
from scrapy import exceptions
from vampire import items
from vampire.models import EntryDocument



class ProxiesPipeline(object):
    clients = []
    total = 0

    def __init__(self, redis_pool, spider):
        if not isinstance(redis_pool, list):
            redis_pool = list(redis_pool)
        self.redis_pool = redis_pool

    def from_crawler(cls, crawler):
        settings = crawler.settings
        redis_pool = settings.get('VAMPIRE_PROXY_POOL')
        if not redis_pool:
            raise exceptions.NotConfigured(
                'settings中未設置VAMPIRE_PROXY_POOL')
        return cls(redis_pool, crawler.spider)

    from_crawler = classmethod(from_crawler)

    def open_spider(self, spider):
        for v in self.redis_pool:
            self.clients.append(redis.Redis.from_url(v))

    def close_spider(self, spider):
        spider.logger.info(
            '總共抓取代理條數: %d'
            % self.total)

    def process_item(self, item, spider):
        address = item['http']
        key = address
        for client in self.clients:
            client.setex(key, address, 3600)

        spider.logger.debug(
            '已抓取 %s'
            % address)
        self.total += 1
        return item
