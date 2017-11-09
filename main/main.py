# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/8'
import traceback
import os
import configparser
from pathlib import Path, PurePath
from openpyxl.reader.excel import load_workbook
from pathlib import Path
import xlrd
import xlwt
import shutil
import xlutils
from lib.tool import *
import json
import asyncio
import time
import requests
import datetime


class dataDrivenAutoTest( object ):
    '''数据驱动自动化测试
    moudle, url, method, data, expectedResult, des,status,detail
    '''
    
    def __new__(cls, *args, **kwargs):
        print( "开始时间：", datetime.datetime.now() )
        return object.__new__( cls )
    
    def __init__(self):
        self.__log = myLog( logName='main' )
        self.__cases = 0
        self.__mainPath = Path.cwd().parent
        self._caseOfFile = []  # case的excel的文件列表
        self._dataOfInit = []  # 测试数据的准备
        self.__wb = None  # 文档
        self.__sheets = None  # 文档对应的所有的表
        self.__localHost = getConfData().get( 'testEnvironment', 'localhost' )
        self.__setUp()
    
    def __del__(self):
        print( "结束时间：", datetime.datetime.now() )
    
    def getAllCases(self):
        '''总用例数'''
        return self.__cases
    
    def __setUp(self):
        '''测试前的准备工作'''
        
        if self.__checkData():
            self.__setExcel( 'case.xlsx' )
        else:
            print( "data for Testting is not exist" )
            return
    
    def __setExcel(self, dataName):
        ''''''
        _path = Path.cwd().parent.joinpath( 'data' ).joinpath( dataName )
        self.__wb = xlrd.open_workbook( filename=str( _path ) )
        self.__sheets = self.__wb.sheet_names()  # all sheets
    
    def __getFileOfApi(self):
        '''所有接口测试文档'''
        return self._caseOfFile
    
    def __getAllSheets(self):
        '''获得所有的表'''
        return self.__sheets
    
    def __getWorksheet(self, index):
        '''获得第几张表'''
        return self.__wb.sheet_by_name( self.__sheets[index] )
    
    def __checkData(self):
        '''检测data下的文件是否准备好了，测试数据准备'''
        __path = Path.cwd().parent.joinpath( 'data' )
        __path_iter = Path( __path ).iterdir()
        for i in __path_iter:
            if i.is_file():
                if str( i.name ).startswith( 'case' ):
                    self._caseOfFile.append( i )
                elif str( i.name ).startswith( 'conf' ):
                    self._dataOfInit.append( i )
        if self._caseOfFile.__len__() != 0 and self._dataOfInit.__len__() != 0:
            return True
        
        return False
    
    # 拼接URL
    def __setUrl(self, url):
        return self.__localHost + url
    
    # 设置输出的结果
    def _setReportExcel(self, name, bold, height):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        # style.borders = borders
        
        return style
    
    def callback(self, r):
        # 在这里进行结果数据的业务判断
        # 读取expectedResult 即kwargs
        __allData = r.result()[1]
        status = ''
        details = ''
        checkPointsList = __allData['_expectedResult'].split( ',' )
        index = __allData['index']
        print( index )
        # 这里有个异常需要判断
        # moudle, url, method, data, expectedResult, des, status, detail
        try:
            if r.result()[0].status_code == 200:
                _res = r.result()[0].json()
                for i in checkPointsList:
                    tmp = str( i ).split( '=' )
                    try:
                        if _res[tmp[0]] == tmp[1]:
                            status = 'pass'
                            details = ''
                        else:
                            
                            status = 'fail'
                            details = str( _res[tmp[0]] ) + '!=' + str( tmp[1] )
                            continue  # 发现一旦出错立即跳过本条case，将其标记为fail
                    except:
                        status = 'error'
                        details = traceback.format_exc()
            else:
                status = 'error'
                details = str( 'r.result()[0].status_code:' + str( r.result()[0].status_code ) )
        except:
            details = traceback.format_exc()
            status = 'error'
        
        print( status, details, )
    
    # 请求requests的方法
    
    
    async def __callApi(self, method, data, url, headers=None, **kwargs):
        if method not in ('post', 'get'):
            return False
        # 创建一个session对话
        res = requests.session()
        r = None
        if method == 'post':
            try:
                r = res.post( url=url, timeout=20, data=data, headers=headers )
            except Exception as e:
                # w网络出错
                r = str( e )
        if method == 'get':
            try:
                r = res.get( url=url, timeout=20, params=data, headers=headers )
            except Exception as e:
                r = str( e )
        
        return r, kwargs
        
        # 主函数入口，多进程+协程
    
    def mainTwo(self):
        pass
        
        # 主函数入口，单线程，协程的方式运行测试用例
    
    def main(self):
        self.__setExcel( 'case.xlsx' )
        worksheet = self.__getWorksheet( 0 )
        _cols = worksheet.ncols
        _rows = worksheet.nrows
        self.__cases = _rows
        _tasks = []
        for i in range( _rows ):
            if i == 0:
                pass
                # moudle, url, method, data, expectedResult, des, status, detail = worksheet.row_values( i, )
                # 重新代开一个excel，写出这几个标题
                # ,这里后续需要补写
                #########################
            else:
                # 顺序如下：moudle,url,method,data,expectedResult,des
                _tmp = worksheet.row_values( i, )
                # 这里要对所传的data转换成json格式的必须要求是双引号
                r = self.__callApi( method=_tmp[2], url=self.__setUrl( _tmp[1] ), data=json.loads( _tmp[3] ),
                                    _expectedResult=_tmp[4], _des=_tmp[5], _moudle=_tmp[0], index=i )
                _tasks.append( asyncio.ensure_future( r ) )
        for t in _tasks:
            t.add_done_callback( self.callback )
        loop = asyncio.get_event_loop()
        loop.run_until_complete( asyncio.wait( _tasks ) )


a = dataDrivenAutoTest()
a.main()
