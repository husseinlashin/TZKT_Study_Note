# -*- coding: utf-8 -*-

# 读取txt文档中的IP地址，写入列表
# 免费公开高匿可用IP：http://www.shenjidaili.com/open/
# 设置随机代理
# 随机代理一直循环请求，直到请求成功

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
    test_url = "http://www.ifeng.com/"

    # 设置代理IP池
    proxy = ip_pool
    # 设置随机用户代理
    user_agents = user_agent.generate_user_agent()
    headers = {'User-Agent': user_agents}
    # 使用IP池随机代理,不断请求，直到请求成功
    # timeout超时设长一点，代理IP的网速很慢，延时短了，会直接抛出异常
    # HTTP都是基于TCP的socket的，经常会抛出异常的。异常了肯定没有返回码
    # 因此try-except语句要放在while循环里面，这样就算异常还是会继续循环请求
    while True:
        try:
            res = requests.get(url=test_url, headers=headers, proxies=random.choice(proxy), timeout=3)
            if res.status_code == 200:
                print("IP地址有效，请求成功")
                break
            else:
                print("IP地址失效，继续请求")
        # 捕获异常
        except Exception as e:
            print("请求异常：")
            print(e)

if __name__ == '__main__':
    print(ip_pool)
    test_proxies()
