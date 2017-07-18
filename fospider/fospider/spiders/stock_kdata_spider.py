import datetime
import json
import os

import scrapy
from kafka import KafkaProducer
from scrapy import Request
from scrapy import Selector
from scrapy import signals

from fospider import settings
from fospider.consts import DEFAULT_KDATA_HEADER, DEFAULT_SH_HEADER, DEFAULT_SZ_HEADER
from fospider.items import KDataItem
from fospider.settings import KAFKA_HOST
from fospider.utils.utils import get_security_item, get_quarters, mkdir_for_security, get_year_quarter, \
    get_sh_stock_list_path, get_sz_stock_list_path, get_kdata_path


# TODO:check whether has new stock and new trading date to ignore download again
class StockKDataSpider(scrapy.Spider):
    name = "stock_kdata"
    custom_settings = {
        "ITEM_PIPELINES": {'fospider.pipelines.GetFilesPipeline': 1}}
    producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

    def start_requests(self):
        yield Request(
            url='http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1',
            headers=DEFAULT_SH_HEADER,
            meta={'path': get_sh_stock_list_path()},
            callback=self.download_stock_list)

        yield Request(
            url='http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1',
            headers=DEFAULT_SZ_HEADER,
            meta={'path': get_sz_stock_list_path()},
            callback=self.download_stock_list)

    def download_stock_list(self, response):
        path = response.meta['path']
        with open(path, "wb") as f:
            f.write(response.body)
            for item in get_security_item(path):
                mkdir_for_security(item['code'], item['type'])

                current_year, current_quarter = get_year_quarter(datetime.date.today())
                # get day k data
                for year, quarter in get_quarters(item['listDate']):
                    data_path = get_kdata_path(item['code'], item['type'], year, quarter)
                    # dont't download again if exist and not current
                    if (current_quarter != quarter or current_year != year) \
                            and os.path.isfile(data_path) and not settings.FORCE_DOWNLOAD_KDATA:
                        continue

                    url = self.get_k_data_url(item['code'], year, quarter)
                    yield Request(url=url, headers=DEFAULT_KDATA_HEADER,
                                  meta={'path': data_path, 'code': item['code'], 'exchange': item['exchange']},
                                  callback=self.download_day_k_data)
                    # yield item

    def download_day_k_data(self, response):
        path = response.meta['path']
        code_id = response.meta['code']
        security_id = "stock" + "_" + response.meta['exchange'] + "_" + code_id
        trs = response.xpath('//*[@id="FundHoldSharesTable"]/tr[position()>1 and position()<=last()]').extract()

        kdata_json = []

        try:
            for tr in trs:
                tds = Selector(text=tr).xpath('//td//text()').extract()
                tds = [x.strip() for x in tds if x.strip()]
                item = KDataItem(securityId=security_id, code=code_id, timestamp=tds[0], open=tds[1], high=tds[2],
                                 close=tds[3], low=tds[4], volume=tds[5], turnover=tds[6], fuquan=tds[7], type='stock',
                                 level='DAY')
                kdata_json.append(dict(item))
                self.producer.send('CHINA_STOCK_KDATA_DAY',
                                   bytes(json.dumps(dict(item), ensure_ascii=False), encoding='utf8'))

                # yield item
        except Exception as e:
            self.logger.error('error when getting k data url={} error={}'.format(response.url, e))

        try:
            with open(path, "x") as f:
                json.dump(kdata_json, f)
        except FileExistsError:
            pass
        except Exception as e:
            self.logger.error('error when saving k data url={} path={} error={}'.format(response.url, path, e))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StockKDataSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s,%s', spider.name, reason)

    def get_k_data_url(self, code, year, quarter):
        return 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/{}.phtml?year={}&jidu={}'.format(
            code, year, quarter)
