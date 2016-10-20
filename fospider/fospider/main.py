from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from fospider.utils.utils import setup_env

setup_env()

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl("download_file")
process.start()  # the script will block here until the crawling is finished
