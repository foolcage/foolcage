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
    code_id = scrapy.Field()
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


class KDataItem(scrapy.Item):
    security_code = scrapy.Field()
    open = scrapy.Field()
    close = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()
    high = scrapy.Field()
    volume = scrapy.Field()
    turnover = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    fuquan = scrapy.Field()


class SectorItem(scrapy.Item):
    start_date = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    producer = scrapy.Field()
    news_title = scrapy.Field()
    news_link = scrapy.Field()
    count = scrapy.Field()
    leadings = scrapy.Field()
