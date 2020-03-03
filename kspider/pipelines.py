# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from kspider.items import MatchItem, EventItem
from api_keys import strapi_server
import re
#import pymongo
import requests


class StrapiPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MatchItem):
            print("FOUND A MATCH")
            API_ENDPOINT = strapi_server + "/matches"
            print(API_ENDPOINT)
            data = {"matchday": item["matchday"],
                    "matchID": item["matchID"],
                    "datetime": item["datetime"],
                    "homeTeam": item["homeTeam"],
                    "awayTeam": item["awayTeam"],
                    "homeGoals": item["homeGoals"],
                    "awayGoals": item["awayGoals"],
                    "stadium": item["stadium"],
                    "attendance": item["attendance"],
                    "referee": item["referee"]}
            response = requests.post(url=API_ENDPOINT, data=data)
            print(response)
        return item


class CleanupPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MatchItem):
            return self.cleanupMatch(item, spider)
        if isinstance(item, EventItem):
            return self.cleanupEvent(item, spider)

    def cleanupEvent(self, item, spider):
        tl = item['eventType']
        print(tl)

        item['team'] = tl[-1]
        item['minute'] = int(re.search('\d{1,2}(?=(\. ))', tl[0]).group())

        try:
            item['extraMinute'] = int(re.search(
                '\d{1,2}(?= Spielminute)', tl[0]).group())
        except:
            item['extraMinute'] = 0

        if re.search(' Karte ', tl[1]):  # Karten
            item['eventType'] = 'card'
            item['player1'] = tl[2]
            item['player2'] = ''
            item['penalty'] = False
            item['ownGoal'] = False
            if re.search('Gelb', tl[1]):
                item['cardColor'] = 'yellow'
            else:
                item['cardColor'] = 'red'
        elif re.search('Spielerwechsel ', tl[1]):  # Auswechslungen
            item['eventType'] = 'substitution'
            item['cardColor'] = ''
            item['player1'] = tl[2]
            item['player2'] = tl[4]
            item['penalty'] = False
            item['ownGoal'] = False
        elif re.search('Tor \d', tl[1]):  # Tore
            item['eventType'] = 'goal'
            item['cardColor'] = ''
            item['player1'] = tl[2]
            if tl[-3] == 'Vorbereitung':
                item['player2'] = tl[-2]
            else:
                item['player2'] = ''
            if re.search('lfmeter', tl[3]):
                item['penalty'] = True
            else:
                item['penalty'] = False
            if re.match('Eigentor', tl[3]):
                item['ownGoal'] = True
            else:
                item['ownGoal'] = False
        else:
            item['eventType'] = 'invalid'
            item['cardColor'] = ''

        return item

    def cleanupMatch(self, item, spider):

        clean_matchday = re.search(
            '\d{1,2}(?=(\. Spieltag))', item['matchday']).group()
        item['matchday'] = int(clean_matchday)

        clean_attendance = ''.join(
            c for c in item['attendance'] if c.isdigit())
        try:
            item['attendance'] = int(clean_attendance)
        except:
            item['attendance'] = 0

        return item


# class MongoDBPipeline(object):

#     # @classmethod
#     # def from_crawler(cls, crawler):
#     #     return cls(
#     #         mongo_uri=crawler.settings.get('MONGO_URI'),
#     #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#     #     )

#     def open_spider(self, spider):
#         user = input("MongoAtlas usr:\n")
#         passwd = input("MongoAtlas pw:\n")
#         self.mongo_uri = 'mongodb+srv://{}:{}@cluster0-v5e6v.mongodb.net/test?retryWrites=true&w=majority'.format(
#             user, passwd)
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[spider.league]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         if isinstance(item, MatchItem):
#             collection_name = 'matches'
#         if isinstance(item, EventItem):
#             collection_name = 'events'

#         self.db[collection_name].insert_one(dict(item))
#         return item
