# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fospider.utils.rethinkdb_utils import db_insert_sector


class GetFilesPipeline(object):
    def process_item(self, item, spider):
        pass
        # db_insert_sector(item)
