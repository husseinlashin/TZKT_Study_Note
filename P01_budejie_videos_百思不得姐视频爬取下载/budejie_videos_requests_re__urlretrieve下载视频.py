# -*- coding: utf-8 -*-

# 爬取百思不得姐网站的视频：http://www.budejie.com/video
# 分析网站，发现是静态网站，视频分页显示，http://www.budejie.com/video/1，最后数字就是页码

import urllib.request
import re
import requests
import time

# 定义一个下载一页视频的方法
def download_video(url):
    # 自定义请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'}
    res = requests.get(url, headers=headers)
    # 查看源码meta标签，使用的是utf-8编码
    res.encoding = 'utf-8'
    # 获取源码,文档类型为字符串，P02中使用XPATH解析，需要转换
    html = res.text
    # print(type(html))
    # 使用re找出所有的视频所在的标签
    # 编写一个正则匹配对象,注意参数re.S,表示把html当做一个整体字符串，忽略其中的换行符\n，
    # .*?是非贪婪模式，找到一个满足要求的即可，最小匹配模式
    # 我们查看源码，发现从<div class="j-r-list-c">开始，只需要匹配到第二个</div>就可以包括了标题和视频地址所在的内容
    pattern = re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)', re.S)
    # 整个源码匹配查找出我们所需要的每一部分内容，返回结果是一个列表
    url_contents = re.findall(pattern, html)
    # 遍历列表，提取标题和视频链接地址
    url_name = []
    for i in url_contents:
        # 有些列表中可能没有视频，所以先找出有视频的内容,提取出链接地址
        # 正则表达式里面使用了小括号编组，匹配返回的结果只有编组里面的内容，即返回URL地址
        video_pattern = r'data-mp4="(.*?)"'
        # 每个i依次匹配，返回值是一个列表，如果没有内容则是一个空列表
        video_url = re.findall(video_pattern, i)
        # print(video_url)
        # 由于有些i中并没有视频匹配，返回值是一个空列表，所以先if判断一下
        if video_url:
            # 如果视频存在，提取对应的标题标签中的文字,下面的.*？两边的括号()代表一个组,匹配提取出组里面的内容
            # name_pattern = re.compile(r'<a href="/detail-.*?.html">(.*?)</a>')
            # 里面有两个括号，提取出两个组，第一个组匹配到的网页中的数字，第二个组是标题文字
            # name_pattern = re.compile(r'<a href="/detail-(.*?).html">(.*?)</a>')
            # .{8}?匹配任意字符一次，限制长度为8，和上面.*？匹配结果相同
            name_pattern = re.compile(r'<a href="/detail-.{8}?.html">(.*?)</a>')
            name = re.findall(name_pattern, i)
            # print(name)
            # 将标题和地址一一对应打包为一个元组，然后添加到列表中
            for i, k in zip(name, video_url):
                # 以列表方式加入，方便后面取出
                url_name.append([i, k])
    # print(url_name)
    for i in url_name:
        # 有些视频链接下载保存为文件时候会出错，文件命名有些字符禁止使用
        try:
            # urlretrieve用于下载文件，从视频地址下载，保存地址
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