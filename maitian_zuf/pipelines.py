# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from maitian_zuf.items import *


class MaitianZufPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    collection_name = 'maitian'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MaitianZufItem):
            self.db[self.collection_name].update({'zf_url': item.get('zf_url')}, {'$set': item}, True)

        if isinstance(item, MaitianEsItem):
            self.db[self.collection_name].update({'es_url': item.get('es_url')}, {'$set': item}, True)