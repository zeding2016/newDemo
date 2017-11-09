# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/7'

import requests

from .tool import myLog

logForHttp = myLog( "http" )


def callApi(method, data, url, **kwargs):
    
    if method not in ('post', 'get'):
        
        logForHttp.error( "{} not exist".format( method ) )
        return False
    
    # 创建一个session对话
    res = requests.session()
    if method == 'post':
        logForHttp.info( method +" "+ str( kwargs ).format( url ) )
        return res.post( url=url, timeout=20, data=data, **kwargs )  # 超时时间 20秒
    
    if method == 'get':
        logForHttp.info( method +" "+ str( kwargs ).format( url ) )
        return res.get( url=url, timeout=20, params=data, **kwargs )  # 超时时间 20秒
