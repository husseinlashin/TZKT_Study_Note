# -*- coding:utf-8 -*-

import requests
from lxml import etree


links = ['https://jobs.51job.com/chengdu-jjq/112533974.html?s=01&t=0',
        'https://jobs.51job.com/chengdu-jnq/112533472.html?s=01&t=0',
    ]


def parse_body(link):
    # 设置请求头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'
    headers = {'User-Agent': user_agent}
    # 请求对象，传入请求头
    r = requests.get(link, headers=headers)
    r.encoding = 'gbk'
    html = etree.HTML(r.text, etree.HTMLParser())
    global requirement
    # 打开几个上面两个连接比较发现
    # 有些岗位职责是放在p标签里面，有些放在div标签里面，
    # 如果放在p标签里面,后面同级下虽然还有div标签，但是最多只有三个
    # 如果有p标签为真,采用第一种提取方法，如果有第四个div标签，则使用第二种方法
    if html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p"):
        requirement = html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()")
    if html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div[4]"):
        requirement = html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div/text()")
    else:
        pass
    # 提取的信息时一个列表，将列表所有内容转换为字符串
    print(requirement)
    work = ''.join(requirement)
    '''
    work = work.strip()
    work = work.replace(' ', '')
    work = work.replace("\r", "")
    work = work.replace("\n", "")
    work = work.replace("\t", "")
    '''

    print(work)

for link in links:
    print(link)
    parse_body(link)