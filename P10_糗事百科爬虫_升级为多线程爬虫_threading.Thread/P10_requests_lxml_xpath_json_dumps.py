# -*- coding:utf-8 -*-

# P09为单线程，一页一页的爬取
# 单线程升级为多线程，多个页面同时爬取

import requests
from lxml import etree
import json
import threading
from queue import Queue


class QiushiSpider():

    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.content_queue = Queue()

    def get_url_list(self):
        # return [self.url_temp.format(i) for i in range(1, 14)]
        # 网址加入到容器队列中
        for i in range(1, 14):
            self.url_queue.put(self.url_temp.format(i))

    def parse_url(self):  # 请求网页，获取网页内容
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url=url, headers=self.headers)
            # return response.content.decode()
            self.html_queue.put(response.content.decode())
            # 任务完成一个，执行task_done()，队列统计里面会自动减少一个计数
            self.url_queue.task_done()

    def get_content_list(self):  # 提取html中的数据内容
        while True:
            html_str = self.html_queue.get()
            html = etree.HTML(html_str, etree.HTMLParser())
            # 分析源码发现所有的段子都是放在div[@id='content-left']标签下的div标签里面，/div提取所有的div标签
            div_list = html.xpath(".//div[@id='content-left']/div")
            content_list = list()
            for div in div_list:
                item = dict()
                # 提取文字内容，文字内容有很多换行符，我们替换删除掉
                item["content"] = div.xpath(
                    ".//div[@class='content']/span[1]/text()")
                item["content"] = [i.replace("\n", "") for i in item["content"]]
                # 提取作者性别,<div class="articleGender womenIcon">26</div>
                item["author_gender"] = div.xpath(
                    ".//div[contains(@class, 'articleGender')]/@class")
                # 空格分隔后，去掉Icon就是性别，后面的if用于判断是否有值，没有就赋值None
                item["author_gender"] = item["author_gender"][0].split(
                    " ")[-1].replace("Icon", "") if len(item["author_gender"]) > 0 else None
                # 提取年龄
                item["author_age"] = div.xpath(
                    ".//div[contains(@class, 'articleGender')]/text()")
                item["author_age"] = item["author_age"][0] if len(
                    item["author_age"]) > 0 else None
                # 提取用户头像
                item["author_img"] = div.xpath(
                    ".//div[@class='author clearfix']//img/@src")
                item["author_img"] = "https:" + \
                                     item["author_img"][0] if len(item["author_img"]) > 0 else None
                content_list.append(item)
            # return content_list
            # 获取到内容后，先放到队列中
            self.content_queue.put(content_list)
            # 内容放到队列中后，才task_done,代表完成了一个任务
            self.html_queue.task_done()

    def save_content_list(self):  # 保存提取的到数据内容
        while True:
            content_list = self.content_queue.get()
            with open("./糗事百科.json", "a", encoding="utf-8") as f:
                for content in content_list:
                    # ensure_ascii是false,不是ascii字符的会包含在里面，即如果是中文就会保存中文
                    f.write(json.dumps(content, ensure_ascii=False) + "\n")
            self.content_queue.task_done()

    def run(self):
        thread_list = list()
        # 1 获取待爬取的url列表
        t_url = threading.Thread(target=self.get_url_list())
        thread_list.append(t_url)
        # 2 打开网页，获取响应
        t_parse = threading.Thread(target=self.parse_url())
        thread_list.append(t_parse)
        # 3 提取数据
        t_html = threading.Thread(target=self.get_content_list())
        thread_list.append(t_html)
        # 4 保存数据
        t_save = threading.Thread(target=self.save_content_list())
        thread_list.append(t_save)
        for t in thread_list:
            # 子线程设置为守护线程，主线程结束，子线程结束
            # 由于上面使用的死循环，子线程一直不会结束
            t.setDaemon(True)
            t.start()

        # 让主线程阻塞，等待所有任务完成，队列里面空了之后，执行之后的主线程代码
        for q in [self.url_queue, self.html_queue, self.content_queue]:
            q.join()

        # 等待所有线程结束后，才继续向下执行代码
        print("子线程全部完成，主线程结束")


if __name__ == "__main__":
    qiushi = QiushiSpider()
    qiushi.run()
