# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/8'
import traceback
import xlrd
import xlwt
import json
import asyncio
import requests
import datetime
from pathlib import Path, PurePath
from logzero import logger, setup_logger
import logging
import configparser
import time
import sys
import io


# 读取配置文
def getConfData():
    '''读取配置文件'''
    # 一次性的全部加载进来，只进行一次一次读取，然后直接调用
    # ConfigParser都会转换为小写的问题，要进行处理
    _con = configparser.ConfigParser()
    _path = Path.cwd().parent.joinpath( 'data' ).joinpath( "conf.ini" )
    try:
        
        _con.read( _path )
        return _con
    except Exception:
        return False


class myLog( object ):
    '''日志模块的封装'''
    
    def __init__(self, logName, nameForLog='log', clevel=logging.DEBUG):
        _tmp = "{}.txt".format( nameForLog )
        __path = str( self.__getLogPath().joinpath( _tmp ) )
        self.__logger = setup_logger( name=logName, logfile=__path, level=clevel )
    
    def __getLogPath(self):
        __path = Path().cwd().parent.joinpath( "log" )  # 获取当前的目录
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


class dataDrivenAutoTest( object ):
    '''数据驱动自动化测试
   
    demo
    1、准备目录结构(采用了markdown语法）
    * case
    >excel的接口测试文档（这里不需要）

    * ext
    >业务流封装包


    * data
    >接口测试需要产生的测试数据
    >这里必须要配置两个文档case.xlsx和conf.ini
        1、conf.ini这里不能有中文
        2、case.xlsx的里面结构如下
            moudle, url, method, data, expectedResult, des,status,detail
    
    * lib
    >一些常用的方法，业务封装方法，接口的逻辑等

    * main
    >主入口
    
    * report
    >接口测试报告
  
    2、运行
        a = dataDrivenAutoTest()
        b.main()
        将会在report下生成一个时间字符串的excel文档
    '''
    
    def __new__(cls, *args, **kwargs):
        print( "startTime：", datetime.datetime.now() )
        return object.__new__( cls )
    
    def __init__(self):
        self.__log = myLog( logName='main' )
        self.__log.debug( '*' * 60 )
        self.__cases = 0
        self.__mainPath = Path.cwd().parent
        self._caseOfFile = []  # case的excel的文件列表
        self._dataOfInit = []  # 测试数据的准备
        self.__wb = None  # 文档
        self.__sheets = None  # 文档对应的所有的表
        self.__localHost = getConfData().get( 'testEnvironment', 'localhost' )
        self.pathForRes = Path.cwd().parent.joinpath( 'report' ).joinpath(
            '{}.xls'.format( str( time.strftime( "%Y%m%d%H%M%S", time.localtime() ) ) ) )
        self.__setUp()
    
    def __del__(self):
        print( "结束时间：", datetime.datetime.now() )
    
    def getAllCases(self):
        '''总用例数'''
        return self.__cases
    
    def __setUp(self):
        '''测试前的准备工作'''
        
        if self.__checkData():
            self.__log.info( "data for testting is on...." )
            self.__setExcel( 'case.xlsx' )
        else:
            self.__log.error( "data for Testting is not exist" )
            return
    
    def __setExcel(self, dataName):
        ''''''
        _path = Path.cwd().parent.joinpath( 'data' ).joinpath( dataName )
        self.__wb = xlrd.open_workbook( filename=str( _path ) )
        self._forResult = xlwt.Workbook()  # 新建一个excel文件
        self.report = self._forResult.add_sheet( 'Sheet1', cell_overwrite_ok=True )
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

    def __getSpecifyLen(self,data, length):
        tmp = len( str( data ) )
        t = ""
        if (length == 0 or tmp == 0):
            return 0
        if (length > tmp):
        
            return data
        else:
            for i in (list( data ))[:length]:
                t += i
            return t

    # 拼接URL
    def __setUrl(self, url):
        return self.__localHost + url
    
    # 设置输出的结果
    def _setReportExcel(self, color):
        # format = workbookx.add_format()
        style = xlwt.easyxf( 'pattern: pattern solid,fore_colour {}; font: bold on;'.format( color ) )
        return style
    
    def callback(self, r):
        # 在这里进行结果数据的业务判断
        # 读取expectedResult 即kwargs
        __allData = r.result()[1]
        status = ''
        details = ''
        checkPointsList = __allData['_expectedResult'].split( ',' )
        index = __allData['index']
        # 这里有个异常需要判断
        percent = (int( index ) / int( self.__cases )) * 100
        s = "running-[{}]-[time:{}]-[{}%]".format( __allData['_des'],r.result()[2], str( percent )[0:5] )
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
                            self.__log.info( s + str( status ) + '  {}'.format( str( details ) ) )
                        else:
                            status = 'fail'
                            details = str( _res[tmp[0]] ) + '!=' + str( tmp[1] )
                            self.__log.warn( s + str( status ) + '  {}'.format( str( details ) ) )
                    except:
                        status = 'error'
                        details = traceback.format_exc()
                        self.__log.error( s + str( status ) + '  {}'.format( details ) )
            
            else:
                status = 'error'
                details = str( 'r.result()[0].status_code:' + str( r.result()[0].status_code ) )
        except:
            details = traceback.format_exc()
            status = 'error'
        self.report.write( index, 0, __allData['_moudle'] )
        self.report.write( index, 1, __allData['_url'] )
        self.report.write( index, 2, __allData['_method'] )
        self.report.write( index, 3, __allData['_data'] )
        self.report.write( index, 4, __allData['_expectedResult'] )
        self.report.write( index, 5, __allData['_des'] )
        if status == 'pass':
            self.report.write( index, 6, status, self._setReportExcel( "green" ) )
            self.report.write( index, 7, details, self._setReportExcel( "green" ) )
        elif status == 'fail':
            self.report.write( index, 6, status, self._setReportExcel( "red" ) )
            self.report.write( index, 7, details, self._setReportExcel( "red" ) )
        elif status == 'error':
            self.report.write( index, 6, status, self._setReportExcel( "yellow" ) )
            self.report.write( index, 7, details, self._setReportExcel( "yellow" ) )
            # time.sleep( 1 )
            
            
            # self.__log.info("运行第{}条case，【".format(index)+str(int(index)/(int(__allData['_all']))-1)+"】"+str(status))
    
    # 请求requests的方法
    async def __callApi(self, method, data, url, headers=None, **kwargs):
        tmpTime  =time.time()
        if method not in ('post', 'get'):
            return False
        # 创建一个session对话
        res = requests.session()
        r = None
        if method == 'post':
            try:
                r = res.post( url=url, timeout=20, data=data, headers=headers )
            except Exception as e:
                r = str( e )
        if method == 'get':
            try:
                r = res.get( url=url, timeout=20, params=data, headers=headers )
            except Exception as e:
                r = str( e )
        totalTime = self.__getSpecifyLen(str(time.time() - tmpTime),5)
        
        return r, kwargs,totalTime
    
    # 参数化case（）后期优化
    def arameterizeMain(self):
        pass
    
    # 主函数入口，多进程+协程 ，后期优化
    def mainTwo(self):
        pass
    
    # 主函数入口，单线程，协程的方式运行测试用例
    def main(self):
        self.__log.info( "start run testCase....." )
        self.__setExcel( 'case.xlsx' )
        worksheet = self.__getWorksheet( 0 )
        _rows = worksheet.nrows
        self.__cases = _rows - 1
        
        _tasks = []
        for i in range( _rows ):
            if i == 0:
                # moudle, url, method, data, expectedResult, des, status, detail = worksheet.row_values( i, )
                a = worksheet.row_values( i, )
                for j in range( len( a ) ):
                    self.report.write( i, j, a[j], self._setReportExcel( "green" ) )
            else:
                # 顺序如下：moudle,url,method,data,expectedResult,des
                _tmp = worksheet.row_values( i, )
                # 这里要对所传的data转换成json格式的必须要求是双引号
                r = self.__callApi( method=_tmp[2], url=self.__setUrl( _tmp[1] ), data=json.loads( _tmp[3] ),
                                    _expectedResult=_tmp[4], _des=_tmp[5], _moudle=_tmp[0], index=i, _data=_tmp[3],
                                    _method=_tmp[2], _url=_tmp[1] )
                self.__log.info( "formate testCase{}.....".format(_tmp[5]) )
                _tasks.append( asyncio.ensure_future( r ) )
        for t in _tasks:
            t.add_done_callback( self.callback )
        loop = asyncio.get_event_loop()
        loop.run_until_complete( asyncio.wait( _tasks ) )
        self._forResult.save( str( self.pathForRes ) )
        time.sleep( 1 )
        self.__log.info( "running testCase.....SUCCESS!!!!!!" )
        
        #
        #
        #
if __name__ == '__main__':
    a = dataDrivenAutoTest()
    a.main()
