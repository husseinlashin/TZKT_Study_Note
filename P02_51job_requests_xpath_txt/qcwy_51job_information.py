# -*- coding:utf-8 -*-
# date: 2019.04.13

# 获取前程无忧上关键字为'Python'所有岗位信息
# 使用requests模块
# 使用lxml和Xpath

import requests
from lxml import etree

# 1. 获取源码
def get_content(i):
    # 每一页页面只有个.html前面的数字不同，采用format函数写入数字，就可以得到不同的网址
    url = 'https://search.51job.com/list/090200,000000,0000,00,9,99,python,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i)
    # 设置请求头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'
    headers = {'User-Agent': user_agent}
    # 请求对象，传入请求头
    r = requests.get(url, headers=headers)
    # 网页源码使用的gbk，charset='gbk'，该处进行解码
    r.encoding = 'gbk'
    # 返回网页源码,是一个字符串类型
    return r.text


# 2. 补充一步，将上面的requests.get得到的text字符串转化为XPath可以解析的对象
def get_html(i):
    text = get_content(i)
    # 解析requests.get获得的源码转化为XPath可以解析的对象
    # 转换之后html类型：<class 'lxml.etree._Element'>
    html = etree.HTML(text,etree.HTMLParser())
    return html

# 3. 解析数据
# item用来存储每一个工作的所有信息，由于要循环爬取多个页面，因此item放在最外层
item = []
def get(html):
    # 先提取一页中所有岗位所在的标签
    jobs = html.xpath(".//div[@id='resultList']//div[@class='el']")
    for job in jobs:
        # 匹配结果仍然是一个列表类型,列表中只有一个元素，提取元素并去掉里面的空格
        # scrapy使用的selector中不能用这种[0].strip()列表语法，使用extract(),extract_first()提取第一个列表元素
        name = job.xpath("./p/span/a/text()")[0].strip()
        link = job.xpath("./p/span/a/@href")[0].strip()
        company = job.xpath("./span[1]/a/text()")[0].strip()
        address = job.xpath("./span[2]/text()")[0].strip()
        date = job.xpath("./span[4]/text()")[0].strip()
        # 发现有些工作缺少工资信息，会导致代码终止，加入try语句
        global salary
        try:
            salary = job.xpath("./span[3]/text()")[0].strip()
        except:
            pass

        # 进入到第二层职位页面，提取职位的详细要求
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
            # 提取标签里面所有的文字
            if html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p"):
                requirement = html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()")
            if html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div[4]"):
                requirement = html.xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div/div/text()")
            else:
                pass
            # 提取的信息时一个列表，将列表所有内容转换为字符串
            work = ''.join(requirement)
            return work

        work = parse_body(link)
        item.append(name + '  ' + company + '  ' + address + '  ' + date + '  ' + link + '\n' + work )

    return item

# 3. 将提取的item写入到文件
def write_file():
    for i in range(1, 2):
        get_content(i)
        html = get_html(i)
        item = get(html)
        for x in item:
            with open('Python成都招聘岗位信息汇总.txt', 'a', encoding='utf-8') as f:
                f.write(x + '\n' + '\n')

if __name__ == '__main__':
    write_file()








