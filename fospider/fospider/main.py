from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from twisted.internet import reactor

from fospider.spiders.stock_gn_spider import StockGNSpider
from fospider.utils.utils import setup_env

setup_env()

configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(StockKDataSpider)
    # yield runner.crawl(StockTickSpider)
    yield runner.crawl(StockGNSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
