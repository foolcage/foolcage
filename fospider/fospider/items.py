# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DownloadInfoItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_path = scrapy.Field()
    request_header = scrapy.Field()


class SecurityItem(scrapy.Item):
    code = scrapy.Field()
    exchange = scrapy.Field()
    type = scrapy.Field()
