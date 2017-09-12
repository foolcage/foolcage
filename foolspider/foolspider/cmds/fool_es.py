import logging

from elasticsearch_dsl import Index

from foolspider.domain.finance import BalanceSheet, IncomeStatement, CashFlowStatement
from foolspider.domain.meta import StockMeta
from foolspider.domain.technical import KdataDay, KdataDayHoufuquan
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


def kdata_to_es(houfuquan=False):
    for security_item in get_security_items():
        # 创建索引
        index = Index(security_item['id'] + "_technical")
        if houfuquan:
            index.doc_type(KdataDayHoufuquan)
        else:
            index.doc_type(KdataDay)

        if not index.exists():
            index.create()
        else:
            index.upgrade()

        for kdata_json in get_kdata_items(security_item, houfuquan):
            try:
                id = '{}_{}'.format(kdata_json['securityId'], kdata_json['timestamp'])
                if houfuquan:
                    kdata_item = KdataDayHoufuquan(
                        meta={'id': id},
                        id=id)
                else:
                    kdata_item = KdataDay(
                        meta={'id': id},
                        id=id)
                fill_doc_type(kdata_item, kdata_json)
                kdata_item.save()
            except Exception as e:
                logger.warn("wrong KdataDay:{},houfuquan:{},error:{}", kdata_item, houfuquan, e)


def balance_sheet_to_es():
    for security_item in get_security_items():
        for json_object in get_balance_sheet_items(security_item):
            try:
                balance_sheet = BalanceSheet(
                    meta={'id': json_object['id']});
                fill_doc_type(balance_sheet, json_object)
                balance_sheet.save()
            except Exception as e:
                logger.warn("wrong BalanceSheet:{},error:{}", json_object, e)


def income_statement_to_es():
    for security_item in get_security_items():
        for json_object in get_income_statement_items(security_item):
            try:
                income_statement = IncomeStatement(
                    meta={'id': json_object['id']});
                fill_doc_type(income_statement, json_object)
                income_statement.save()
            except Exception as e:
                logger.warn("wrong IncomeStatement:{},error:{}", json_object, e)


def cash_flow_statement_to_es():
    for security_item in get_security_items():
        for json_object in get_cash_flow_statement_items(security_item):
            try:
                cash_flow_statement = CashFlowStatement(
                    meta={'id': json_object['id']});
                fill_doc_type(cash_flow_statement, json_object)
                cash_flow_statement.save()
            except Exception as e:
                logger.warn("wrong CashFlowStatement:{},error:{}", json_object, e)


if __name__ == '__main__':
    from elasticsearch_dsl.connections import connections

    connections.create_connection(hosts=['localhost'], timeout=20)
    # balance_sheet_to_es()
    # income_statement_to_es()
    # cash_flow_statement_to_es()
    kdata_to_es()
