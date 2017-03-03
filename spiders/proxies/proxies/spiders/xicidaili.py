# -*- coding: utf-8 -*-

import scrapy

from vampire.items import VampireProxyItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ["xicidaili.com"]

    # INDEX_URL_TEMPLATE = 'http://api.xicidaili.com/free2016.txt'
    INDEX_URL_TEMPLATE = 'http://www.xicidaili.com/nn/{}'

    HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
               }
    MAX_PAGE = 10
    DOWNLOAD_DELAY = 10.0

    def start_requests(self):
        for i in range(self.MAX_PAGE):
            yield scrapy.Request('http://www.xicidaili.com/nn/{}'.format(i + 1), callback=self.parse, headers=self.HEADERS)
            pass

    def parse(self, response):
        # proxies = response.text.split('\r\n')
        # for proxy in proxies:
        #     url = '{}://{}'.format('http', proxy)
        #     item = VampireProxyItem()
        #     item['http'] = url
        #     yield item
        item = VampireProxyItem()

        ip = response.xpath('//*[@class="odd"]/td[2]/text()').extract()
        port = response.xpath('//*[@class="odd"]/td[3]/text()').extract()
        type = response.xpath('//*[@class="odd"]/td[6]/text()').extract()
        for proxy in zip(ip, port, type):
            url = '{}://{}{}'.format(proxy[2].lower(), proxy[0], ':{}'.format(proxy[1]) if str(proxy[1]) != '80' else '')
            item['http'] = url
            yield item
            pass
        pass