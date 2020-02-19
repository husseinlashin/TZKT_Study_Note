# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from my51jobCrawl.items import JobListItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class My51jobSpider(CrawlSpider):
    name = 'my51job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/090200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    # 网页提取规则可使用正则或者xpath，
    # 参考Spider_development_study_note中网页解析验证中的文件my51job_rules_allow_use_xpath_1.py
    # 注意extract()提取所有的元素的内容其结果是一个列表，extract_first()提取列表中第一个元素内容
    # 提取li标签中最后一个元素使用li[last()]，倒数第二个li[last()-1]
    # 使用XPATH规则提取连接，只需要写到连接所在的标签即可
    rules = (
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[2]/div[4]/div[55]/div/div/div/ul/li[last()]/a'),
             callback='parse_job_list', follow=True),
    )

    def parse_job_list(self, response):

        # 先提取一页中所有岗位所在的标签
        jobs = response.xpath(".//div[@id='resultList']//div[@class='el']")

        # 每一个工作标签中提取工作相关的信息
        for job in jobs:
            # 匹配结果仍然是一个列表类型,列表中只有一个元素，
            # P02中已经提取过，发现里面有很多空格，提取第一个元素的值并去掉里面的空格
            # 注意P02使用的是etree.HTML解析源码，提取元素可以使用列表语法，该处是scrapy中的selector下的xpath不可以
            # 待解析的对象实例化为一个Selector对象，返回的对象实际是一个列表对象：SelectorList和Selector，其中前者是后者的集合，前者也是一个列表对象。然后该对象支持css re XPath
            # 官方推荐 ：
            # .extract_first()：提取SelectorList对象中第一个元素的内容。即返回列表中的一个元素内容。
            # .extract()：如果是SelectorList对象使用，则返回包含内容的列表；如果是Selector使用，则返回它的内容。返回的是一个列表，包含所有的内容。
            # 参考Python_advanced_learning中的04文件夹中的XPATH部分有详细总结
            jobName = job.xpath("./p/span/a/text()").extract_first().strip()
            jobLink = job.xpath("./p/span/a/@href").extract_first().strip()
            jobCompany = job.xpath("./span[1]/a/text()").extract_first().strip()
            jobAddress = job.xpath("./span[2]/text()").extract_first().strip()
            jobDate = job.xpath("./span[4]/text()").extract_first().strip()
            # 发现有些工作缺少工资信息，会导致代码终止，加入try语句
            global jobSalary
            try:
                jobSalary = job.xpath("./span[3]/text()").extract_first().strip()
            except:
                pass

            # 上面提取到的信息，加入到Item容器中，用于存储每一个工作的信息
            jobListItem = JobListItem(jobName=jobName, jobLink=jobLink,
                                      jobCompany=jobCompany, jobAddress=jobAddress,
                                      jobDate=jobDate, jobSalary=jobSalary,
                                      )

            # 进入单个工作页面，提取工作要求
            request = scrapy.Request(url=jobLink, meta={'jobListItem': jobListItem}, callback=self.parse_job_detail)
            yield request

    # 进入到第二层职位页面，提取职位的详细要求
    def parse_job_detail(self, response):
        jobListItem = response.meta['jobListItem']
        # 打开工作详细页面，发现有些岗位职责是放在p标签里面，有些放在div标签里面，
        # 如果放在p标签里面,后面同级下虽然还有div标签，但是最多只有三个
        # 如果有p标签为真,采用第一种提取方法，如果有第四个div标签，则使用第二种方法
        # 提取标签里面所有的文字
        global requirement
        if response.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p"):
            # 注意该处selector提取结果要使用.extract()提取出来，div下面有多个p标签，包含多条文字
            # 结果是一个列表，里面包含了所有的工作要求
            requirement = response.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()").extract()
        if response.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div[4]"):
            requirement = response.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div/text()").extract()
        else:
            pass
        # 提取的信息时一个列表，将列表所有内容转换为字符串
        jobRequirement = ''.join(requirement)
        jobRequirement = jobRequirement.strip()
        jobRequirement = jobRequirement.replace(' ', '')
        jobRequirement = jobRequirement.replace("\r", "")
        jobRequirement = jobRequirement.replace("\n", "")
        jobRequirement = jobRequirement.replace("\t", "")
        jobListItem['jobRequirement'] = jobRequirement
        yield jobListItem


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('my51job')
    process.start()