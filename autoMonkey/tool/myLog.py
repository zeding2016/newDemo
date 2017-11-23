# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/22'

from logzero import setup_logger
import logging
from pathlib import Path,PurePath


class myLog( object ):
    '''日志模块的封装'''
    def __init__(self, logName, nameForLog='log', clevel=logging.INFO):
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


