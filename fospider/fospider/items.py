# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecurityItem(scrapy.Item):
    code = scrapy.Field()
    exchange = scrapy.Field()
    type = scrapy.Field()
