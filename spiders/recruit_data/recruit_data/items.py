# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    companySize = scrapy.Field()
    firstType = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    financeStage = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    industryField = scrapy.Field()
    createTime = scrapy.Field()
    positionLables = scrapy.Field()
    salary = scrapy.Field()
    positionName = scrapy.Field()
    jobNature = scrapy.Field()
    companyFullName = scrapy.Field()
    companyLabelList = scrapy.Field()
    descript = scrapy.Field()
    pass
