import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from fospider.utils import db_setup

if not os.path.exists('data/ticks'):
    os.makedirs('data/ticks')
db_setup()
settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl("download_file")
process.start()  # the script will block here until the crawling is finished
