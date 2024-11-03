import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def setup_logger(name='my_loger'):
    # 创建 Logger
    logger = logging.getLogger(name) # 创建 Logger 对象 name 为日志名称
    logger.setLevel(logging.DEBUG) # 设置日志级别为 DEBUG

    if not logger.hasHandlers():
        # 创建Handler，用于写入日志文件
        console_handler = logging.StreamHandler() # 创建 StreamHandler 对象，用于将日志输出到控制台
        console_handler.setLevel(logging.DEBUG) # 设置日志级别为 DEBUG

        # 创建Formatter，用于设置日志格式 将其添加到 Handler 中
        formatter = logging.Formatter('%(asctime)s -%(name)s %(levelname)s - %(message)s') # 创建 Formatter 对象，用于设置日志格式
        console_handler.setFormatter(formatter)

        # 将 Handler 添加到 Logger 中
        logger.addHandler(console_handler)

    return logger


