# -*- coding: utf-8 -*-

import scrapy
import time
import sys
import urllib
import json
from scrapy.utils.project import get_project_settings
from recruit_data.items import RecruitDataItem
reload(sys)
sys.setdefaultencoding('utf-8')


class LagouSpider(scrapy.Spider):
    """拉勾网招聘数据抓取"""
    name = 'lagou_spider'
    allowed_domains = ["lagou.com"]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_java?px=default&city=%E5%85%A8%E5%9B%BD',
            'X-Requested-With': 'XMLHttpRequest',
        }
    }

    DOWNLOAD_DELAY = 0.2
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    INDEX_URL_TEMPLATE = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'
    COOKIES_ORIGINAL = 'user_trace_token=20170113145256-ea1ee772-d95c-11e6-a5f1-525400f775ce; LGUID=20170113145256-ea1eeb7a-d95c-11e6-a5f1-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f77lk60UqFg0FNkUs0B84dm00000PMAMj300000XdPY7C.THL0oUhY1x60UWdBmy-bIy9EUyNxTAT0T1d9mHu9nyFWm10snA7Wnvwb0ZRqrDNaf1RLnHPAf1bkn19an1cYPH6YPW0sPjTzPW-7nj60mHdL5iuVmv-b5Hc3rHmsPHb3n1mhTZFEuA-b5HDv0ARqpZwYTjCEQLILIz4_myIEIi4WUvYE5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAn0mLFW5HcsnWnk%26tpl%3Dtpl_10085_14394_1%26l%3D1050461913%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E4%2525B8%25259A%2525E7%25259A%252584%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E6%25258B%25259B%2525E8%252581%252598%2525E5%2525B9%2525B3%2525E5%25258F%2525B0%25252C%2526xp%253Did%28%252522m4c6eceef%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D230%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26issp%3D1%26f%3D3%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26oq%3Ddata%2525E5%2525A4%25258D%2525E6%252595%2525B0%26inputT%3D2899%26prefixsug%3Dlagou%26rsp%3D0; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; _gat=1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=53; index_location_city=%E6%B7%B1%E5%9C%B3; login=false; unick=""; _putrc=""; JSESSIONID=71FF46159FDD2BBB7BC033C34D4FC590; TG-TRACK-CODE=index_search; SEARCH_ID=78d24ca82c0a4cf7bffdc456c7b2082f; _ga=GA1.2.317118795.1484290377; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1484290377,1484290895,1486095035,1486732078; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486733367; LGSID=20170210210757-f143586d-ef91-11e6-8f66-5254005c3644; LGRID=20170210212927-f1db18c6-ef94-11e6-a159-525400f775ce'

    def start_requests(self):
        cities = ['北京']
        jobs = ['java', 'python']
        cookies = [dict(name=v.split('=')[0], value=v.split('=')[1]) for v in self.COOKIES_ORIGINAL.split(';')]
        pages = [x+1 for x in range(30)]
        for city in cities:
            for job in jobs:
                referer = 'https://www.lagou.com/jobs/list_{}?px=default&city={}'.format(urllib.quote(job),
                                                                                         urllib.quote(city),
                                                                                         )
                self.custom_settings['DEFAULT_REQUEST_HEADERS']['Referer'] = referer

                for page in pages:
                    payload = {
                        'first': 'false',
                        'pn': '{}'.format(page),
                        'kd': '{}'.format(job),
                    }

                    yield scrapy.http.FormRequest(
                        self.INDEX_URL_TEMPLATE.format(urllib.quote(city)),
                        callback=self.parse,
                        formdata=payload,
                        cookies=cookies,
                    )
                    pass
                pass
            pass

    def parse(self, response):
        try:
            job_message = json.loads(response.body)
        except ValueError:
            self.logger.debug("返回json为非可用数据")
            raise scrapy.exceptions.DropItem

        job_results = job_message['content']['positionResult']['result']
        job_id = job_message['content']['hrInfoMap'].keys()

        # 忍不住想吐槽一下，真恶心！！！（i为url中唯一id，j为json文本内容为格式化数据）
        for i in job_id:
            for j in job_results:
                tmp = job_message['content']['hrInfoMap'][i]['userId']
                if j['publisherId'] == tmp:
                    yield scrapy.Request('https://www.lagou.com/jobs/{}.html'.format(i),
                                         meta={'data': j},
                                         callback=self.parse_detail
                                         )
                    pass

        pass

    def parse_detail(self, response):
        item = RecruitDataItem()

        tmp = ''
        descript = response.xpath('//*[@class="job_bt"]/div/p/span/text()').extract()

        if not descript:
            descript = response.xpath('//*[@class="job_bt"]/div/p/text()').extract()

        for x in range(len(descript)):
            tmp = tmp + descript[x]
            pass

        item['url'] = response.url
        item['format_data'] = response.meta['data']
        item['descript'] = tmp
        yield item
        pass