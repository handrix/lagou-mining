# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mongoengine
from datetime import datetime
from . import JobDocument


class RecruitDataPipeline(object):
    client = None

    def open_spider(self, spider):
        self.client = mongoengine.connect('lagou_spiders', host='localhost')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        url = item['url']
        del item['url']

        try:
            doc = JobDocument.objects.get(pk=url)
        except JobDocument.DoesNotExist:
            doc = JobDocument(pk=url)
            doc.date_created = datetime.now()
            doc.date_updated = doc.date_created

        doc.descript = item['descript']
        doc.companySize = item['companySize']
        doc.firstType = item['firstType']
        doc.workYear = item['workYear']
        doc.education = item['education']
        doc.financeStage = item['financeStage']
        doc.city = item['city']
        doc.district = item['district']
        doc.industryField = item['industryField']
        doc.createTime = item['createTime']
        doc.positionLables = item['positionLables']
        doc.salary = item['salary']
        doc.positionName = item['positionName']
        doc.jobNature = item['jobNature']
        doc.companyFullName = item['companyFullName']
        doc.companyLabelList = item['companyLabelList']
        doc.save()
        return item
