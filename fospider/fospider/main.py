from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from fospider.items import DownloadInfoItem

download_info_items = [DownloadInfoItem(file_urls=[
    'http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1'],
    file_path='sh.xlsx',
    request_header={
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
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"})]

for item in download_info_items:
    settings = get_project_settings()
    settings.set('download_info_item', item)
    settings.set('DEFAULT_REQUEST_HEADERS', item.get('request_header'))
    process = CrawlerProcess(settings)
    process.crawl("download")
    process.start()  # the script will block here until the crawling is finished
