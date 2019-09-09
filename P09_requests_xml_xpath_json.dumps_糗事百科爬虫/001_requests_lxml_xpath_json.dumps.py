# -*- coding:utf-8 -*-

import requests
from lxml import etree
import json


class QiushiSpider():

    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}

    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(1, 14)]

    def parse_url(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):  # 提取数据
        html = etree.HTML(html_str, etree.HTMLParser())
        # 分析源码发现所有的段子都是放在div[@id='content-left']标签下的div标签里面，/div提取所有的div标签
        div_list = html.xpath(".//div[@id='content-left']/div")
        content_list = list()
        for div in div_list:
            item = dict()
            # 提取文字内容，文字内容有很多换行符，我们替换删除掉
            item["content"] = div.xpath(".//div[@class='content']/span[1]/text()")
            item["content"] = [i.replace("\n", "") for i in item["content"]]
            # 提取作者性别,<div class="articleGender womenIcon">26</div>
            item["author_gender"] = div.xpath(".//div[contains(@class, 'articleGender')]/@class")
            # 空格分隔后，去掉Icon就是性别，后面的if用于判断是否有值，没有就赋值None
            item["author_gender"] = item["author_gender"][0].split(" ")[-1].replace("Icon", "") if len(
                item["author_gender"]) > 0 else None
            # 提取年龄
            item["author_age"] = div.xpath(".//div[contains(@class, 'articleGender')]/text()")
            item["author_age"] = item["author_age"][0] if len(item["author_age"]) > 0 else None
            # 提取用户头像
            item["author_img"] = div.xpath(".//div[@class='author clearfix']//img/@src")
            item["author_img"] = "https:" + item["author_img"][0] if len(item["author_img"]) > 0 else None
            content_list.append(item)
        return content_list

    def save_content_list(self, page_num, content_list):
        with open("./糗事百科.json", "a", encoding="utf-8") as f:
            for content in content_list:
                # ensure_ascii是false,不是ascii字符的会包含在里面，即如果是中文就会保存中文
                f.write(json.dumps(content, ensure_ascii=False) + "\n")
            print("第%s页保存成功" % page_num)

    def run(self):
        # 1 获取待爬取的url列表
        url_list = self.get_url_list()
        print(url_list)
        # 2 打开网页，获取响应
        for url in url_list:
            html_str = self.parse_url(url)
            # 3 提取数据
            content_list = self.get_content_list(html_str)
            # 4 保存数据
            # url地址转换为列表，取倒数第二个元素就是页码
            page_num = list(url)[-2]
            self.save_content_list(page_num, content_list)


if __name__ == "__main__":
    qiushi = QiushiSpider()
    qiushi.run()
