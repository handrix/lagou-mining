# -*- coding: utf-8 -*-

import scrapy
import time
import sys
import urllib
import json
import types
from scrapy.utils.project import get_project_settings
from recruit_data.items import BookDataItem
reload(sys)
sys.setdefaultencoding('utf-8')


class LagouSpider(scrapy.Spider):
    """拉勾网招聘数据抓取"""
    name = 'amazon'
    allowed_domains = ["amazon.cn"]

    DOWNLOAD_DELAY = 5
    handle_httpstatus_list = [503]
    HEADERS = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    URL_TEMPLATE = 'https://www.amazon.cn/b?ie=UTF8&page={}&node=66081{}051'
    COOKIES_ORIGINAL = 'x-wl-uid=1G/Ua8LCVV7NMunFo0N84+SfQ0Dt7QUjlgQ+1RyvqmLqQU4lo+qn1mZiATac9BtdFhECuQk424Tr+UI3zLoEy2g==; gw-warning-displayed=displayed; session-token="LgFqvcvpAp4LCMBODKSyLHOW1tLBI7+kel7x5eKDedEfb8gz/Hhf4pAyrQSWqE7lUP/2TacWrJEysAxYd3xhanWtOd+8rUseY+ZLu/9CrkzDGl8HBMruT83rtPx7oW0aCVpoL0ZORd/v/mWcWYO8UHxHb2DhheYAErhuT+jPkphy+ZbT8LAeVLu4VHEeCDG0Gq9PtUJZ3hIZNXQU02lgpIqDeXJuW/q/uTI7qy0wjsk="; x-acbcn="ZO7wIIFH9JEW@FlVQVY4TfqeqoCwkMAN"; at-main=Atza|IwEBIK4TgxAng8QgP1Fl-lym5CoWqhUi3N2AIFsGGP_IS-PCYZqZ6ZHGcpqHsyk9TAxFPAEdMkqOEHVOHnlDDTKvD67J95qP5D240gov9yerWXzlxNAVTU1wDsEqWoMp0OL9NknSOL0zmgga18oDoBnet8gdPzcaIQqD3mB8JP2AfBAW9GhRItg3uHOCEvhaVq6jRcd-FwYaY9dXijqG3H06UA7oaxwezierMX8OZtoC8Dqlz1pNdOtJKQxAe_sKPId948WPGF1JQx4Z81oH2B_rbd8ZMhGqtvlKl4dm0mCwPFqOM50H9skqBD3VCBc8e_sNyjmW-NTLYFliL7GQ_5Z8RT5WGMneBlk2_LAynDdp0_mn5HZZjXDM_Z0L66KbJL7GWvANm0uV1ZkGl2apLesoO3br; __utma=164006624.1322084484.1457454873.1475288289.1475290368.74; __utmz=164006624.1475290368.74.19.utmccn=(referral)|utmcsr=amazon.cn|utmcct=/s/ref=nb_sb_noss_1|utmcmd=referral; __utmv=164006624.rzaixiancom-23; s_fid=043CC390B97FA108-3F9901D1E657F3DB; ubid-acbcn=479-7313174-1981907; session-id-time=2082729601l; session-id=454-8954288-6765618; csm-hit=S57PBDY214XX37KBTK3B+s-S57PBDY214XX37KBTK3B|1475377881458'
    def start_requests(self):
        cookies = [dict(name=v.split('=')[0], value=v.split('=')[1]) for v in
                   self.COOKIES_ORIGINAL.split(';')]

        num_list = [x + 2 for x in range(3)]
        page_list = [x + 1 for x in range(75)]
        for num in num_list:
            for page in page_list:
                target_url = self.URL_TEMPLATE.format(page, num)
                yield scrapy.Request(target_url,
                                     callback=self.parse,
                                     cookies=cookies,
                                     headers=self.HEADERS)
                pass
            pass

    def parse(self, response):
        cookies = [dict(name=v.split('=')[0], value=v.split('=')[1]) for v in
                   self.COOKIES_ORIGINAL.split(';')]

        if response.status == 301:
            yield scrapy.Request(response.headers['Location'],
                                 callback=self.parse,
                                 cookies=cookies,
                                 headers=self.HEADERS
                                 )
        else:
            urls = response.xpath('//*[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href').extract()[:-2]
            for url in urls:
                yield scrapy.Request(url,
                                     callback=self.detail_parse,
                                     cookies=cookies,
                                     headers=self.HEADERS
                                     )
                pass
        pass

    def detail_parse(self, response):
        cookies = [dict(name=v.split('=')[0], value=v.split('=')[1]) for v in
                   self.COOKIES_ORIGINAL.split(';')]

        if response.status == 301:
            yield scrapy.Request(response.headers['Location'],
                                 callback=self.detail_parse,
                                 cookies=cookies,
                                 headers=self.HEADERS
                                 )
        else:
            item = BookDataItem()

            item['url'] = response.url
            item['title'] = response.xpath(
                '/html/head/title/text()').extract()[0]
            item['book_name'] = response.xpath(
                '//span[@id="productTitle"]/text()').extract()[0]
            f = open('/tmp/{}'.format(response.url[-6:]), 'a')
            f.write(str(response.text))
            f.close()
            descripts = open('/tmp/{}'.format(response.url[-6:])).readlines()
            for descript in enumerate(descripts):
                if "<em></em>" in descript[1]:
                    tmp = descripts[descript[0] - 1]
            item['descript'] = tmp
            item['auth'] = response.xpath(
                '//span[@class="author notFaded"]/a/text()').extract()[0]
            item['price'] = response.xpath(
                '//span[@class="a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P"]/text()'
            ).extract()[0]
            yield item
            pass
        pass