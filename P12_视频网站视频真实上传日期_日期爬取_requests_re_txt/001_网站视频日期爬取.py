# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date: 2019/9/16 21:22
Desc:
'''

# 视频网址视频下面日期是视频上传日期，真实拍摄日期大多数都早一天
# 视频源码中的日期正好是早一天的真实日期，直接提取对应日期即可

import requests
import re
import time

def get_date(url_list):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
    }
    # 循环URL地址
    for url in url_list:
        # 每间隔5秒请求一个页面
        response = requests.get(url=url, headers=headers)
        time.sleep(0.5)
        # 获取页面源码
        html = response.content.decode()
        # 寻找出日期, 类似格式：November 11, 2018
        date_list = re.findall(">([a-zA-Z]+ \d+, \d+)<", html)
        with open("date.txt", "a", encoding="utf-8") as f:
            for date in date_list:
                # July 18, 2019修改为Vixen.19.07.18
                # 先替换20为Vixen.
                date = date.replace("20", "Vixen.")
                # 匹配分组，交换顺序
                date_new = re.sub(r'([a-zA-Z]+) (\d+), (Vixen.\d+)', r'\3.\1.\2', date)
                # 分别进行月份替换
                date_new = date_new.replace("January", "01")
                date_new = date_new.replace("February", "02")
                date_new = date_new.replace("March", "03")
                date_new = date_new.replace("April", "04")
                date_new = date_new.replace("May", "05")
                date_new = date_new.replace("June", "06")
                date_new = date_new.replace("July", "07")
                date_new = date_new.replace("August", "08")
                date_new = date_new.replace("September", "09")
                date_new = date_new.replace("October", "10")
                date_new = date_new.replace("November", "11")
                date_new = date_new.replace("December", "12")
                f.write(date_new + "\n")
            with open("date_list.txt", "a", encoding="utf-8") as f:
                f.write(url + "：爬取完成" + "\n")
                f.write(str(date_list) + "\n")
        print(url + "：爬取完成")
        print(date_list)


if __name__ == '__main__':
    url_list = ["https://www.vixen.com/videos?page=" + str(i) + "&size=12" for i in range(1, 21)]
    get_date(url_list)

