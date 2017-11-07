# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/7'

import os
import time
from pathlib import Path
from pathlib import PurePath
import shutil
import logzero
from logging.handlers import SysLogHandler
from logzero import logger, setup_logger
import logging
import random
from datetime import datetime
from functools import wraps
import hashlib


def singleton(cls):
    '''单例装饰器'''
    instances = {}
    
    @wraps( cls )
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls( *args, **kw )
        return instances[cls]
    return getinstance


class myLog( object ):
    '''日志模块的封装'''
    def __init__(self, logName, nameForLog='log', clevel=logging.INFO):
        _tmp="{}.txt".format( nameForLog )
        __path = str(self.__getLogPath().joinpath(_tmp))
        self.__logger = setup_logger( name=logName, logfile=__path, level=clevel )
    
    def __getLogPath(self):
        __path = Path().cwd().parent.joinpath("log")  # 获取当前的目录
        return __path
    
    def debug(self, message):
        self.__logger.debug( message )
    
    def info(self, message):
        self.__logger.info( message )
    
    def warn(self, message):
        self.__logger.warn( message )
    
    def error(self, message):
        self.__logger.error( message )
    
    def cri(self, message):
        self.__logger.critical( message )

forTime = myLog( "-time-",nameForLog="time" )



# 计时装饰器
def describeTime(func):
    def inner(*args, **kwargs):
        startTime = time.clock()
        a = func( *args, **kwargs )
        totalTime = time.clock() - startTime
        forTime.info("耗时："+totalTime)
        return a
    return inner


#生成mac地址
def getMac() :
    # 生成A0:18:28:83:C8:0B
    Maclist = []
    for i in range(1, 7) :
        RANDSTR = "".join(random.sample("0123456789abcdefghijklmnpqrstuvw", 2))
        Maclist.append(RANDSTR)
    RANDMAC = ":".join(Maclist).upper()
    return RANDMAC


def md5_str(content, encoding='utf-8'):
    """计算字符串的MD5值

    :param content:输入字符串
    :param encoding: 编码方式
    :return:
    """
    m = hashlib.md5(content.encode(encoding))
    return m.hexdigest()

