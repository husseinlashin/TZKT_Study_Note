# The project includes a series of Python demos.

# 本项目包含多个Python小项目
# 用于练习巩固Python知识
# 爬虫小项目、网络热点小项目

## P01_budejie_videos
- 百思不得姐网站全部视频下载
    - 主要使用：requests,urllib进行请求
    - 解析网页分别使用了：xpath和re正则两种方法
    - 下载视频使用：urllib.request.urlretrieve方法
    - xpath解析更加简单明了
    - re正则相对代码行数较多

## P02_51job
- 前程无忧岗位获取（入门版）
- 获取前程无忧上关键字为'Python'所有岗位信息
    - requests库
    - XPath
    - 爬取第一层和第二层页面相关信息
    
## P03_51job
- 前程无忧岗位获取（进阶版）
- 获取前程无忧上成都地区关键字为'Python'所有岗位信息
    - scrapy模块
    - scrapy-redis去重
    - MongDB副本集存储数据  
    - 反爬措施：随机用户代理，自动限速，禁用Cookies，IP代理池（失效，未启用）  

## P04_dbmeinv
- 爬取不羞涩网站的所有图片
    - urllib.request：请求获取对象
    - bs4：解析对象
    - urllib.request.urlretrieve：远程下载数据
    
## P05_python缓存小案例
- python实现缓存的一个小案例

## P06_xicidaili_ip_addresses
- 代理IP爬取及使用
    - 爬取西刺代理网站的高匿IP
    - 单个IP代理使用方式
    - 多个IP代理使用方式
    - 使用IP池随机代理
    - 筛选有效代理，移除无效代理

## P07_logging_record_crawl_process
- logging日志

## P08_requests_re_内涵段子爬虫
- 内涵段子爬虫
    - requests
    - re正则提取数据
    
## P09_requests_xml_xpath_json.dumps_糗事百科爬虫
- 糗事百科爬虫
    - requests
    - xml xpath解析
    - json存储数据
    
## P10_糗事百科爬虫_升级为多线程爬虫_threading.Thread
- 多线程糗事百科爬虫
    - requests
    - xml xpath解析
    - json存储数据
    - threading.Thread
    
## P11_哔哩哔哩各栏目下面视频地址爬取-JS动态请求分析
- 哔哩哔哩视频爬虫
    - 爬取一个栏目所有视频信息
    - JS动态请求逆向分析
    - 核心是寻找视频页面的真实请求地址
    - 重点是JS分析
## P12_视频网站视频真实上传日期_日期爬取_requests_re_匹配分组
- 视频网站视频真实日期提取
    - requests
    - re正则
    - 正则匹配分组
    - 日期匹配分组后交换位置
    - 日期替换
    - 日期修改
    
## P13_requests_xpath_bt下载_网站定义规则搜索_提取所有搜索结果bt的magnet值_两级解析
- 种子批量爬虫
    - 搜索种子(搜索规则也可以加入到爬虫中)
    - 提取搜索到的种子magnet值
    - 去除重复的种子，保存


