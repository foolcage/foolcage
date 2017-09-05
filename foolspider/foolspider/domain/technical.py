from elasticsearch_dsl import DocType, Keyword, Date, Float
from elasticsearch_dsl import MetaField


# 不复权
class BaseKData(DocType):
    id = Keyword()
    securityId = Keyword()
    timestamp = Date()
    type = Keyword()
    code = Keyword()
    level = Keyword()
    fuquan = Float()

    open = Float()
    close = Float()
    high = Float()
    low = Float()
    volume = Float()
    turnover = Float()


class KdataDay(BaseKData):
    class Meta:
        all = MetaField(enabled=False)


class KdataDayHoufuquan(BaseKData):
    class Meta:
        all = MetaField(enabled=False)
