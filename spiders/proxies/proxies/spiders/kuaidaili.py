# -*- coding: utf-8 -*-

import scrapy
import re
from vampire.items import VampireProxyItem


class KuaidailiSpider(scrapy.Spider):
    name = 'kuaidaili'
    allowed_domains = ["kuaidaili.com"]
    MAX_PAGE = 10
    RATE = 2.0
    DOWNLOAD_DELAY = 0.8

    def start_requests(self):
        # ..todo::
        # 个别页面莫名其妙的503错误，越往后越多，现在也能获取，但不是全量
        for p in range(self.MAX_PAGE):
            # 国内高匿
            target_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(str(p + 1))
            # 国内透明
            # target_url = 'http://www.kuaidaili.com/free/intr/{}/'.format(str(p + 1))
            yield scrapy.Request(target_url, callback=self.parse_detail)
            pass
        pass

    def parse_detail(self, response):
        for x in range(15):
            ip = response.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[1]/text()'.format(str(x + 1))).extract()[0]
            port = response.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[2]/text()'.format(str(x + 1))).extract()[0]
            type = response.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[4]/text()'.format(str(x + 1))).extract()[0].lower()
            delay = response.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[6]/text()'.format(str(x + 1))).extract()[0]

            delay = re.findall(r'\d+', delay)[0]

            if float(delay) < self.RATE:
                url = '{}://{}{}'.format(type, ip, ':{}'.format(port) if str(port) != '80' else '')

                item = VampireProxyItem()
                item['http'] = url
                yield item
                pass
        pass
    pass