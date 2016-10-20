from unittest import TestCase

from fospider.utils.utils import chrome_copy_header_to_dict, get_quarters, get_trading_dates


class TestUtils(TestCase):
    def test_chrome_copy_header_to_dict(self):
        src = '''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:zh-CN,zh;q=0.8,en;q=0.6
Connection:keep-alive
Host:www.szse.cn
Referer:http://www.szse.cn/main/marketdata/jypz/colist/
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'''
        header = chrome_copy_header_to_dict(src)
        assert header.get('Accept') == 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        assert header.get('Accept-Encoding') == 'gzip, deflate, sdch'
        assert header.get('Accept-Language') == 'zh-CN,zh;q=0.8,en;q=0.6'
        assert header.get('Connection') == 'keep-alive'
        assert header.get('Host') == 'www.szse.cn'
        assert header.get('Referer') == 'http://www.szse.cn/main/marketdata/jypz/colist/'
        assert header.get('Upgrade-Insecure-Requests') == '1'
        assert header.get('Host') == 'www.szse.cn'
        assert header.get(
            'User-Agent') == 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'

    def test_get_quarters(self):
        set1 = set(get_quarters('2014-4-1'))
        assert set1 == {(2014, 2), (2014, 3), (2014, 4), (2015, 1), (2015, 2), (2015, 3), (2015, 4),
                        (2016, 1), (2016, 2), (2016, 3), (2016, 4)}
        set2 = set(get_quarters('2015-4-1'))
        assert set2 == {(2015, 2), (2015, 3), (2015, 4), (2016, 1), (2016, 2), (2016, 3), (2016, 4)}
        set3 = set(get_quarters('2016-4-1'))
        assert set3 == {(2016, 2), (2016, 3), (2016, 4)}

    def test_get_trading_dates(self):
        dates = get_trading_dates('sh600000', 'stock')
        assert dates[0] == '1999-12-30'
        assert dates[-1] == '2016-10-19'
