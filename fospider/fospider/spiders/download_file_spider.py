import datetime
import json
import os

import scrapy
from scrapy import Request
from scrapy import Selector
from scrapy import signals

from fospider import settings
from fospider.consts import DEFAULT_KDATA_HEADER, DEFAULT_SH_HEADER, DEFAULT_SZ_HEADER
from fospider.items import KDataItem
from fospider.utils.utils import get_security_item, get_quarters, mkdir_for_security, get_kdata_dir, get_year_quarter


class DownloadFileSpider(scrapy.Spider):
    name = "download_file"
    custom_settings = {
        "ITEM_PIPELINES": {'fospider.pipelines.GetFilesPipeline': 1},
        "DOWNLOADER_MIDDLEWARES": {
            'fospider.middlewares.GetFileMiddleware': 1,
        }}
    security_download_info = {
        # 上海A股列表
        'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1': {
            'path': os.path.join(settings.FILES_STORE, settings.SH_STOCK_FILE),
            'header': DEFAULT_SH_HEADER},
        # 深圳A股列表
        'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1': {
            'path': os.path.join(settings.FILES_STORE, settings.SZ_STOCK_FILE),
            'header': DEFAULT_SZ_HEADER}
    }
    start_urls = [
        'http://www.fakeurl.com']

    def parse(self, response):
        for url in self.security_download_info.keys():
            yield Request(url, headers=self.security_download_info.get(url).get('header'),
                          callback=self.download_stock_list)

    def download_day_k_data(self, response):
        path = self.security_download_info.get(response.url).get('path')

        code_id = self.security_download_info.get(response.url).get('code_id')
        trs = response.xpath('//*[@id="FundHoldSharesTable"]/tr[position()>1 and position()<=last()]').extract()

        kdata_json = []

        try:
            for tr in trs:
                tds = Selector(text=tr).xpath('//td//text()').extract()
                tds = [x.strip() for x in tds if x.strip()]
                item = KDataItem(security_code=code_id, time=tds[0], open=tds[1], high=tds[2], close=tds[3],
                                 low=tds[4],
                                 volume=tds[5], turnover=tds[6], fuquan=tds[7], type='stock')
                kdata_json.append(dict(item))
                # yield item
        except Exception as e:
            self.logger.error('error when parsing k data from {}'.format(response.url))
            self.logger.error(e)

        try:
            with open(path, "x") as f:
                json.dump(kdata_json, f)
        except FileExistsError:
            pass
        except Exception as e:
            self.logger.error('error when saving k data url:{} path:{}'.format(response.url, path))

    def download_stock_list(self, response):
        path = self.security_download_info.get(response.url).get('path')
        with open(path, "wb") as f:
            f.write(response.body)
            for item in get_security_item(path):
                mkdir_for_security(item['code_id'], item['type'])

                current_year, current_quarter = get_year_quarter(datetime.date.today())
                # get day k data
                for year, quarter in get_quarters(item['list_date']):
                    data_path = os.path.join(get_kdata_dir(item['code_id'], item['type']),
                                             '{}-{}-d.json'.format(year, quarter))
                    # dont't download again if exist and not current
                    if (current_quarter != quarter or current_year != current_year) \
                            and os.path.isfile(data_path) and not settings.FORCE_DOWNLOAD_KDATA:
                        continue

                    url = self.get_k_data_url(item['code'], year, quarter)
                    self.security_download_info[url] = {
                        'path': data_path,
                        'header': DEFAULT_KDATA_HEADER,
                        'code_id': item['code_id']}
                    yield Request(url, headers=self.security_download_info.get(url).get('header'),
                                  callback=self.download_day_k_data)
                    yield item

                    # url = self.get_tick_url(item['list_date'], item['code'])
                    # self.security_download_info[url] = {'path': item['code'] + "_" + item['list_date'] + ".xls",
                    #                                     'header': DEFAULT_TICK_HEADER}
                    #
                    # yield Request(url, headers=self.security_download_info.get(url).get('header'),
                    #               callback=self.download_file)

                    # path = os.path.join(self.settings.get('FILES_STORE'), 'ticks', path)
                    # with open(path, "wb") as f:
                    #     f.write(response.body)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(DownloadFileSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s,%s', spider.name, reason)

    def get_tick_url(self, date, code):
        return 'http://market.finance.sina.com.cn/downxls.php?date={}&symbol={}'.format(date, code)

    def get_k_data_url(self, code, year, quarter):
        return 'http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/{}.phtml?year={}&jidu={}'.format(
            code, year, quarter)
