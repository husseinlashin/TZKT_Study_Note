# -*- coding: utf-8 -*-

# 1. 爬取西刺代理网站的国内高匿代理的IP地址和端口
# 2. 使用随机用户代理生成器
# 3. 如何使用获取的高匿代理
# 高匿代理：服务器只能发现代理的地址，但是发现不了你真实的IP地址
# 起始网页：https://www.xicidaili.com/nn/1

import  requests
from lxml import etree
import user_agent


def crawl_xicidaili():
    # 用于存储有效IP地址的空列表
    global ip_list
    ip_list = []
    # 爬取20页的代理IP地址
    for i in range(1, 20):
        start_url = 'https://www.xicidaili.com/nn/{}'.format(i)
        # 随机生成用户代理,每次请求都会变化
        headers = {
            'User-Agent': user_agent.generate_user_agent()
        }
        # 请求获取网页,指定网页源码相同的编码格式
        res = requests.get(url=start_url, headers=headers)
        res.encoding = 'utf-8'
        # 将网页源码str格式转换成xpath支持的html格式
        # 转换之后html类型：<class 'lxml.etree._Element'>
        html = etree.HTML(res.text, etree.HTMLParser())
        # 提取IP地址和端口所在的所有标签
        # 使用火狐浏览器，查看元素，右键复制table标签所在的xpath路径
        addresses = html.xpath("//table[@id='ip_list']//tr")
        # 循环上面得到的所有标签，注意tr[1]是栏目栏,tr[2]开始才是IP地址栏
        # 遍历每个IP标签，提取有效的IP最后添加到ip_list中
        for address in addresses[1:]:
            # 再次确认判断一下地址是否为高匿地址：
            if address.xpath("./td[5]/text()")[0] == "高匿":
                ip_address = address.xpath("./td[2]/text()")[0]
                ip_port = address.xpath("./td[3]/text()")[0]
                ip_proxy = ip_address + ":" + ip_port

                # 验证IP地址是否可以正常使用，使用代理请求是否成功
                test_url = "https://www.hao123.com/"
                # 设置代理地址参数，# 使用IP代理格式类似：'http://127.0.0.1:8118'
                # 使用的字典的键值形式设置IP代理
                proxies = {
                    'http': 'http://' + ip_proxy,
                    'https': 'https://' + ip_proxy,
                }
                # 代理的格式：
                '''
                proxies = {
                    "http": "http://10.10.1.10:3128",
                    "https": "http://10.10.1.10:1080",
                }
                '''
                # 使用代理IP请求百度首页，加入代理和超时参数，代理无效打印语句
                # requests代理使用参考：https://2.python-requests.org/zh_CN/latest/user/advanced.html?highlight=%E4%BB%A3%E7%90%86#proxies
                try:
                    res = requests.get(url=test_url, headers=headers, proxies=proxies, timeout=1)
                    if res.status_code == 200:
                        print("该IP地址有效:", ip_proxy)
                        ip_list.append(ip_proxy)
                        # 将可用的IP写入文件
                        with open('ip_proxy_xici.txt', mode='a+', encoding='utf-8') as f:
                            f.write(ip_proxy + "\n")
                except Exception:
                    print("该IP地址已失效:", ip_proxy, Exception)

if __name__ == '__main__':
    crawl_xicidaili()
    print(ip_list)


