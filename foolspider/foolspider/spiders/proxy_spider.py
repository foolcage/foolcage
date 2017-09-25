import json

import scrapy
from scrapy import Request
from scrapy import Selector
from scrapy import signals

from foolspider.consts import HIDEME_NAME_HEADER
from foolspider.proxy.proxy_manager import g_socks2http_proxy_items
from foolspider.utils.utils import get_forecast_event_path


class ProxySpider(scrapy.Spider):
    name = "proxy"

    def start_requests(self):
        url = self.get_proxy_url(0)
        meta = {}
        if g_socks2http_proxy_items.get('127.0.0.1:1081'):
            meta['proxy'] = g_socks2http_proxy_items['127.0.0.1:1081']
        yield Request(url=url,
                      headers=HIDEME_NAME_HEADER,
                      meta={'proxy': 'http://127.0.0.1:10000'},
                      callback=self.download_proxy_data)

    def download_proxy_data(self, response):
        security_item = response.meta['item']
        trs = response.xpath('//*[@id="dataTable"]//tr').extract()

        forecast_jsons = []

        try:
            for tr in trs[1:]:
                tds = Selector(text=tr).xpath('//td//text()').extract()
                tds = [x.strip() for x in tds if x.strip()]

                # 业绩变动字符串转为float
                change_str = tds[7]
                change_start = None

                if '~' in change_str:
                    i = change_str.index('~')
                    change_start = change_str[0:i]
                    change = change_str[i + 1:]
                else:
                    change = change_str

                if change:
                    change = change.strip('%')
                    change = float(change) / 100
                if change_start:
                    change_start = change_start.strip('%')
                    change_start = float(change_start) / 100

                # preEPS可能为空
                preEPS = None
                try:
                    preEPS = float(tds[6])
                except Exception as e:
                    pass

                json_item = {"id": '{}_{}'.format(security_item['id'], tds[3]),
                             "securityId": security_item['id'],
                             "reportDate": tds[3],
                             "reportPeriod": tds[4],
                             "type": tds[2],
                             "description": tds[5],
                             "preEPS": preEPS,
                             "changeStart": change_start,
                             "change": change,
                             }
                forecast_jsons.append(json_item)

            if forecast_jsons:
                try:
                    with open(get_forecast_event_path(security_item), "w") as f:
                        json.dump(forecast_jsons, f, ensure_ascii=False)
                except Exception as e:
                    self.logger.error(
                        'error when saving forecast url={} path={} error={}'.format(response.url,
                                                                                    get_forecast_event_path(
                                                                                        security_item), e))



        except Exception as e:
            self.logger.error('error when getting k data url={} error={}'.format(response.url, e))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ProxySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s,%s\n', spider.name, reason)

    def get_proxy_url(self, position):
        return 'https://hidemy.name/en/proxy-list/?start={}#list'.format(
            position)
