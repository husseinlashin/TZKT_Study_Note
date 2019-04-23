# -*- coding: utf-8 -*-
# logging模块记录输出日志信息
# 参考TLXY_study_note中高级语法log-日志记录

import logging

# 自定义记录格式：时间，日志级别，日志内容
LOG_FORMAT = "%(asctime)s------%(levelname)s------%(message)s"

# 设置输出的日志文件，设置输出什么级别的日志和日志的格式
# 该函数只在程序第一次调用时生效
# 文件内容保存到文件中，格式为自定义格式level设置的级别及该级别一上的才会打印
# 要设置编码格式，需要将文件名放到handlers中
logging.basicConfig(
    # filename='logging_record_information_1.log',
    level=logging.WARNING,
    format=LOG_FORMAT,
    handlers=[logging.FileHandler('logging_record_information_1.log', 'a', 'utf-8')]
)

# 设置相应级别的日志输出实例，括号中就是日志输出的内容
logging.debug("This is a debug log: 日志内容.")
logging.info("This is a info log: 日志内容.")
logging.warning("This is a warning log: 日志内容.")
logging.error("This is a error log: 日志内容.")
logging.critical("This is a critical log: 日志内容.")