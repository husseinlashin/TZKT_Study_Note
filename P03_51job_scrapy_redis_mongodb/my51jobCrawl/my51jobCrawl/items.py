# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class My51JobcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobListItem(scrapy.Item):
    # 工作名称
    jobName = scrapy.Field()
    # 工作连接
    jobLink = scrapy.Field()
    # 公司名称
    jobCompany = scrapy.Field()
    # 公司地址
    jobAddress = scrapy.Field()
    # 发布时间
    jobDate = scrapy.Field()
    # 工资
    jobSalary = scrapy.Field()
    # 工作要求
    jobRequirement = scrapy.Field()
