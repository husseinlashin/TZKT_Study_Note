# -*- coding: utf-8 -*-

# 读取txt文档中的IP地址，写入列表
# 免费公开高匿可用IP：http://www.shenjidaili.com/open/
# 设置随机代理

import user_agent
import requests
import random
import time

# 设置用于存放IP地址的空列表
ip_pool = []

# 打开txt文件，逐行读取所有的内容
# 将每个IP以字典的键值形式添加到列表中
with open('ip_proxy_xici.txt', mode='r', encoding='utf-8') as f:
    # 逐行读取txt中所有的内容
    ip_address = f.readlines()
    for i in ip_address:
        # 逐行读取时候，每一行末尾有换行符：\n，替换掉换行符
        i = i.replace('\n', '')
        # 将IP转换成requests参数proxies规定的格式，字典键值形式
        i_dict = {'http': 'http://' + i, 'https': 'https://' + i}
        ip_pool.append(i_dict)
# print(ip_pool)

def test_proxies():
    test_url = "https://www.hao123.com/"

    # 设置代理IP池
    proxy = ip_pool
    # 设置随机用户代理
    user_agents = user_agent.generate_user_agent()
    headers = {'User-Agent': user_agents}
    # 使用IP池随机代理,不断请求，直到请求成功
    try:
        while True:
            res = requests.get(url=test_url, headers=headers, proxies=random.choice(proxy), timeout=1)
            if res.status_code == 200:
                print("该IP地址有效,网页请求成功")
                break
            else:
                pass
    except Exception:
        pass

if __name__ == '__main__':
    # 加入while死循环，一直随机请求
    # while True:
    # test_proxies()
    print(ip_pool)
    test_proxies()
