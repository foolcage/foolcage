from unittest import TestCase

from fospider.utils import chrome_copy_header_to_dict


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
