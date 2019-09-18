# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date: 2019/9/18 21:47
Desc:
'''

import user_agent
import requests
import random

def ip_pool():
    ip_pool = list()
    with open('ip_proxy_xici.txt', mode='r', encoding='utf-8') as f:
        content = f.readlines()
        for ip in content:
            # 逐行读取时候，每一行末尾有换行符：\n，替换掉换行符
            ip = ip.replace('\n', '')
            # 将IP转换成requests参数proxies规定的格式，字典键值形式
            ip_dict = {'http': 'http://' + ip, 'https': 'http://' + ip}
            # 验证IP是否有效，有效就添加到列表中去
            try:
                test_url = "https://www.hao123.com/"
                headers = {'User-Agent': user_agent.generate_user_agent()}
                response = requests.get(url=test_url, headers=headers, proxies=ip_dict, timeout=1)
                if response.status_code == 200:
                    ip_pool.append(ip_dict)
            except Exception:
                pass
    print(ip_pool)
    return ip_pool


def test_proxies():

    test_url = "https://www.hao123.com/"

    # 设置代理IP池
    proxies = ip_pool()
    headers = {'User-Agent': user_agent.generate_user_agent()}
    # 使用IP池随机代理,不断请求，直到请求成功
    # timeout超时设长一点，代理IP的网速很慢，延时短了，会直接抛出异常
    # HTTP都是基于TCP的socket的，经常会抛出异常的。异常了肯定没有返回码
    # 因此try-except语句要放在while循环里面，这样就算异常还是会继续循环请求
    while True:
        try:
            ip = random.choice(proxies)
            response = requests.get(url=test_url, headers=headers, proxies=ip, timeout=1)
            if response.status_code == 200:
                print(response.status_code)
                print(ip)
                break
        except Exception as e:
            print("请求异常: %s" % e)

if __name__ == '__main__':
    test_proxies()
