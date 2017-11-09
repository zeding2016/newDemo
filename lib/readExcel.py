# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/8'

from openpyxl.reader.excel import load_workbook
from pathlib import Path
import xlrd
import xlwt

from lib.tool import *
import json
import asyncio
import time
import requests
localHost = getConfData().get('testEnvironment','localhost')



async def callApi(method, data, url, **kwargs):
    if method not in ('post', 'get'):
        
        return False
    # 创建一个session对话
    res = requests.session()
    print(time.time())
    if method == 'post':
        return res.post( url=url, timeout=20, data=data, **kwargs ) # 超时时间 20秒
    if method == 'get':
        return res.get( url=url, timeout=20, params=data, **kwargs )  # 超时时间 20秒


_path = Path.cwd().parent.joinpath( 'data' ).joinpath( "case.xlsx" )
wb = xlrd.open_workbook(filename=str(_path))
sheets = wb.sheet_names()#所有的表
worksheet = wb.sheet_by_name(sheets[0])#第一张表



# resulsheet = wb.sheet_by_name(sheets[1])#第一张表
def auth(num=1):
  
    try:
        url__ = localHost + getConfData().get( 'auth', 'url' )[0]
        payload = {'runMode': num}
        return callApi( url=url__, method='get', data=payload )
    except Exception as e:
       
        return False
    
    

cols = worksheet.ncols
rows = worksheet.nrows



cases = []


tasks=[]



for i in range(rows):
    if i == 0:
        moudle,url,method,data,expectedResult,des = worksheet.row_values(i,)
    else:
        #顺序如下：moudle,url,method,data,expectedResult,des
        _tmp =worksheet.row_values(i,)
        _moudle = _tmp[0]
        _url =localHost+_tmp[1]
        _method = _tmp[2]
        _data = _tmp[3]
        _expectedResult = _tmp[4]
        _des = _tmp[5]
        
        #这里要对所传的data转换成json格式的必须要求是双引号
        r = callApi(method=_method,url=_url,data=json.loads(_data))
        tasks.append(asyncio.ensure_future(r))
        

loop = asyncio.get_event_loop()
loop.run_until_complete( asyncio.wait( tasks ) )
for t in tasks:
    print( t.result() )



# demo3
# tasks=[
#     asyncio.ensure_future(work1(1)),
#     asyncio.ensure_future( work1( 12) ),
#     asyncio.ensure_future( work1( 5 ) ),
#     asyncio.ensure_future( work1( 10) )
#
# ]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))
#
for t in tasks:
    print(t.result())
    
    

#把task全部封装起来
 

 
 
# #第一列为表头名
# moudle = worksheet.cell_value(0,0)
# url = worksheet.cell_value(0,1)
# method= worksheet.cell_value(0,2)
# description = worksheet.cell_value(0,3)
# time= worksheet.cell_value(0,4)
# result = worksheet.cell_value(0,5)
# detail= worksheet.cell_value(0,6)
#





