# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date: 2019/9/29 22:27
Desc:
'''
from lxml import etree
import requests

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
    }

url = "https://www.vixen.com/videos?page=1&size=12"
response = requests.get(url, headers=headers).content.decode()
# 解析requests.get获得的源码转化为XPath可以解析的对象，转换后类型：<class 'lxml.etree._Element'>
html = etree.HTML(response, etree.HTMLParser())
print(response)

div_list = html.xpath("//div[@class='sc-1egln9q-0 gpzUBK']")
for div in div_list:
    img = div.xpath("./img/@src")
    print(img)
