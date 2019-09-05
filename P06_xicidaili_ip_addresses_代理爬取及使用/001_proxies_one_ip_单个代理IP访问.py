# -*- coding: utf-8 -*-

# 单个IP代理设置方式

import requests

proxy = {
    'HTTPS': '162.105.30.101:8080'
}

url = '爬取链接地址'

response = requests.get(url,proxies=proxy)