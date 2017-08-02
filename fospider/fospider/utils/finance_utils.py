import logging
import os

from fospider import settings
from fospider.items import SecurityItem
from fospider.utils.utils import get_balance_sheet_path, detect_encoding

logger = logging.getLogger(__name__)


def get_balance_sheet_item(security_item):
    path = get_balance_sheet_path(security_item)
    encoding = settings.DOWNLOAD_TXT_ENCODING if settings.DOWNLOAD_TXT_ENCODING else detect_encoding(
        url='file://' + os.path.abspath(path)).get('encoding')
    with open(path, encoding=encoding) as fr:
        lines = fr.readlines()
        for line in lines:
            items = line.split()
            yield items


for item in get_balance_sheet_item(SecurityItem(type='stock', code='000004', exchange='sz')):
    logger.info(item)
