# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class T58AgentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    agentname   = scrapy.Field()
    source      = scrapy.Field()
    sourceurl   = scrapy.Field()

class T58PositionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionname = scrapy.Field()
    positionurl  = scrapy.Field()
    salary       = scrapy.Field()
    location     = scrapy.Field()
    education    = scrapy.Field()
    experience   = scrapy.Field()
    headcount    = scrapy.Field()
    updatetime   = scrapy.Field()
    agenturl     = scrapy.Field()


