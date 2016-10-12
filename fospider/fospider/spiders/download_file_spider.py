import os

import scrapy
from scrapy import Request

from fospider.utils import chrome_copy_header_to_dict, get_security_item, rethinkdb_insert_security_item


class DownloadFileSpider(scrapy.Spider):
    name = "download_file"
    custom_settings = {
        "ITEM_PIPELINES": {'fospider.pipelines.GetFilesPipeline': 1},
        "DOWNLOADER_MIDDLEWARES": {
            'fospider.middlewares.GetFileMiddleware': 1,
        }}
    download_info = {
        # 上海A股列表
        'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1': {
            'path': 'sh.txt',
            'header': chrome_copy_header_to_dict('''
                    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
                    Accept-Encoding:gzip, deflate, sdch
                    Accept-Language:zh-CN,zh;q=0.8,en;q=0.6
                    Connection:keep-alive
                    Cookie:PHPStat_First_Time_10000011=1464572600205; PHPStat_Cookie_Global_User_Id=_ck16053009432012139947369251193; PHPStat_Main_Website_10000011=_ck16053009432012139947369251193%7C10000011%7C%7C%7C; VISITED_STOCK_CODE=%5B%22600272%22%5D; VISITED_COMPANY_CODE=%5B%22600272%22%5D; seecookie=%5B600272%5D%3A%u5F00%u5F00%u5B9E%u4E1A; PHPStat_Return_Count_10000011=3; PHPStat_Return_Time_10000011=1476152548261; _trs_uv=1j7y_532_itpgj4e2; VISITED_MENU=%5B%228482%22%2C%228530%22%2C%228529%22%2C%228453%22%2C%228454%22%2C%228464%22%2C%228466%22%2C%228469%22%2C%228451%22%2C%228528%22%5D
                    Host:query.sse.com.cn
                    Referer:http://www.sse.com.cn/assortment/stock/list/share/
                    Upgrade-Insecure-Requests:1
                    User-Agent:Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36
            ''')},
        # 深圳A股列表
        'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENUM=1&ENCODE=1&TABKEY=tab1': {
            'path': 'sz.xlsx',
            'header': chrome_copy_header_to_dict('''
                    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
                    Accept-Encoding:gzip, deflate, sdch
                    Accept-Language:zh-CN,zh;q=0.8,en;q=0.6
                    Connection:keep-alive
                    Host:www.szse.cn
                    Referer:http://www.szse.cn/main/marketdata/jypz/colist/
                    Upgrade-Insecure-Requests:1
                    User-Agent:Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36
                ''')}
    }
    start_urls = [
        'http://www.fakeurl.com']

    def parse(self, response):
        for url in self.download_info.keys():
            yield Request(url, headers=self.download_info.get(url).get('header'), callback=self.download_file)

    def download_file(self, response):
        path = os.path.join(self.settings.get('FILES_STORE'), self.download_info.get(response.url).get('path'))
        with open(path, "wb") as f:
            f.write(response.body)
            for item in get_security_item(path):
                print(item)
                rethinkdb_insert_security_item(dict(item))
