# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/22'
from pathlib import Path,PurePath
import time


def setLogName(versionNum, deviceId, testEnvironment, *args):
    '''
    :param version: 版本号
    :param deviceId: 测试设备序列号
    :param testnvironment: 测试环境
    :return:
    '''
    local_time = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
    tmp = "_".join( [str( versionNum ), str( deviceId ), str( testEnvironment ),str(local_time)])
    
    if len( args ) == 0:
        return tmp
    
    else:
        tmpList = []
        for i in args:
            if not isinstance( i, str ):
                i = str( i )
                tmpList.append( i )
            else:
                tmpList.append( i )
    return tmp + "_".join( tmpList )


    
    
def getLocalPath():
    path = Path.cwd().parent
    if str(path).endswith("autoMonkey"):
        return str(path)+"/log"
    else:
        return None
