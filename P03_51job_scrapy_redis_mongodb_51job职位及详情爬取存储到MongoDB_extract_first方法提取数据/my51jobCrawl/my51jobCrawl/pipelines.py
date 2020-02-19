# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy.exceptions import DropItem
from my51jobCrawl.items import JobListItem


# 下载数据到MongoDB数据库jobList中
# 下载ITEM中的数据到本地json文件中

class My51JobcrawlPipeline(object):

    def __init__(self, mongo_uri, mongo_db, replicaset):

        # 设置mongDB的相关参数
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    # 定义连接MongDB数据库的方法
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get('MONGO_DATABASE', '51job'),
            replicaset=crawler.settings.get('REPLICASET')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, JobListItem):
            self._process_joblist_item(item)
        else:
            pass
        return item

    # 定义一个方法用于处理工作信息，插入数据到数据库
    def _process_joblist_item(self, item):
        '''
        处理小说信息
        :param item:
        :return:
        '''
        # 向数据库51job中的jobList表中插入item数据
        self.db.jobList.insert(dict(item))

class MyJobcrawlPipeline(object):

    def __init__(self):
        self.file = open('51jobs.json', 'w', encoding='utf-8')

    # 将ITEM里面的信息写入到一个json文件中
    def process_item_json(self, jobListItem, spider):
        # 判断item字典对象中jobName对应的是否还有值
        if jobListItem['jobName']:
            # 将item字典类型的数据转换成json格式的字符串,
            # 注意json.dumps 序列化时对中文默认使用的ascii编码，要想写入中文，加上ensure_ascii=False
            line = json.dumps(dict(jobListItem), ensure_ascii=False) + "\n"
            self.file.write(line)
            return jobListItem
        else:
            raise DropItem("Missing title in %s" % jobListItem)
