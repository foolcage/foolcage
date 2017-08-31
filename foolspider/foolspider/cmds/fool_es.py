import logging

from elasticsearch_dsl import Index

from foolspider.domain.finance import BalanceSheet, IncomeStatement, CashFlowStatement
from foolspider.domain.meta import StockMeta
from foolspider.domain.technical import KdataDay
from foolspider.utils.finance_utils import get_balance_sheet_items, get_income_statement_items, \
    get_cash_flow_statement_items
from foolspider.utils.utils import get_security_items, get_kdata_items, fill_doc_type

logger = logging.getLogger(__name__)


def security_meta_to_es():
    for item in get_security_items():
        try:
            stock_meta = StockMeta(meta={'id': item['id']}, id=item['id'], type=item['type'],
                                   exchange=item['exchange'], code=item['code'], listDate=item['listDate'],
                                   name=item['name']);
            stock_meta.save()
        except Exception as e:
            logger.warn("wrong SecurityItem:{},error:{}", item, e)


def kdata_to_es():
    for security_item in get_security_items():
        # 创建索引
        index = Index(security_item['id'] + "_technical")
        index.doc_type(KdataDay)
        index.create()
        for kdata_json in get_kdata_items(security_item):
            try:
                kdata_item = KdataDay(
                    meta={'id': '{}_{}'.format(kdata_json['securityId'], kdata_json['timestamp'])},
                    securityId=kdata_json['securityId'], type=kdata_json['type'],
                    code=kdata_json['code'],
                    open=kdata_json['open'], close=kdata_json['close'], high=kdata_json['high'],
                    low=kdata_json['low'], volume=kdata_json['volume'], turnover=kdata_json['turnover'],
                    timestamp=kdata_json['timestamp'], level=kdata_json['level'])
                kdata_item.save()
            except Exception as e:
                logger.warn("wrong DayKdata:{},error:{}", kdata_item, e)


def balance_sheet_to_es():
    for security_item in get_security_items():
        for json_object in get_balance_sheet_items(security_item):
            try:
                balance_sheet = BalanceSheet(
                    meta={'id': '{}_{}'.format(json_object['securityId'], json_object['reportDate'])});
                fill_doc_type(balance_sheet, json_object)
                balance_sheet.save()
            except Exception as e:
                logger.warn("wrong BalanceSheet:{},error:{}", json_object, e)


def income_statement_to_es():
    for security_item in get_security_items():
        for json_object in get_income_statement_items(security_item):
            try:
                income_statement = IncomeStatement(
                    meta={'id': '{}_{}'.format(json_object['securityId'], json_object['reportDate'])});
                fill_doc_type(income_statement, json_object)
                income_statement.save()
            except Exception as e:
                logger.warn("wrong IncomeStatement:{},error:{}", json_object, e)


def cash_flow_statement_to_es():
    for security_item in get_security_items():
        for json_object in get_cash_flow_statement_items(security_item):
            try:
                cash_flow_statement = CashFlowStatement(
                    meta={'id': '{}_{}'.format(json_object['securityId'], json_object['reportDate'])});
                fill_doc_type(cash_flow_statement, json_object)
                cash_flow_statement.save()
            except Exception as e:
                logger.warn("wrong CashFlowStatement:{},error:{}", json_object, e)


if __name__ == '__main__':
    from elasticsearch_dsl.connections import connections

    connections.create_connection(hosts=['localhost'], timeout=20)
    balance_sheet_to_es()
    income_statement_to_es()
    cash_flow_statement_to_es()
