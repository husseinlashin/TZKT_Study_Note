# 参考P06代理爬取相关案例

# 官方格式：

```python
import requests

proxy = {
    'http': 'http://162.105.30.101:8080',
    'https': 'http://162.105.30.101:8080',
}

url = 'https://www.hao123.com/'
response = requests.get(url, proxies=proxy)  #默认verify为True，verify=False是否验证服务器的SSL证书

print(response.status_code)
print(response.headers)
```

# 注意：上面IP地址前面的http://可以不写，最后一行的逗号也可以不写，推荐都按标准格式写
# http和https要小写，如果写成大写，就会识别为语法错误， 相当于没有写，proxies=None
# 如果单词写错了也会当成proxies=None

