# The project includes a series of Python demos.

# 本项目包含多个Python小项目
# 用于练习巩固Python知识
# 爬虫小项目、网络热点小项目

## P01_dbmeinv
- 爬取不羞涩网站的所有图片
    - urllib.request：请求获取对象
    - bs4：解析对象
    - urllib.request.urlretrieve：远程下载数据

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
    
## P04_python缓存小案例
- python实现缓存的一个小案例

## P05_budejie_videos
- 百思不得姐网站全部视频下载
    - 主要使用：requests,urllib进行请求
    - 解析网页分别使用了：xpath和re正则两种方法
    - 下载视频使用：urllib.request.urlretrieve方法
    - xpath解析更加简单明了
    - re正则相对代码行数较多
    
## P06_xicidaili_ip_addresses
- 代理IP爬取及使用
    - 爬取西刺代理网站的高匿IP
    - 单个IP代理使用方式
    - 多个IP代理使用方式
    - 使用IP池随机代理


