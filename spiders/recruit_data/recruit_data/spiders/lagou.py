# -*- coding: utf-8 -*-

import scrapy
import time
import sys
import urllib
import json
import types
from scrapy.utils.project import get_project_settings
from recruit_data.items import RecruitDataItem
reload(sys)
sys.setdefaultencoding('utf-8')


class LagouSpider(scrapy.Spider):
    """拉勾网招聘数据抓取"""
    name = 'lagou'
    allowed_domains = ["lagou.com"]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_java?px=default&city=%E5%85%A8%E5%9B%BD',
            'X-Requested-With': 'XMLHttpRequest',
        }
    }

    DOWNLOAD_DELAY = 1.2
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    INDEX_URL_TEMPLATE = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'
    COOKIES_ORIGINAL = 'user_trace_token=20170113145256-ea1ee772-d95c-11e6-a5f1-525400f775ce; LGUID=20170113145256-ea1eeb7a-d95c-11e6-a5f1-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f77lk60UqFg0FNkUs0B84dm00000PMAMj300000XdPY7C.THL0oUhY1x60UWdBmy-bIy9EUyNxTAT0T1d9mHu9nyFWm10snA7Wnvwb0ZRqrDNaf1RLnHPAf1bkn19an1cYPH6YPW0sPjTzPW-7nj60mHdL5iuVmv-b5Hc3rHmsPHb3n1mhTZFEuA-b5HDv0ARqpZwYTjCEQLILIz4_myIEIi4WUvYE5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAn0mLFW5HcsnWnk%26tpl%3Dtpl_10085_14394_1%26l%3D1050461913%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E4%2525B8%25259A%2525E7%25259A%252584%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E6%25258B%25259B%2525E8%252581%252598%2525E5%2525B9%2525B3%2525E5%25258F%2525B0%25252C%2526xp%253Did%28%252522m4c6eceef%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D230%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26issp%3D1%26f%3D3%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26oq%3Ddata%2525E5%2525A4%25258D%2525E6%252595%2525B0%26inputT%3D2899%26prefixsug%3Dlagou%26rsp%3D0; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; _gat=1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=53; index_location_city=%E6%B7%B1%E5%9C%B3; login=false; unick=""; _putrc=""; JSESSIONID=71FF46159FDD2BBB7BC033C34D4FC590; TG-TRACK-CODE=index_search; SEARCH_ID=78d24ca82c0a4cf7bffdc456c7b2082f; _ga=GA1.2.317118795.1484290377; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1484290377,1484290895,1486095035,1486732078; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486733367; LGSID=20170210210757-f143586d-ef91-11e6-8f66-5254005c3644; LGRID=20170210212927-f1db18c6-ef94-11e6-a159-525400f775ce'

    def start_requests(self):
        cities = ['北京', '上海', '杭州', '广州', '成都']
        jobs = list(set(['Java', 'PHP', 'C++', 'Android', 'iOS', '数据挖掘', '测试', '前端开发', 'html5', '技术总监', '架构师', 'CTO', '后端开发', 'Java', 'Python', 'PHP', '.NET', 'C#', 'C++', 'C', 'VB', 'Delphi', 'Perl', 'Ruby', 'Hadoop', 'Node.js', '数据挖掘', '自然语言处理', '搜索算法', '精准推荐', '全栈工程师', 'Go', 'ASP', 'Shell', '后端开发其它', '移动开发', 'HTML5', 'Android', 'iOS', 'WP', '移动开发其它', '前端开发', 'web前端', 'Flash', 'html5', 'JavaScript', 'U3D', 'COCOS2D-X', '前端开发其它', '测试', '测试工程师', '自动化测试', '功能测试', '性能测试', '测试开发', '游戏测试', '白盒测试', '灰盒测试', '黑盒测试', '手机测试', '硬件测试', '测试经理', '测试其它', '运维', '运维工程师', '运维开发工程师', '网络工程师', '系统工程师', 'IT支持', 'IDC', 'CDN', 'F5', '系统管理员', '病毒分析', 'WEB安全', '网络安全', '系统安全', '运维经理', '运维其它', 'DBA', 'MySQL', 'SQLServer', 'Oracle', 'DB2', 'MongoDB', 'ETL', 'Hive', '数据仓库', 'DBA其它', '高端职位', '技术经理', '技术总监', '架构师', 'CTO', '运维总监', '技术合伙人', '项目总监', '测试总监', '安全专家', '高端技术职位其它', '项目管理', '项目经理', '项目助理', '硬件开发', '硬件', '嵌入式', '自动化', '单片机', '电路设计', '驱动开发', '系统集成', 'FPGA开发', 'DSP开发', 'ARM开发', 'PCB工艺', '模具设计', '热传导', '材料工程师', '精益工程师', '射频工程师', '硬件开发其它', '企业软件', '实施工程师', '售前工程师', '售后工程师', 'BI工程师', '企业软件其它', '产品总监', '产品经理', '数据产品经理', '游戏策划', '产品经理', '产品经理', '网页产品经理', '移动产品经理', '产品助理', '数据产品经理', '电商产品经理', '游戏策划', '产品实习生', '产品设计师', '网页产品设计师', '无线产品设计师', '高端职位', '产品部经理', '产品总监', '游戏制作人', 'UI设计师', '交互设计', '网页设计师', '平面设计师', '视觉设计师', '视觉设计', '网页设计师', 'Flash设计师', 'APP设计师', 'UI设计师', '平面设计师', '美术设计师（2D/3D）', '广告设计师', '多媒体设计师', '原画师', '游戏特效', '游戏界面设计师', '视觉设计师', '游戏场景', '游戏角色', '游戏动作', '用户研究', '数据分析师', '用户研究员', '游戏数值策划', '高端职位', '设计经理/主管', '设计总监', '视觉设计经理/主管', '视觉设计总监', '交互设计经理/主管', '交互设计总监', '用户研究经理/主管', '用户研究总监', '交互设计', '网页交互设计师', '交互设计师', '无线交互设计师', '硬件交互设计师', '新媒体运营', '编辑', '数据运营', '运营总监', 'COO', '运营', '内容运营', '产品运营', '数据运营', '用户运营', '活动运营', '商家运营', '品类运营', '游戏运营', '网络推广', '运营专员', '网店运营', '新媒体运营', '海外运营', '运营经理', '编辑', '副主编', '内容编辑', '文案策划', '记者', '客服', '售前咨询', '售后客服', '淘宝客服', '客服经理', '高端职位', '主编', '运营总监', 'COO', '客服总监', '市场推广', '市场总监', '市场策划', 'BD', '销售总监', '市场/营销', '市场策划', '市场顾问', '市场营销', '市场推广', 'SEO', 'SEM', '商务渠道', '商业数据分析', '活动策划', '网络营销', '海外市场', '政府关系', '公关', '媒介经理', '广告协调', '品牌公关', '销售', '销售专员', '销售经理', '客户代表', '大客户代表', 'BD经理', '商务渠道', '渠道销售', '代理商销售', '销售助理', '电话销售', '销售顾问', '商品经理', '高端职位', '市场总监', '销售总监', '商务总监', 'CMO', '公关总监', '采购总监', '投资总监', '供应链', '物流', '仓储', '采购', '采购专员', '采购经理', '商品经理', '投资', '分析师', '投资顾问', '投资经理', 'HR', '行政', '财务', '审计', '人力资源', '人事/HR', '培训经理', '薪资福利经理', '绩效考核经理', '人力资源', '招聘', 'HRBP', '员工关系', '行政', '助理', '前台', '行政', '总助', '文秘', '财务', '会计', '出纳', '财务', '结算', '税务', '审计', '风控', '高端职位', '行政总监/经理', '财务总监/经理', 'HRD/HRM', 'CFO', 'CEO', '法务', '法务', '律师', '专利', '投资', '融资', '并购', '风控', '投融资', '投资经理', '分析师', '投资助理', '融资', '并购', '行业研究', '投资者关系', '资产管理', '理财顾问', '交易员', '风控', '风控', '资信评估', '合规稽查', '律师', '审计税务', '审计', '法务', '会计', '清算', '高端职位', '投资总监', '融资总监', '并购总监', '风控总监', '副总裁']))
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

        data = response.meta['data']
        tmp = ''
        descript = response.xpath('//*[@class="job_bt"]/div/p/span/text()').extract()

        if not descript:
            descript = response.xpath('//*[@class="job_bt"]/div/p/text()').extract()

        if not descript:
            descript = response.xpath('//*[@class="job_bt"]/div/p/strong/text()').extract()

        for x in range(len(descript)):
            tmp = tmp + descript[x]
            pass

        item['url'] = response.url
        item['companySize'] = data.get('companySize')
        item['firstType'] = data.get('firstType')
        item['workYear'] = data.get('workYear')
        item['education'] = data.get('education')
        item['financeStage'] = data.get('financeStage')
        item['city'] = data.get('city')
        item['district'] = data.get('district')
        item['industryField'] = data.get('industryField')
        item['createTime'] = data.get('createTime')
        if not data.get('positionLables'):
            data['positionLables'] = ['暂无']
        else:
            if data.get('positionLables') is not types.ListType:
                data['positionLables'] = list(data.get('positionLables'))
        item['positionLables'] = data.get('positionLables')
        item['salary'] = data.get('salary')
        item['positionName'] = data.get('positionName')
        item['jobNature'] = data.get('jobNature')
        item['companyFullName'] = data.get('companyFullName')
        if not data.get('companyLabelList'):
            data['companyLabelList'] = ['暂无']
        else:
            if data.get('companyLabelList') is not types.ListType:
                data['companyLabelList'] = list(data.get('companyLabelList'))
        item['companyLabelList'] = data.get('companyLabelList')
        item['descript'] = tmp
        yield item
        pass