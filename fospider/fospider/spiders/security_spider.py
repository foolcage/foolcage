import scrapy

from fospider.items import FiledownloadItem


class SecuritySpider(scrapy.Spider):
    name = "security"
    custom_settings = {
        "ITEM_PIPELINES": {'fospider.pipelines.FoFilesPipeline': 1},
        "FILES_STORE": './',
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "PHPStat_First_Time_10000011=1475418900925; PHPStat_Cookie_Global_User_Id=_ck16100222350019435800313791251; PHPStat_Return_Time_10000011=1475418900925; PHPStat_Main_Website_10000011=_ck16100222350019435800313791251%7C10000011%7C%7C%7C; _trs_uv=7fhg_532_itsqbi56; VISITED_MENU=%5B%228528%22%5D",
            "Host": "query.sse.com.cn",
            "Pragma": "no-cache",
            "Referer": "http://www.sse.com.cn/assortment/stock/list/share/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"}}

    start_urls = [
        'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1']

    def parse(self, response):
        yield FiledownloadItem(
            file_urls=[
                'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1',
                'http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab2PAGENUM=1&ENCODE=1&TABKEY=tab2']
        )
