import datetime
import json
import os

import openpyxl

from fospider import settings
from fospider.items import SecurityItem
from fospider.utils.rethinkdb_utils import db_setup


def chrome_copy_header_to_dict(src):
    lines = src.split('\n')
    header = {}
    if lines:
        for line in lines:
            try:
                index = line.index(':')
                key = line[:index]
                value = line[index + 1:]
                if key and value:
                    header.setdefault(key.strip(), value.strip())
            except Exception:
                pass
    return header


def is_sh_stock_file(path):
    return path.endswith(settings.SH_STOCK_FILE)


def is_sz_stock_file(path):
    return path.endswith(settings.SZ_STOCK_FILE)


def get_security_item(path):
    if is_sh_stock_file(path):
        return get_sh_security_item(path)
    elif is_sz_stock_file(path):
        return get_sz_security_item(path)


def get_tick_item(path):
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')
    with open(path, encoding=encoding) as fr:
        lines = fr.readlines()
        for line in lines[1:]:
            code, name, _, _, list_date, _, _ = line.split()
            yield SecurityItem(code='sh' + code, name=name, list_date=list_date, exchange='sh', type='stock')


def get_sz_security_item(path):
    wb = openpyxl.load_workbook(path)
    for name in wb.get_sheet_names():
        sheet = wb.get_sheet_by_name(name)
        max_row, max_column = sheet.max_row, sheet.max_column
        for i in range(2, max_row):
            code = sheet.cell(row=i, column=1).value
            name = sheet.cell(row=i, column=2).value
            list_date = sheet.cell(row=i, column=8).value
            # ignore just in B
            if not list_date:
                continue
            yield SecurityItem(code_id='sz' + code, code=code, name=name, list_date=list_date, exchange='sz',
                               type='stock')


def get_sh_security_item(path):
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')
    with open(path, encoding=encoding) as fr:
        lines = fr.readlines()
        for line in lines[1:]:
            code, name, _, _, list_date, _, _ = line.split()
            yield SecurityItem(code_id='sh' + code, code=code, name=name, list_date=list_date, exchange='sh',
                               type='stock')


def detect_encoding(url):
    import urllib.request
    from chardet.universaldetector import UniversalDetector

    usock = urllib.request.urlopen(url)
    detector = UniversalDetector()
    for line in usock.readlines():
        detector.feed(line)
        if detector.done: break
    detector.close()
    usock.close()
    return detector.result.get('encoding')


def setup_env():
    if not os.path.exists('data'):
        os.makedirs('data')
    db_setup()


def mkdir_for_security(code_id, type):
    root = os.path.join(settings.FILES_STORE, type, code_id)
    if not os.path.exists(root):
        os.makedirs(root)

    kdata = os.path.join(root, 'kdata')
    if not os.path.exists(kdata):
        os.makedirs(kdata)

    tick = os.path.join(root, 'tick')
    if not os.path.exists(tick):
        os.makedirs(tick)


def get_kdata_dir(code_id, type):
    return os.path.join(settings.FILES_STORE, type, code_id, 'kdata')


def get_kdata_path(code_id, type, year, quarter):
    return os.path.join(get_kdata_dir(code_id, type), '{}-{}-d.json'.format(year, quarter))


def get_tick_dir(code_id, type):
    return os.path.join(settings.FILES_STORE, type, code_id, 'tick')


def get_tick_path(code_id, type, date):
    return os.path.join(get_tick_dir(code_id, type), date + ".xls")


def get_sh_stock_list_path():
    return os.path.join(settings.FILES_STORE, settings.SH_STOCK_FILE)


def get_sz_stock_list_path():
    return os.path.join(settings.FILES_STORE, settings.SZ_STOCK_FILE)


def get_trading_dates(code_id, type):
    dir = get_kdata_dir(code_id, type)
    files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    dates = []
    for f in files:
        with open(f) as data_file:
            items = json.load(data_file)
            for item in items:
                dates.append(item['time'])
    dates.sort()
    return dates


def is_available_tick(path):
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')
    try:
        with open(path, encoding=encoding) as fr:
            line = fr.readline()
            return u'成交时间', u'成交价', u'价格变动', u'成交量(手)', u'成交额(元)', u'性质' == line.split()
    except Exception:
        return False


# time utils
def get_datetime(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")


def get_year_quarter(time):
    return time.year, (time.month // 3) + 1


def get_quarters(start):
    start_time = get_datetime(start)
    today = datetime.date.today()
    start_year_quarter = get_year_quarter(start_time)
    current_year_quarter = get_year_quarter(today)
    if current_year_quarter[0] == start_year_quarter[0]:
        return [(current_year_quarter[0], x) for x in range(start_year_quarter[1], current_year_quarter[1] + 1)]
    elif current_year_quarter[0] - start_year_quarter[0] == 1:
        return [(start_year_quarter[0], x) for x in range(start_year_quarter[1], 5)] + \
               [(current_year_quarter[0], x) for x in range(1, current_year_quarter[1] + 1)]
    elif current_year_quarter[0] - start_year_quarter[0] > 1:
        return [(start_year_quarter[0], x) for x in range(start_year_quarter[1], 5)] + \
               [(x, y) for x in range(start_year_quarter[0] + 1, current_year_quarter[0]) for y in range(1, 5)] + \
               [(current_year_quarter[0], x) for x in range(1, current_year_quarter[1] + 1)]
    else:
        raise Exception("wrong start time:{}".format(start));
