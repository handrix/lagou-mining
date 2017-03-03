# -*- coding: utf-8 -*-

import scrapy
import re

from vampire.items import VampireProxyItem


class YoudailiSpider(scrapy.Spider):
    name = 'youdaili'
    INDEX_URL_TEMPLATE = 'http://www.youdaili.net/Daili/http/'
    DOWNLOAD_DELAY = 1.0
    MAX_PAGE = 5

    def start_requests(self):
        yield scrapy.Request(self.INDEX_URL_TEMPLATE, callback=self.parse_list)
        pass

    def parse_list(self, response):
        # 最新更新代理列表
        target_url = response.xpath('//*[@class="chunlist"]/ul/li[1]/p/a/@href').extract()[0]
        tmp = target_url

        for x in range(self.MAX_PAGE):
            if x == 0:
                yield scrapy.Request(target_url, callback=self.parse_detail)
                pass
            target_url = tmp[:-5] + '_' + str(x + 1) + tmp[-5:]
            yield scrapy.Request(target_url, callback=self.parse_detail)
            pass
        pass

    def parse_detail(self, response):
        proxies = response.xpath('//*[@class="content"]/p/text()').extract()
        # 最后一个是'\r\n'
        proxies.pop()
        for proxy in proxies:
            type = re.findall(r'@(.*)#', proxy)[0].lower()
            port = re.findall(r':(.*)@', proxy)[0]
            ip = re.findall(r'(.*):', proxy)[0]
            # print 'ooooooooooooo', type, port, ip
            if type != 'http':
                continue

            url = '{}://{}{}'.format(type, ip, ':{}'.format(port) if str(port) != '80' else '')

            item = VampireProxyItem()
            item['http'] = url
            yield item
            pass
        pass
    pass