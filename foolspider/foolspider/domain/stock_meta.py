from elasticsearch_dsl import DocType, Keyword, Date, Float
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])


class StockMeta(DocType):
    id = Keyword()
    type = Keyword()
    exchange = Keyword()
    code = Keyword()
    name = Keyword()
    listDate = Date()

    class Meta:
        index = 'security_meta'
        doc_type = 'stock_meta'


class StockTickItem(DocType):
    securityId = Keyword()
    code = Keyword()
    timestamp = Date()
    price = Float()
    change = Float()
    direction = Keyword()
    volume = Float()
    turnover = Float()

    class Meta:
        index = 'stock_tick'

        @property
        def doc_type(self):
            return StockTickItem.securityId


# 后复权
class KDataBackwardDayItem(DocType):
    securityId = Keyword()
    type = Keyword()
    code = Keyword()
    open = Float()
    close = Float()
    high = Float()
    low = Float()
    volume = Float()
    turnover = Float()
    timestamp = Date()
    level = Keyword()
    fuquan = Float()

    class Meta:
        index = 'stock_kdata_backward'
        doc_type = 'day'


# 不复权
class KDataDayItem(DocType):
    securityId = Keyword()
    type = Keyword()
    code = Keyword()
    open = Float()
    close = Float()
    high = Float()
    low = Float()
    volume = Float()
    turnover = Float()
    timestamp = Date()
    level = Keyword()

    class Meta:
        index = 'stock_kdata'
        doc_type = 'day'
