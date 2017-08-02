from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from twisted.internet import reactor

from fospider.spiders.stock_finance_spider import StockFinanceSpider
from fospider.spiders.stock_kdata_spider import StockKDataSpider
from fospider.spiders.stock_tick_spider import StockTickSpider
from fospider.utils.utils import setup_env

configure_logging()

setup_env()

runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(SecurityListSpider)
    # yield runner.crawl(StockKDataSpider)

    # yield runner.crawl(StockTickSpider)
    yield runner.crawl(StockFinanceSpider)
    # yield runner.crawl(StockGNSpider)

    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
