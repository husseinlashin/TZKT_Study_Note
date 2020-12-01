# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date: 2019/9/17 19:17
Desc: https://www.51cc.co/磁力链接网站种子批量下载
# 1.按规则搜索某个种子
# 2.获取首页的种子列表
# 3.进入单个种子详情页获取magnet的值
# 4.进入下一页，获取该页的种子列表
# 5.获取该页的种子的magnet的值
# 6.依次获取之后每一页的每一个种子
# 为了代码简单，页码可以确定，规律统一，直接构造url列表即可

# 代码只需要手动输入self.url = "xxxxx"
# 修改要爬取的页码范围range(1, 26)
'''

import requests
from lxml import etree
import re
import user_agent

class BtDownload():

    def __init__(self):
        # 使用随机浏览器代理
        self.headers = {
            'User-Agent': user_agent.generate_user_agent()}
        # 初始URL手动输入，自定义的搜索规则
        self.url = "https://www.51cc.co/list?q=Vixen%201080p.MP4-KTR%5Brarbg%5D&page={}"
        # self.url = "https://www.51cc.co/list?q=Tushy%201080p.MP4-KTR%5Brarbg%5D&page={}"
        # 使用代理IP
        self.proxy = {'HTTPS': 'http://162.105.30.101:8080'}

    def url_list(self):  # 构造所有页码的url列表
        # 原始网址来自搜索某个种子的结果页
        url_list = [self.url.format(i) for i in
                    range(28, 29)]
        return url_list

    def get_html(self, url):  # 获取html文档
        # 请求对象，传入请求头
        response = requests.get(url, headers=self.headers, proxies=self.proxy).content.decode()
        # 解析requests.get获得的源码转化为XPath可以解析的对象，转换后类型：<class 'lxml.etree._Element'>
        html = etree.HTML(response, etree.HTMLParser())
        # 返回网页源码,是一个字符串类型
        return html

    def get_bt(self, html):  # 解析数据,获取一页的bt信息
        # 定义一个空字典，用于存储bt的信息，类似scrapy中的item容器
        bt_list = list()
        # 先提取一页中所有岗位所在的标签
        bts = html.xpath(".//ul[@class='list']/li")
        for bt in bts:
            bt_dict = dict()
            # 获取链接地址，只是部分地址
            link_old = bt.xpath("./a/@href")[0]
            # 拼接主页，才是完整的地址
            link = "https://www.51cc.co" + link_old
            magnet = self.get_magnet(link)
            title = bt.xpath("./a/@title")[0]
            bt_dict["title"] = title
            bt_dict["link"] = link
            bt_dict["magnet"] = magnet
            bt_list.append(bt_dict)
        return bt_list

    def get_magnet(self, link):  # 获取详情页的magnet的值
        # 详情页magnet使用xpath查找不出来，未找到原因，此处使用re直接提取magnet的值
        response = requests.get(link, headers=self.headers, proxies=self.proxy).content.decode()
        magnet = re.findall(r">(magnet:.*?)</code>", response)[0]
        return magnet

    def save_bt(self, bt_list):
        with open("vixen.txt", "a", encoding="utf-8") as f:
            for bt in bt_list:
                print(bt["magnet"])
                f.write(bt["magnet"] + "\n")

    def run(self):
        # 1. 构造URL列表
        url_list = self.url_list()
        # 2. 循环请求每一个url，即每一个页面
        for url in url_list:
            print(url)
            # 3. 获取一个url即一个页面的html文档
            html = self.get_html(url)
            # 4. 获取页面中每一个bt种子的信息
            bt_list = self.get_bt(html)
            # 5. 存储bt信息
            self.save_bt(bt_list)


if __name__ == '__main__':
    bt_download = BtDownload()
    bt_download.run()
