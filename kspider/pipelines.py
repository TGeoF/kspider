# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from kspider.items import MatchItem, EventItem
import pymongo


class CleanupPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MatchItem):
            return self.cleanupMatch(item, spider)
        if isinstance(item, EventItem):
            return self.cleanupEvent(item, spider)

    def cleanupEvent(self, event, spider):
        return event

    def cleanupMatch(self, match, spider):
        return match


class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        passwd = input("MongoAtlas pw:\n")
        self.mongo_uri = 'mongodb+srv://tom:{}@cluster0-v5e6v.mongodb.net/test?retryWrites=true&w=majority'.format(
            passwd)
        self.mongo_db = 'Fussballdaten'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MatchItem):
            collection_name = 'matches'
        if isinstance(item, EventItem):
            collection_name = 'events'

        self.db[collection_name].insert_one(dict(item))
        return item
