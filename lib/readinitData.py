# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/9/8'

import configparser
import os


def getConfData(api, data):
    '''
    读取配置文件
    :param api:
    :param data:
    :return:返回的是列表，0为指定的元素，第二个为该api下的所有元素选项
    '''
    
    # ConfigParser都会转换为小写的问题，要进行处理
    # 初始化时候要设置s的变量，s为你目录文件夹名称
    data = data.lower()
    
    
    
    #
    # def setPath(fileName, s='MiFi-test'):
    #     '''设置路径'''
    #
    #     path = os.path.abspath( '.' )
    #
    #     if path.endswith( s ):
    #         return path + '/data/' + fileName
    #
    #     elif os.path.dirname( path ).endswith( s ):
    #         return os.path.dirname( path ) + '/data/' + fileName
    #
    #     elif os.path.dirname( os.path.dirname( path ) ).endswith( s ):
    #         return os.path.dirname( os.path.dirname( path ) ) + '/data/' + fileName
    #
    #     else:
    #         raise RuntimeError( '请确认正确的路径' )
    #
    # _path = setPath( 'conf.conf' )
    #
    # _con = configparser.ConfigParser()
    # try:
    #     with open( _path, 'r' ) as f:
    #         _con.readfp( f )
    #         allData = _con.sections()
    #
    #         if allData.count( api ) == 1 and _con.options( api ).count( data ):
    #
    #             return _con.get( api, data ), _con.options( api )
    #         else:
    #             exit( '无法找到所对应的变量' )
    # except Exception as e:
    #
    #     return e
    #






