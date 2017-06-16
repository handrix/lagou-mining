# -*- coding:utf-8 -*-

from pymongo import MongoClient
import jieba
import sklearn
import re
import sys
from sklearn.feature_extraction.text import CountVectorizer
from random import choice
reload(sys)
sys.setdefaultencoding('utf8')

class Pretreatment(object):
    def __init__(self, host, port, db_name, collection_name):
        self.client = MongoClient(host=host, port=port)
        self.db_name = db_name
        self.collection_name = collection_name
        self.word_table = []
        pass

    def get_collection(self):
        db = self.client[self.db_name]
        collection = db[self.collection_name]
        return collection
        pass

    def split_document(self, collection):
        items = collection.find()

        for item in items:
            # 临时逻辑
            # if item.get('descript').strip() == [u'']:
            #     collection.remove({'_id': item.get('_id')})

            sentences = re.split(u'，|；|。', item.get('descript').replace(u' ', ''))
            del sentences[-1]

            # 英文，HR摸鱼等的招聘信息作为脏数据清洗。
            if not sentences:
                collection.remove({'_id': item.get('_id')})

            collection.update({
                '_id': item.get('_id')
            },{
                '$set': {'sentence': [sentence.strip() for sentence in sentences]}
            })
        pass

    def pretreatment_sentence(self, collection):
        items = collection.find()
        stop_words = [unicode(line.strip()) for line in open(
            __file__.rsplit('/', 1)[0] + '/config/stop-words.txt').readlines()]

        for item in items:
            sentence_list = [(' '.join(
                set(jieba.cut(sentence)) - set(stop_words))) for sentence in item.get('sentence')]

            collection.update({
                '_id': item.get('_id')
            },{
                '$set': {'cut_result': sentence_list}
            })
            pass
        pass

    def said_temp(self, collection):
        items = collection.find()
        for item in items:
            label_list = []
            label = [0, 1, 2, 3, 4]
            k_means_label = [0, 1]
            for cut_sentense in item.get('cut_result'):
                if cut_sentense == '' or cut_sentense == ' ':
                    label_list.append([0, 0])
                else:
                    label_list.append([choice(label), choice(k_means_label)])
                    pass
            collection.update({
                '_id': item.get('_id')
            }, {
                '$set': {'label': label_list}
            })
        pass

    def quantization_sentence(self, words_table, collection):
        items = collection.find()
        word_tables = words_table.find()
        cv = CountVectorizer(vocabulary=words_table)

        for item in items:
            cv.fit_transform(item.get('cut_result')).toarray()
            pass
        pass

    def get_word_table(self, collection):
        items = collection.find()
        word_table = []
        num = 0

        for item in items:
            num += 1
            for i in item.get('cut_result'):
                word_table.extend(i.split(' '))
                print num
                pass
            pass
        word_table = list(set(word_table))
        client = MongoClient()
        db = client['lagou_spiders']
        collection = db['word_table']
        collection.insert({'word_table': word_table})
        pass
    pass

if __name__ == '__main__':
    preteatment_words_table = Pretreatment(
        host='127.0.0.1', port=27017, db_name='lagou_spiders', collection_name='word_table'
    )
    preteatment = Pretreatment(
        host='127.0.0.1', port=27017, db_name='lagou_spiders', collection_name='job_document'
    )
    # preteatment.pretreatment_sentence(preteatment.get_collection())
    # preteatment.split_document(preteatment.get_collection())
    # preteatment.get_word_table(preteatment.get_collection())
    # preteatment.quantization_sentence(preteatment_words_table.get_collection(),
    #                                   preteatment.get_collection())
    preteatment.said_temp(preteatment.get_collection())
    pass