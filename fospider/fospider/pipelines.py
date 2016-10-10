# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline


class FospiderPipeline(object):
    def process_item(self, item, spider):
        return item


class FoFilesPipeline(FilesPipeline):
    custom_file_path = None

    def __init__(self, store_uri, download_func=None, settings=None):
        self.custom_file_path = settings.get('download_info_item').get('file_path')
        super(FoFilesPipeline, self).__init__(store_uri, download_func, settings)

    def file_path(self, request, response=None, info=None):
        if self.custom_file_path:
            return self.custom_file_path
        else:
            return super().file_path(request, response, info)
