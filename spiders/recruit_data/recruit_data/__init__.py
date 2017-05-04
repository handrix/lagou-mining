# -*- coding: utf-8 -*-

from mongoengine import StringField, URLField, DateTimeField, ListField
from mongoengine import Document
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class JobDocument(Document):
    url = URLField(verbose_name='抓取页URL', primary_key=True, required=True, help_text="详情页")
    descript = StringField(verbose_name='职位描述', max_length=2048, default='', help_text='短文本')
    companySize = StringField(verbose_name='公司规模', max_length=64, default='', help_text='公司规模')
    firstType = StringField(verbose_name='我也不知道这是个啥', max_length=128, default='', help_text='')
    workYear = StringField(verbose_name='工作经验', max_length=64, default='', help_text='工作经验')
    education = StringField(verbose_name='教育经历', max_length=64, default='', help_text='')
    financeStage = StringField(verbose_name='不知道是个啥', max_length=128, default='', help_text='')
    city = StringField(verbose_name='城市', max_length=32, default='', help_text='城市')
    district = StringField(verbose_name='描述', max_length=512, default='', help_text='描述')
    industryField = StringField(verbose_name='', max_length=256, help_text='')
    createTime = StringField(verbose_name='', max_length=128, default='', help_text='')
    positionLables = ListField(verbose_name='', max_length=256, default='', help_text='')
    salary = StringField(verbose_name='', max_length=64, default='', help_text='')
    positionName = StringField(verbose_name='', max_length=256, default='', help_text='')
    jobNature = StringField(verbose_name='', max_length=256, default='', help_text='')
    companyFullName = StringField(verbose_name='', max_length=64, default='', help_text='')
    companyLabelList = ListField(verbose_name='', max_length=256, default='', help_text='')
    date_created = DateTimeField()
    date_updated = DateTimeField()
    pass


class BookDocument(Document):
    url = URLField(verbose_name='抓取页URL', primary_key=True, required=True, help_text="索引")
    title = StringField(verbose_name='抓取页标题', required=True, default='')
    book_name = StringField(verbose_name='图书名', required=True, default='')
    descript = StringField(verbose_name='描述', required=True, default='')
    auth = StringField(verbose_name='作者', required=True, default='')
    price = StringField(verbose_name='价格', required=True, default='')
    date_created = DateTimeField()
    date_updated = DateTimeField()
    pass