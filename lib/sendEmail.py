# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/7'
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib




class myMail( object ):
    '''邮件相关'''
    _to_list = ['dingze4321@sina.com', 'dingze647@pingan.com.cn']
    
    def __init__(self, subject):
        '''
        :param subject: 主题
        '''
        try:
            self._server = smtplib.SMTP()
            self._msg = MIMEMultipart()
        except Exception as e:
            print( e )
            return
        
        self.subject = subject
        self._mail_user = 'test_mifi@sina.com'  # 用户名
        self._mail_pass = 'abcd1234'  # 口令
    
    def __del__(self):
        try:
            self._server.close()
        except Exception as e:
            print( e )
    
    def setMail(self, content, att=None, subtype=u'html'):
        '''
        :param att:  附件 必须为列表的格式
        :param content:  内容
        :param subtype: 附件的格式
        :return:
        '''
        
        if att:
            assert type( att ) == list
            if len( att ) != 0:
                for i in att:
                    name = str( i ).split( r'/' )[-1]
                    att1 = MIMEText( open( i, 'rb' ).read(), 'base64', 'utf-8' )
                    att1["Content-Type"] = 'application/octet-stream'
                    att1["Content-Disposition"] = 'attachment; filename="attachment{}"'.format(
                        name )  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                    self._msg.attach( att1 )
        
        self._msg.attach( MIMEText( content, _subtype=subtype, _charset='utf-8' ) )
    
    def sendMail(self, sender='邮件发送', rec=_to_list):
        ''''''
        self._msg['To'] = ";".join( rec )
        self._msg['Subject'] = self.subject  # 设置主题
        self._msg['From'] = self._mail_user
        
        try:
            self._server.connect( 'smtp.sina.com' )
            self._server.starttls()
            self._server.login( self._mail_user, self._mail_pass )
            self._server.sendmail( self._mail_user, self._to_list, self._msg.as_string() )
        
        except Exception as e:
            print( e )
            return False
        finally:
            self._server.close()



