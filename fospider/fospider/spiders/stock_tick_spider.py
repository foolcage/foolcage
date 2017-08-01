import itertools
import json
import os

import scrapy
from kafka import KafkaProducer
from scrapy import Request
from scrapy import signals

from fospider import settings
from fospider.consts import DEFAULT_TICK_HEADER
from fospider.settings import KAFKA_HOST, AUTO_KAFKA, STOCK_START_CODE, STOCK_END_CODE
from fospider.utils.utils import get_security_item, get_sh_stock_list_path, get_trading_dates, get_tick_path, \
    is_available_tick, get_sz_stock_list_path, get_datetime, get_tick_item


# TODO:add start/end date/stocks setting for download ticks
class StockTickSpider(scrapy.Spider):
    name = "stock_tick"
    if AUTO_KAFKA:
        producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

    def start_requests(self):
        for item in itertools.chain(get_security_item(get_sh_stock_list_path()),
                                    get_security_item(get_sz_stock_list_path())):
            if STOCK_START_CODE <= item['code'] <= STOCK_END_CODE:
                for trading_date in get_trading_dates(item):
                    if get_datetime(trading_date) < get_datetime(settings.START_TICK_DATE) or get_datetime(
                            trading_date) < get_datetime(settings.AVAILABLE_TICK_DATE):
                        continue
                    path = get_tick_path(item, trading_date)

                    if os.path.isfile(path) and is_available_tick(path):
                        continue

                    yield Request(url=self.get_tick_url(trading_date, item['exchange'] + item['code']),
                                  meta={'path': path,
                                        'trading_date': trading_date,
                                        'item': item},
                                  headers=DEFAULT_TICK_HEADER,
                                  callback=self.download_tick)

    def download_tick(self, response):
        content_type_header = response.headers.get('content-type', None)

        if content_type_header.decode("utf-8") == 'application/vnd.ms-excel':
            path = response.meta['path']
            trading_date = response.meta['trading_date']
            item = response.meta['item']
            with open(path, "wb") as f:
                f.write(response.body)
                f.flush()
                if AUTO_KAFKA:
                    for tick_item in get_tick_item(path, trading_date, item):
                        self.producer.send('CHINA_STOCK_TICK',
                                           bytes(json.dumps(tick_item, ensure_ascii=False), encoding='utf8'))

        else:
            self.logger.error(
                "get tick error:url={} content type={} body={}".format(response.url, content_type_header,
                                                                       response.body))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StockTickSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s,%s', spider.name, reason)

    def get_tick_url(self, date, code):
        return 'http://market.finance.sina.com.cn/downxls.php?date={}&symbol={}'.format(date, code)
