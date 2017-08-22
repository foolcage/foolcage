from elasticsearch_dsl import DocType, Keyword, Date, Float
from elasticsearch_dsl import Index
from elasticsearch_dsl import MetaField


# 不复权
class BaseKData(DocType):
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


class DayKdata(BaseKData):
    class Meta:
        all = MetaField(enabled=False)
