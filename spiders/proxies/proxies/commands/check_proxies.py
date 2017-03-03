# -*-coding:utf-8 -*-

from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler
from multiprocessing.dummy import Pool as ThreadPool
import redis
import requests


class Command(ScrapyCommand):
    requires_project = True

    def run(self, args, opts):
        r = redis.Redis(host='localhost', port=6379, db=4)
        ips = r.keys()

        def test_ip(ip):
            proxies = {'http': '{}'.format(ip)}
            try:
                result = requests.get('http://www.baidu.com', proxies=proxies, timeout=10)
                if result.status_code != 200:
                    r.delete(ip)
                    print '{} 未通过测试，已删除'.format(ip)
            except:
                r.delete(ip)
                print '{} 未通过测试，已删除'.format(ip)
            pass

        pool = ThreadPool(100)
        pool.map(test_ip, ips)
        pool.close()
        pool.join()
        pass
    pass