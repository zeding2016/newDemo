# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/9/8'

import configparser
from pathlib import Path
from openpyxl.reader.excel import load_workbook
from pathlib import Path
import xlrd
import xlwt

from lib.tool import *
import json
import asyncio
import time
import requests



#读取配置文件相关



def getConfData():
    '''
    读取配置文件
    :param api:
    :param data:
    :return:返回的是列表，0为指定的元素，第二个为该api下的所有元素选项
    '''
    #一次性的全部加载进来
    # ConfigParser都会转换为小写的问题，要进行处理
    _con = configparser.ConfigParser()
    _path = Path.cwd().parent.joinpath('data').joinpath("conf.ini")
    print(_path)
    try:
        _con.read(str(_path))
        return _con
    except Exception :
        return False
    

