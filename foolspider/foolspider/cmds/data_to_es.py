import json
import logging
import os

from elasticsearch_dsl import Index

from foolspider.domain.KData import DayKdata
from foolspider.domain.stock_meta import StockMeta, KDataDayItem
from foolspider.utils.utils import get_sh_stock_list_path, get_sz_stock_list_path, get_security_item, get_kdata_dir, \
    get_security_items

logger = logging.getLogger(__name__)


def security_item_to_es():
    stock_files = (get_sh_stock_list_path(), get_sz_stock_list_path())
    for stock_file in stock_files:
        for item in get_security_item(stock_file):
            try:
                stock_meta = StockMeta(meta={'id': item['id']}, id=item['id'], type=item['type'],
                                       exchange=item['exchange'], code=item['code'], listDate=item['listDate'],
                                       name=item['name']);
                stock_meta.save()
            except Exception as e:
                logger.warn("wrong SecurityItem:{},error:{}", item, e)


def kdata_item_to_es():
    for item in get_security_items():
        try:
            dir = get_kdata_dir(item)
            if os.path.exists(dir):
                files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

                for f in files:
                    with open(f) as data_file:
                        kdata_jsons = json.load(data_file)
                        for kdata_json in kdata_jsons:
                            kdata_item = DayKdata(
                                meta={'id': '{}_{}'.format(kdata_json['securityId'], kdata_json['timestamp'])},
                                securityId=kdata_json['securityId'], type=kdata_json['type'],
                                code=kdata_json['code'],
                                open=kdata_json['open'], close=kdata_json['close'], high=kdata_json['high'],
                                low=kdata_json['low'], volume=kdata_json['volume'], turnover=kdata_json['turnover'],
                                timestamp=kdata_json['timestamp'], level=kdata_json['level'])
                            kdata_item.save()

        except Exception as e:
            logger.warn("wrong SecurityItem:{},error:{}", item, e)


if __name__ == '__main__':
    from elasticsearch_dsl.connections import connections

    connections.create_connection(hosts=['localhost'], timeout=20)
    blogs = Index('blogs')
    # StockMeta.init()
    # security_item_to_es()
    KDataDayItem.init()
    kdata_item_to_es()
