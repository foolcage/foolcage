import json
import socket
import subprocess
from contextlib import closing

from foolspider.settings import DG_PATH, HTTP_PROXY_ITEMS_PATH


def start_delegate(proxy):
    local_port = find_free_port()
    cmd = '{} ADMIN=nobdoy RESOLV="" -P:{} SERVER=http TIMEOUT=con:15 SOCKS={}:{}'.format(
        DG_PATH, local_port, proxy['ip'], proxy['port'])
    subprocess.Popen(cmd, shell=True)
    return {'ip': '127.0.0.1',
            'port': local_port,
            'location': 'foolcage',
            'speed': '1',
            'type': 'http',
            'anonymity': 'high'
            }


def stop_delegate(localport):
    cmd = '{} -P:{} -Fkill'.format(DG_PATH, localport)
    subprocess.Popen(cmd, shell=True)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def check_port(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        try:
            s.bind(("127.0.0.1", port))
        except socket.error as e:
            return True
    return False


socks_proxy_items = []
http_proxy_items = []
socks2http_proxy_items = {}


def int_proxy():
    global socks2http_proxy_items
    global http_proxy_items
    global socks_proxy_items

    my_1080 = {'ip': '127.0.0.1',
               'port': 1080,
               'location': 'foolcage',
               'speed': '1',
               'type': 'socks',
               'anonymity': 'high'
               }
    my_1081 = {'ip': '127.0.0.1',
               'port': 1081,
               'location': 'foolcage',
               'speed': '1',
               'type': 'socks',
               'anonymity': 'high'
               }
    socks2http_proxy_items['{}:{}'.format(my_1080['ip'], + my_1080['port'])] = start_delegate(my_1080)

    socks2http_proxy_items['{}:{}'.format(my_1081['ip'], + my_1081['port'])] = start_delegate(my_1081)
    try:
        with open(HTTP_PROXY_ITEMS_PATH) as fr:
            items = json.load(fr)
            http_proxy_items = http_proxy_items + items
    except Exception as e:
        print(e)


def release_socks2http_proxy():
    for _, item in socks2http_proxy_items:
        stop_delegate(item['port'])
