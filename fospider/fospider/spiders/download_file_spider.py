import json
import os

import scrapy
from scrapy import Request
from scrapy import Selector
from scrapy import signals

from fospider import settings
from fospider.consts import DEFAULT_KDATA_HEADER, DEFAULT_SH_HEADER, DEFAULT_SZ_HEADER
from fospider.items import KDataItem
from fospider.utils import get_security_item, get_quarters


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
            yield Request(url, headers=self.security_download_info.get(url).get('header'), callback=self.download_file)

    def download_file(self, response):
        path = self.security_download_info.get(response.url).get('path')
        if path.endswith(settings.SZ_STOCK_FILE) or path.endswith(settings.SH_STOCK_FILE):
            with open(path, "wb") as f:
                f.write(response.body)
                for item in get_security_item(path):
                    # get day k data
                    for year, quarter in get_quarters(item['list_date']):
                        url = self.get_k_data_url(item['code'], year, quarter)
                        self.security_download_info[url] = {
                            'path': os.path.join(settings.FILES_STORE, item['code_id'],
                                                 '{}-{}-d.json'.format(year, quarter)),
                            'header': DEFAULT_KDATA_HEADER,
                            'code_id': item['code_id']}

                        yield Request(url, headers=self.security_download_info.get(url).get('header'),
                                      callback=self.download_file)
                        yield item

                        # url = self.get_tick_url(item['list_date'], item['code'])
                        # self.security_download_info[url] = {'path': item['code'] + "_" + item['list_date'] + ".xls",
                        #                                     'header': DEFAULT_TICK_HEADER}
                        #
                        # yield Request(url, headers=self.security_download_info.get(url).get('header'),
                        #               callback=self.download_file)
        elif path.endswith('-d.json'):
            # parse k data
            # '\r\n\t\t\t\r\n\t\t',
            # '\r\n\t\t\t\t\t2007-04-30\t\t\t\t\t\t',
            # '\r\n\t\t\t\t\t\t',
            # '70.000',
            # '71.000',
            # '64.930',
            # '62.880',
            # '20737497.000',
            # '1365189211.000',
            # '1.000'

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
                print(e)
            try:
                if not os.path.exists('data/{}'.format(code_id)):
                    os.makedirs('data/{}'.format(code_id))
                with open(path, "w") as f:
                    json.dump(kdata_json, f)
                    f.flush()
            except Exception as e:
                print(e)

        else:
            pass
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
