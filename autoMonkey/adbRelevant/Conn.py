# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/22'
from pathlib import Path, PurePath
import datetime, time, os, sys
import subprocess
from autoMonkey.tool.tool import setLogName
from functools import reduce
import platform




class AdbDevice( object ):
    '''adb命令封装'''
    __adb_start = 'adb start-server'
    __adb_kill = 'adb kill-server'
    __adb_version = 'adb version'
    __adb_battery = 'adb shell dumpsys battery'
    __adb_all = 'adb shell getprop ro.product.model'  # 查看设备信息
    __adb_Android_version = 'adb shell getprop ro.build.version.release'
    __adb_cpu = 'adb shell cat /proc/cpuinfo'
    __adb_allDetails = 'adb shell getprop'  # 更多硬件与系统属性

    # ro.build.version.sdk	SDK版本
    # ro.build.version.release	Android 系统版本
    # ro.build.version.security_patch	Android安全补丁程序级别
    # ro.product.model	型号
    # ro.product.brand	品牌
    # ro.product.name	设备名
    # ro.product.board	处理器型号
    # ro.product.cpu.abilist	CPU支持的 abi 列表
    # persist.sys.isUsbOtgEnabled	是否支持 OTG
    # dalvik.vm.heapsize	每个应用程序的内存上限
    # ro.sf.lcd_density	屏幕密度
    _adb_shot = 'adb shell screencap -p /sdcard/sc.png'  # 截图
    _adb_screenRecord = 'adb shell screenrecord /sdcard/filename.mp4'  # 录制屏幕
    
    def __init__(self, packageName):
        self.__packageName = packageName
        '''试着去连接adb'''
        self.__osName = platform.system()  # 当前系统
        self.__package = self.__getPackage()  # 应用的包名
        self.__devices = self.__getDevices()  # 设备列表
        
      
    def __getDevices(self):
        try:
            # 无阻塞的方法
            a = subprocess.Popen( "adb devices", shell=True, stdout=subprocess.PIPE )
            b = a.communicate()[0].decode( 'utf-8' )  # 该方法会阻塞父进程，直到子进程完成。
            _devices = b.split( "\n" )[1:]  # .split( "\t" )[0]  # 第一个设备，后期做扩展
            tmp = []
            for i in _devices:
                if i != "":
                    tmp.append( i.split( "\t" )[0] )
            # self.devices = tmp #设备列表
            a.kill()  # 这里只是尝试性的去连接adb，及时断开；
        except subprocess.CalledProcessError as err:
            print( err )
            print( "command error" )
            return None
        except Exception as e:
            print( e )
            return None
        return tmp
    
    # 安装app，确保apk文件在当前文件夹下
    def __installApp(self):
        apkPath = None
        path = Path.cwd().parent
        for i in Path( path ).iterdir():
            if str( i ).endswith( "data" ):
                for j in Path( i ).iterdir():
                    if str( j ).endswith( ".apk" ):
                        apkPath = j
        if apkPath != None:
            try:
                os.popen( 'adb install -r {}'.format( str( apkPath ) ) )
            except Exception as e:
                print( e )
                return False
    
    
    def __getPackage(self):
        '''获取包名的应用'''
        adb_shell='adb shell pm list packages -3|grep {}'.format( self.__packageName )
        osRes = os.popen( adb_shell ).read()
        if osRes == "":
            self.__installApp()
            while True:
                osRes = os.popen( adb_shell ).read()
                if osRes != "":
                    break
        return osRes
        
        
        
    def getPackageName(self):
        '''获取包名称，并确保安装了对应的app'''
        return self.__package
   
 
    def getDevices(self):
        '''获取设备列表'''
        return self.__devices



#
# a = AdbDevice("mifi")
#
# print(a.getDevices())
