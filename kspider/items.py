# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EventItem(scrapy.Item):
    l = scrapy.Field()


class MatchItem(scrapy.Item):
    league = scrapy.Field()
    season = scrapy.Field()
    matchday = scrapy.Field()
    matchID = scrapy.Field()
    datetime = scrapy.Field()
    homeTeam = scrapy.Field()
    awayTeam = scrapy.Field()
    homeGoals = scrapy.Field()
    awayGoals = scrapy.Field()
    stadium = scrapy.Field()
    attendance = scrapy.Field()
    referee = scrapy.Field()
