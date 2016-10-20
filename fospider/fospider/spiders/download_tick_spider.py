import itertools
import os

import scrapy
from scrapy import Request
from scrapy import signals

from fospider import settings
from fospider.consts import DEFAULT_TICK_HEADER
from fospider.utils.utils import get_security_item, get_sh_stock_list_path, get_trading_dates, get_tick_path, \
    is_available_tick, get_sz_stock_list_path


class DownloadTickSpider(scrapy.Spider):
    name = "download_tick"
    custom_settings = {
        'ITEM_PIPELINES': {'fospider.pipelines.GetFilesPipeline': 1},
        'DEFAULT_REQUEST_HEADERS': DEFAULT_TICK_HEADER}
    request_infos = {
    }

    def start_requests(self):
        for item in itertools.chain(get_security_item(get_sh_stock_list_path()),
                                    get_security_item(get_sz_stock_list_path())):
            for trading_date in get_trading_dates(item['code_id'], item['type']):
                if trading_date < settings.START_TICK_DATE or trading_date < settings.AVAILABLE_TICK_DATE:
                    continue
                path = get_tick_path(item['code_id'], item['type'], trading_date)

                if os.path.isfile(path) and is_available_tick(path):
                    continue

                url = self.get_tick_url(trading_date, item['code_id'])
                self.request_infos[url] = {'path': path}

                yield Request(url, callback=self.download_file)

    def download_file(self, response):
        content_type_header = response.headers.get('content-type', None)

        if content_type_header.decode("utf-8") == 'application/vnd.ms-excel':
            path = self.request_infos.get(response.url).get('path')
            with open(path, "wb") as f:
                f.write(response.body)
        else:
            self.logger.error("wrong content type:{}".format(content_type_header))
            self.logger.error("body:{}".format(response.body))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DownloadTickSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s,%s', spider.name, reason)

    def get_tick_url(self, date, code):
        return 'http://market.finance.sina.com.cn/downxls.php?date={}&symbol={}'.format(date, code)
