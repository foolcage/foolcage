import itertools

import scrapy
from kafka import KafkaProducer
from scrapy import Request
from scrapy import signals

from foolspider.consts import DEFAULT_BALANCE_SHEET_HEADER
from foolspider.settings import KAFKA_HOST, AUTO_KAFKA, STOCK_START_CODE, STOCK_END_CODE
from foolspider.utils.utils import get_security_item, get_sh_stock_list_path, get_sz_stock_list_path, \
    get_balance_sheet_path, get_income_statement_path, get_cash_flow_statement_path, mkdir_for_security


class StockFinanceSpider(scrapy.Spider):
    name = "stock_finance"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,

        'SPIDER_MIDDLEWARES': {
            'foolspider.middlewares.FoolErrorMiddleware': 1000,
        }
    }

    if AUTO_KAFKA:
        producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

    def start_requests(self):
        for item in itertools.chain(get_security_item(get_sh_stock_list_path()),
                                    get_security_item(get_sz_stock_list_path())):
            if STOCK_START_CODE <= item['code'] <= STOCK_END_CODE:
                mkdir_for_security(item)
                for (data_url, data_path) in (
                        (self.get_balance_sheet_url(item['code']), get_balance_sheet_path(item)),
                        (self.get_income_statement_url(item['code']), get_income_statement_path(item)),
                        (self.get_cash_flow_statement_url(item['code']), get_cash_flow_statement_path(item))):
                    yield Request(url=data_url,
                                  meta={'path': data_path,
                                        'item': item},
                                  headers=DEFAULT_BALANCE_SHEET_HEADER,
                                  callback=self.download_finance_sheet)

    def download_finance_sheet(self, response):
        content_type_header = response.headers.get('content-type', None)

        if content_type_header.decode("utf-8") == 'application/vnd.ms-excel':
            path = response.meta['path']
            item = response.meta['item']
            with open(path, "wb") as f:
                f.write(response.body)
                f.flush()
                if AUTO_KAFKA:
                    # todo: parse the sheet and send it to kafka
                    pass
        else:
            self.logger.error(
                "get finance sheet error:url={} content type={} body={}".format(response.url, content_type_header,
                                                                                response.body))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StockFinanceSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s,%s\n', spider.name, reason)

    def get_balance_sheet_url(self, code):
        return 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/{}/ctrl/all.phtml' \
            .format(code)

    def get_income_statement_url(self, code):
        return 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/{}/ctrl/all.phtml' \
            .format(code)

    def get_cash_flow_statement_url(self, code):
        return 'http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/{}/ctrl/all.phtml' \
            .format(code)
