# -*- coding: utf-8 -*-

from mongoengine import StringField, URLField, DateTimeField
from mongoengine import Document
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class JobDocument(Document):
    url = URLField(verbose_name='抓取页URL', primary_key=True, required=True, help_text="详情页")
    descript = StringField(verbose_name='职位描述', max_length=2000, required=True, help_text='短文本')
    format_data = StringField(verbose_name='格式化数据', max_length=2000, required=True, help_text='标准json')
    date_created = DateTimeField()
    date_updated = DateTimeField()
    pass