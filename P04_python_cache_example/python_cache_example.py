# -*- coding:utf-8 -*-

# python缓存实例（用于节省内存）
# CPU从内存中读取数据，频繁读取的数据放入到CPU的缓存中
# CPU处理数据非常快，内存相对于CPU而言非常慢，因此CPU经常被访问的数据可以放入CPU的缓存中

# 装饰器：本质上也是一个函数，在不改变原来函数功能的基础上，增加额外的功能
# 比如：王者荣耀的一个英雄，本身拥有三个技能，买个皮肤，增加了一个外观，但是原来三个技能不变。

# 装饰器本案例中使用：
# 1. 实现缓存 2. 计算函数的运行时间 3. 插入日志 4. 权限的校验

import time

# 定义一个用于获取func函数运行时间的函数
def get_time1(func):

    # 内部定义实现该函数的功能
    def get_running_time(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(end - start)

    return get_running_time

# 定义一个缓存，我们要使用函数要使用参数12和3，如果12和3在缓存之中，则函数直接拿来使用
# 如果函数不在缓存之中，则从内存中取出12和3，然后放到缓存，以便下次使用，这就是缓存的用途
rets = {}
def outer(f):

    def wrapper(*args, **kwargs):
        # 从缓存(上面的rets字典）中获取数据，数据存储在键中
        key = "%s, %s" % (args, kwargs)
        # 如果key有数据返回数据，没有则返回None
        dict_data = rets.get(key, None)
        # 判断一下，如果有key，则获取key的值，没有数据则执行原函数，并把返回的结果加入到缓存
        if dict_data:
            print("缓存中获取的数据")
            ret = dict_data
        else:
            print("缓存中无数据，执行该函数，获取的结果写入缓存")
            ret = f(*args, **kwargs)
            rets[key] = key
        return ret

    return wrapper


# 给函数加入第一个装饰器，增加一个获取该函数运行时间的功能
@get_time1
# 给函数加入第二个装饰器，用于写入缓存
@outer
def func_a(a, b):
    time.sleep(2)
    ret = a * b * b * b * b * b * b
    print(ret)
    return ret

func_a(3, 1)
print("--------------")
func_a(2, 1)
print("--------------")

time1 = time.time()
func_a(3, 1)
time2 = time.time()
print("第三次调用函数用时：%s" % (time2 - time1))






