# -*- coding:utf-8 -*-

from pymongo import MongoClient
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Pretreatment(object):
    def __init__(self, host, port, db_name, collection_name):
        self.client = MongoClient(host=host, port=port)
        self.db_name = db_name
        self.collection_name = collection_name
        pass

    def split_document(self):
        db = self.client[self.db_name]
        collection = db[self.collection_name]
        datas = collection.find()

        for data in datas:
            # 临时逻辑
            # if data.get('descript').strip() == [u'']:
            #     collection.remove({'_id': data.get('_id')})

            collection.update({
                '_id': data.get('_id')
            },{
                '$set': {'sentence': re.split(u'，|；|。', data.get('descript'))}
            })
        pass

    def pretreatment_sentence(self):

        pass

    def quantization_sentence(self):

        pass
    pass

if __name__ == '__main__':
    preteatment = Pretreatment(
        host='127.0.0.1', port=27017, db_name='lagou_spiders', collection_name='job_document'
    )
    preteatment.split_document()
    pass