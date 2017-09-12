from elasticsearch_dsl import DocType, Keyword, Date, Text, Float


class Forecast(DocType):
    id = Keyword()
    securityId = Keyword()
    reportDate = Date()
    reportPeriod = Date()
    type = Keyword()
    description = Text()
    preEPS = Float()
    min = Float()
    max = Float()
