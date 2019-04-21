# -*- coding: utf-8 -*-

# 爬取百思不得姐网站的视频：http://www.budejie.com/video
# 分析网站，发现是静态网站，视频分页显示，http://www.budejie.com/video/1，最后数字就是页码
# 1. 获取源码；2. 解析得到一页视频列表里面所有视频标题及对应视频链接；
# 3. 下载视频以标题命名；4. 调用一页视频下载的方法下载所有页面视频

import urllib.request
import time
import requests
from lxml import etree

# 定义一个下载一页视频的方法
def download_video(url):
    # 自定义请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'}
    res = requests.get(url, headers=headers)
    # 查看源码meta标签，使用的是utf-8编码
    res.encoding = 'utf-8'
    # 获取源码,文档类型为字符串，P02中使用XPATH解析，需要转换
    html = etree.HTML(res.text, etree.HTMLParser())
    # print(type(html))
    videos = html.xpath(".//div[@class='j-r-list-c']")
    # 每一页第一个j-r-list-c标签没有视频，直接排出掉，后面if判断也可，代码太多
    url_names = []
    for video in videos[1:]:
        # 提取出标题和对应的视频url,提取列表第一个元素并去掉字符两端的空格
        title = video.xpath("./div[1]/a[1]/text()")[0].strip()
        video_url = video.xpath("./div[2]/div[1]/@data-mp4")[0].strip()
        # print(title, video_url)
        url_name = [title, video_url]
        url_names.append(url_name)

    for i in url_names:
        # 有些视频链接下载保存为文件时候会出错，文件命名有些字符禁止使用
        try:
            # urlretrieve用于下载文件
            urllib.request.urlretrieve(i[1], r'D:\Hello World\python_download\budejie_videos\%s.mp4' % i[0])
            # 缓慢下载，设置延时
            time.sleep(0.5)
            print("正在下载视频： %s" % i[0])
        except FileNotFoundError:
            pass
        finally:
            pass

# 获取每一页页面的地址，调用上面的方法，下载每一页的所有视频
def download_videos():
    # 提取每一页的连接，规律相同，网页最后一个数字不同
    for page in range(0, 5):
        page += 1
        url = 'http://www.budejie.com/video/%s' % page
        print("正在下载第%s页的所有视频......" % page)
        # 调用上面的爬虫方法下载每一页的图片
        try:
            download_video(url)
        # 上面页码可以加大，但是有可能页码后面就没了，加一个万能异常
        except Exception:
            pass
        finally:
            pass

if __name__ == '__main__':
    download_videos()