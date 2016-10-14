# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FileItem(scrapy.Item):
    path = scrapy.Field()


class ExchangeItem(scrapy.Item):
    name = scrapy.Field()
    desc = scrapy.Field()


class SecurityTypeItem(scrapy.Item):
    name = scrapy.Field()


class SecurityItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    list_date = scrapy.Field()
    exchange = scrapy.Field()
    type = scrapy.Field()


class TickItem(scrapy.Item):
    security_id = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    volume = scrapy.Field()
    turnover = scrapy.Field()
