# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


#def mongo_uid(dbname, collname):
    

class GaonengfunPipeline(object):
    db_name = 'onepiece'
    collection_name = 'gaonengfun'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'onepiece')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.util = self.client['util']
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        if item.get('title') and item.get('content') and item.get('imgs'):
            ret = self.util.sequence.find_and_modify({'dbname': 'onepiece', 'colname': 'gaonengfun'}, {'$inc': {'seq': 1}}, new=True, fields={'_id': 0, 'seq': 1})
            article = dict(item)
            article.update({'id': ret['seq']})
            article.update({'type': 1})
            self.db[self.collection_name].insert(article)
            return article
