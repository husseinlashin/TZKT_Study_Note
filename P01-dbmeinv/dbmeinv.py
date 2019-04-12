# -*- coding:utf-8 -*-

# 爬取www.dbmeinv.com网站所有的第一层页面的图片
# 要爬取第二层图片，推荐使用scrapy爬取,定义parse和parse_body方法分别解析第一层和第二层
# 复习巩固：urllib.request bs4 urllib.request.urlretrieve等使用

# https://www.dbmeinv.com/?pager_offset=1

import time
from bs4 import BeautifulSoup
from urllib import request


# 用于图片命名
x = 0

# 定义一个下载一页里面所有图片的方法
def dbmeinvSpier(url):
    # 设置请求头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3650.400 QQBrowser/10.4.3341.400'
    headers = {'User-Agent': user_agent}
    # 请求对象
    req = request.Request(url, headers=headers)
    # 打开对象
    res = request.urlopen(req, timeout=20)
    # 读取得到源代码
    contents = res.read()
    # 使用bs4解析源码
    soup = BeautifulSoup(contents, 'html.parser')
    # 找出所有的图片标签，返回结果是一个列表
    girl_pictures = soup.find_all('img')
    # 提取出每张图片的标签
    for girl_picture in girl_pictures:
        # 从图片标签中获取图片的链接
        img_link = girl_picture.get('src')
        # 使用urlretrieve下载函数来下载图片，存储到指定文件夹
        # 参数url：下载数据的链接地址
        # 参数filename：指定了保存本地路径及文件名称
        # girl_pictures为py文件同级目录下的文件夹，%s.jpg是下载文件的名称
        global x
        # 从1开始，按数字名称顺序命名，也可以提取图片标题命名
        x += 1
        request.urlretrieve(img_link,'girl_pictures\%s.jpg' % x)
        # 缓慢下载，设置延时
        time.sleep(0.1)
        print("正在下载第%s张图片" % x)

# 获取每一页页面的地址，调用上面的方法，下载每一页的所有图片
def dbmeinvallSpier():
    # 提取每一页的连接，规律相同，网页最后一个数字不同
    for page in range(0, 5):
        page += 1
        url = 'https://www.dbmeinv.com/?pager_offset=%s' % page
        print("正在下载第%s页的所有图片......" % page)
        # 调用上面的爬虫方法下载每一页的图片
        dbmeinvSpier(url)

if __name__ == '__main__':
    dbmeinvallSpier()




