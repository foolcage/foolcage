from elasticsearch_dsl import DocType, Keyword, Date, Text, Float
from elasticsearch_dsl import MetaField


class ForecastEvent(DocType):
    id = Keyword()
    securityId = Keyword()
    reportDate = Date()
    reportPeriod = Date()
    type = Keyword()
    description = Text()
    preEPS = Float()
    changeStart = Float()
    change = Float()

    class Meta:
        all = MetaField(enabled=False)
