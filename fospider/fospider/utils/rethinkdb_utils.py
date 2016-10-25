# database info
import logging
import os

from rethinkdb import r, json

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015

FOOLCAGE_DB = 'foolcage'

TABLE_EXCHANGE = 'exchange'
TABLE_SECURITY = 'security'
TABLE_TICK = 'tick'
TABLE_SECTOR = 'sector'
TABLE_STOCK_SECTOR = 'stock_sector'

SECURITY_TYPES = ('stock', 'future')

conn = None

logger = logging.getLogger('rethinkdb')


def table_exist(conn, name):
    return name in r.db(FOOLCAGE_DB).table_list().run(conn)


def create_tables(conn):
    if not table_exist(conn, TABLE_EXCHANGE):
        r.db(FOOLCAGE_DB).table_create(TABLE_EXCHANGE).run(conn)
    if not table_exist(conn, TABLE_SECURITY):
        r.db(FOOLCAGE_DB).table_create(TABLE_SECURITY, primary_key='code_id').run(conn)
    if not table_exist(conn, TABLE_TICK):
        r.db(FOOLCAGE_DB).table_create(TABLE_TICK).run(conn)
    if not table_exist(conn, TABLE_SECTOR):
        r.db(FOOLCAGE_DB).table_create(TABLE_SECTOR).run(conn)
    if not table_exist(conn, TABLE_STOCK_SECTOR):
        r.db(FOOLCAGE_DB).table_create(TABLE_STOCK_SECTOR).run(conn)


def db_setup():
    global conn
    try:
        conn = r.connect(host=RDB_HOST, port=RDB_PORT)

        if not FOOLCAGE_DB in r.db_list().run(conn):
            r.db_create(FOOLCAGE_DB).run(conn)
        create_tables(conn)
    except r.ReqlDriverError or r.ReqlDriverError as error:
        logger.error(error.message)


def db_insert_stock_sector(item):
    try:
        r.db(FOOLCAGE_DB).table(TABLE_STOCK_SECTOR).insert(item, conflict="error").run(conn)
    except r.RqlRuntimeError as err:
        logger.error(err.message)


def db_insert_sector(item):
    try:
        r.db(FOOLCAGE_DB).table(TABLE_SECTOR).insert(item, conflict="error").run(conn)
    except r.RqlRuntimeError as err:
        logger.error(err.message)


def db_get_securities():
    selection = list(r.table(TABLE_SECURITY).run(conn))
    return json.dumps(selection)


def db_insert_security(item):
    try:
        r.db(FOOLCAGE_DB).table(TABLE_SECURITY).insert(item, conflict="error").run(conn)
    except r.RqlRuntimeError as err:
        logger.error(err.message)
