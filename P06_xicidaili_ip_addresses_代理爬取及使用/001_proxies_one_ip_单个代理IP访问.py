# -*- coding: utf-8 -*-

# 单个IP代理设置方式

import requests

proxy = {
    'HTTPS': '162.105.30.101:8080'
}

url = 'https://www.baidu.com/'

response = requests.get(url,proxies=proxy)

print(response.status_code)
print(response.headers)