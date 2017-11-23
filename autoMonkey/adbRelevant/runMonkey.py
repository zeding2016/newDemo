# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/22'
import random
from autoMonkey.tool import tool

class RunMonkey(object):
    '''启动monkey'''
    def __init__(self,device,packageName,version,deviceId,testEnvironment,default):
        '''设备'''
        self.device = device
        self.packageName = packageName
        self.testEnvironment = testEnvironment
        self.version = version
        self.deviceId = deviceId
        self.default = default #默认次数
    def setLog(self,log_for_android):
        '''设置log'''
        
        pass
    
    
    
    def setParam(self):
        '''设置运行的参数'''
        data=[]
        #在事件之间插入固定的时间（毫秒）延迟，你可以使用这个设置来减缓Monkey的运行速度，
        #如果你不指定这个参数，则事件之间将没有延迟，事件将以最快的速度生成。
        data.append("--throttle 450") #这里默认设置450毫秒
        
        #伪随机数生成器的seed值。如果用相同的seed值再次运行Monkey， 它将生成相同的事件序列。
        data.append("-s {}".format(random.randint(10,100000)))
        
        #确定运行的程序包名
        data.append("-p {}".format(self.packageName))
        
        # 调整触摸事件的百分比( 触摸事件是一个down - up事件，它发生在屏幕上的某单一位置)。
        data.append( "--pct-touch {}".format("50" ) )

        #调整“系统”按键事件的百分比(这些按键通常被保留，由 系统使用，如Home、Back、Start Call、End Call及音量控制键)。
        data.append( "--pct-syskeys {}".format( "0" ) )
        
        # 通常，当应用程序崩溃或发生任何失控异常时，Monkey将停止运行。如果设置此选项，Monkey将 继续向系统发送事件，
        # 直到计数完成。
        data.append( "--ignore-crashes" )

        data.append( " --ignore-security-exceptions" )

        data.append( " --ignore-timeouts" )

        data.append( "--monitor-native-crashes" )
        #日志等级
        data.append( "-v -v -v" )

        data.append( "--bugreport" )
        
  
        logFileName = "%s.log " % tool.setLogName(versionNum=self.version,deviceId=self.deviceId,testEnvironment="test")
        
    
        allShellCmd = "adb shell monkey " + "".join(data)+" "+str(self.default)+">{}".format(tool.getLocalPath()+logFileName)
        
        return allShellCmd
      
    
        


    def start_monkey(self):
        '''初始化参数'''
        
        
        pass
    
    def main(self):
        ''''''
        print("running start.....")
        
        #开始运行adb monkey....
