import datetime
import json
import logging

from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from foolspider.settings import HTTP_PROXY_ITEMS_PATH, SOCKS_PROXY_ITEMS_PATH

logger = logging.getLogger(__name__)

PROXY = "socks5://127.0.0.1:1081"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server={}'.format(PROXY))
chrome_options.add_argument('headless')

chrome = webdriver.Chrome(chrome_options=chrome_options)

chrome.get('https://hidemy.name/en/proxy-list/')
element = WebDriverWait(chrome, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "proxy__t"))
)

trs = Selector(text=element.get_attribute('innerHTML')).xpath('//tr').extract()

http_jsons = []
socks_jsons = []

for tr in trs[1:]:
    tds = Selector(text=tr).xpath('//td//text()').extract()
    tds = [x.strip() for x in tds]

    location = tds[2]
    if tds[3]:
        location = location + " " + tds[3]

    check_time_gap = int(tds[7].split()[0].strip())
    check_time = (datetime.datetime.now() + datetime.timedelta(seconds=-check_time_gap)).strftime(
        '%Y-%m-%d %H:%M:%S')

    json_item = {"ip": tds[0],
                 'port': tds[1],
                 'location': location,
                 'speed': tds[4],
                 'type': tds[5],
                 'anonymity': tds[6],
                 'checkTime': check_time}

    if tds[5] == 'HTTP' or tds[5] == 'HTTPS':
        http_jsons.append(json_item)
    else:
        socks_jsons.append(json_item)

    if http_jsons:
        try:
            with open(HTTP_PROXY_ITEMS_PATH, "w") as f:
                json.dump(http_jsons, f, ensure_ascii=False)
        except Exception as e:
            logger.error("failed to save http proxy json:{}", e)

    if socks_jsons:
        try:
            with open(SOCKS_PROXY_ITEMS_PATH, "w") as f:
                json.dump(http_jsons, f, ensure_ascii=False)
        except Exception as e:
            logger.error("failed to save socks proxy json:{}", e)
