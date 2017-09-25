from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from twisted.internet import reactor

from foolspider.proxy.proxy_manager import int_proxy
from foolspider.spiders.proxy_spider import ProxySpider
from foolspider.spiders.security_list_spider import SecurityListSpider
from foolspider.spiders.stock_finance_spider import StockFinanceSpider
from foolspider.spiders.stock_forecast_spider import StockForecastSpider
from foolspider.spiders.stock_kdata_spider import StockKDataSpider
from foolspider.spiders.stock_tick_spider import StockTickSpider
from foolspider.utils.utils import setup_env

configure_logging()

setup_env()

int_proxy()

runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    # yield runner.crawl(SecurityListSpider)
    # yield runner.crawl(StockKDataSpider)

    yield runner.crawl(StockTickSpider)
    # yield runner.crawl(StockFinanceSpider)
    # yield runner.crawl(StockGNSpider)
    # yield runner.crawl(StockForecastSpider)
    # yield runner.crawl(ProxySpider)

    reactor.stop()


crawl()

reactor.run()  # the script will block here until the last crawl call is finished
