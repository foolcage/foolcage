from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from fospider.spiders.download_spider import DownloadSpider

# download_files_info = {
#     "from_url":
# }
process = CrawlerProcess(get_project_settings())

process.crawl("download")
process.start()  # the script will block here until the crawling is finished
