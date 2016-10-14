# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy import Request

from fospider.utils import get_security_item, db_insert_security


class GetFilesPipeline(object):
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        path = item['path']
        if path and os.path.exists(path):
            for item in get_security_item(path):
                print(item)
                db_insert_security(dict(item))
        return item

        self.crawler.engine.crawl(
            Request(
                url='someurl',
                callback=self.custom_callback,
            ),
            spider,
        )

        # you have to drop the item, and send it again after your check
        raise DropItem()

    # YES, you can define a method callback inside the same pipeline
    def custom_callback(self, response):
        yield item
