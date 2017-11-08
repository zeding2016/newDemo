# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/7'

def format_(f, n):
    if round( f ) == f:
        m = len( str( f ) ) - 1 - n
        if f / (10 ** m) == 0.0:
            return f
        else:
            return float( int( f ) / (10 ** m) * (10 ** m) )
    return round( f, n - len( str( int( f ) ) ) ) if len( str( f ) ) > n + 1 else f




class myResultForEmail( object ):
    '''拼接为html格式的邮件'''
    
    def __init__(self, subject, startTime, endTime):
        '''
        :param subject: 报告的名称
        '''
        self.sub = subject
        self._moudles = []
        self._cases = []
        self._AllCases = []
        self._totalNum = 0
        self._passNum = 0
        self._failNum = 0
        self._errNum = 0
        self._totalTime = 0
        self.startTime, self.endTime = startTime, endTime
    
    def setAll(self, cases):
        '''把所有的case传入进来做分析,读取文件的形式
            demo：case=['testmoudle-testCase-status-time-details']
            如果status是pass则details为None
        '''
        self._cases = cases
    
    def getInfo(self, con):
        '''

        :param con: 1、module测试模块     2、cases 所有的测试用例  包含了  pass   fail    error   time  模块名称
        :return:
        '''
        if con == 1:
            return self._moudles
        if con == 2:
            return self._cases
    
    def _setDiv1(self):
        
        _div1 = u''' <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
	    <head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width,initial-scale=1.0">

		<title></title>
	    <body style="padding:0">
                    <div id="1" style="text-align: center">
			        <h1 style="color: deeppink">{}</h1>
		            </div>
		        '''.format( self.sub )
        
        return _div1
    
    def _setTime(self):
        '''

        :param s: 开始时间
        :param e: 结束时间
        :return:
        '''
        _time = u'''
        <ul style="padding: 0;list-style: none;">
			<li>开始时间：{0}</li>
			<li>结束时间：{1}</li>
		</ul>
        '''.format( self.startTime, self.endTime )
        return _time
    
    def _setDiv2(self, p, f, e):
        '''

        :param p:  pass%
        :param f: fail%
        :param e: e%
        :return:
        '''
        
        _div2 = u'''
        <div >
			<div style="width:{}%;height: 15px;background: green ;display: inline-block;float: left;text-align: center;font-size: 10px;" >{}%</div>
			<div style="width:{}%;height: 15px;background: red ;display: inline-block;margin-left: 0;float: left;text-align: center;font-size: 10px" >{}%</div>
			<div style="width:{}%;height: 15px;background: grey ;display: inline-block;float: left;text-align: center;font-size: 10px" >{}%</div>
		</div>'''.format( p, p, f, f, e, e )
        
        return _div2
    
    def _setTable(self, body):
        '''

        :param _moudle:
        :param case:
        :param total:
        :return:
        '''
        _table = u'''


        <table width="100%" border="1" cellspacing="0" class="report" style="border-collapse: collapse;text-align: center;">
        <tr class="testHeader">
				<th width="60%">测试moudle/测试case</th>
				<th>总数</th>
				<th>成功</th>
				<th>错误</th>
				<th>失败</th>
				<th>耗时</th>
		</tr>
		{}
        </table>
        </body>
                    </html>

        '''.format( body )
        return _table
    
    def _setTestMoudle(self, s, t, p, f, e, time):
        '''
        testModle
        :param t:
        :param p:
        :param f:
        :param e:
        :return:
        '''
        
        _testMoudle = u'''
        <tr class="testMoudle">
				<td>{0}</td>
				<td>{1}</td>
				<td>{2}</td>
				<td>{3}</td>
				<td>{4}</td>
				<td>{5}s</td>

		</tr>
        '''.format( s, t, p, f, e, time )
        self._moudles.append( s )
        return _testMoudle
    
    def _setTestCase(self, case, stat, d, t):
        '''
        :param case:
        :param stat:
        :param t:
        :return:
        '''
        _s = self._setCaseDetils( d )
        if stat == 'pass':
            _testCase = '''
                   <tr class="testCase">
                   <td>{0}</td>
                   <td colspan="4">{1}</td>
                   <td>{2}s</td>
                   </tr>
                   '''.format( case, stat, t )
        
        else:
            _a = '''
                <a href="#" style="color: red;text-decoration: none;" onclick="if (this.nextElementSibling.style.visibility =='hidden'){alert(1);this.nextElementSibling.style.visibility ='visible';this.nextElementSibling.style.display=''}else{this.nextElementSibling.style.visibility ='hidden';this.nextElementSibling.style.display='none'}">
               %s</a> %s
               ''' % (stat, _s)
            _testCase = '''
                   <tr class="testCase">
                   <td>{0}</td>
                   <td colspan="4">{1}</td>
                   <td>{2}</td>
                   </tr>
                   '''.format( case, _a, t )
        
        return _testCase
    
    def _setCaseDetils(self, details):
        _details = u'''<pre style="visibility:hidden;display: none;clear: both">{}</pre>'''.format( details )
        return _details
    
    def _setTotal(self, total, p, f, e, t):
        _total = u'''
        <tr class="end">
				<td>总结</td>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
				<td>{}</td>
				<td >{}s</td>
		</tr>

        '''.format( total, p, f, e, t )
        
        return _total
    
    def _setTotalReport(self):
        '''
        case=['testmoudle-testCase-status-time-details']
        _data={'testMoudle':[(case1,pass,time,details),(case2,fail,time,details).....]}
        :return:
        '''
        _data = {}
        # _result = {} #{'testMoudle'：[total,pass,fail,wrong]} 全部结果的显示 为int型
        # _totalReport =[]
        _one = None
        try:
            if self._cases:
                for i in self._cases:
                    
                    l = str( i ).split( "-" )
                    if l[0] not in _data.keys():
                        # 并初始化
                        _data[l[0]] = []
                    _data[l[0]].append( [l[1], l[2], l[3], l[4]] )
            
            else:
                print( "无相关case" )
        except Exception as e:
            print( e )
            pass
        
        _one = ""
        for i in _data.keys():
            _t, _p, _f, _e, _time = 0, 0, 0, 0, 0
            _TestCase, _TestMoudle = "", ""
            _t = len( _data[i] )
            self._totalNum += len( _data[i] )
            for k in _data[i]:
                
                # j是对应moudle的所有cases数目列表 case, stat, d, t
                #
                # print( k )
                # print( k[0], k[1], k[3], k[2] )
                _TestCase = _TestCase + self._setTestCase( k[0], k[1], k[3], k[2] )
                self._totalTime += int( k[2] )
                _time += int( k[2] )
                if k[1] == 'pass':
                    
                    _p += 1
                    self._passNum += 1
                elif k[1] == 'fail':
                    
                    _f += 1
                    self._failNum += 1
                elif k[1] == 'error':
                    
                    _e += 1
                    self._errNum += 1
            
            _TestMoudle = self._setTestMoudle( i, _t, _p, _f, _e, _time )
            
            _one += (_TestMoudle + _TestCase)
        
        _one = _one + self._setTotal( self._totalNum, self._passNum, self._failNum, self._errNum, self._totalTime )
        
        # 拼接报告的body
        return self._setDiv1() + self._setTime() + self._setDiv2(
            (100 * format_( (self._passNum / self._totalNum), 5 )),
            (100 * format_( (self._failNum / self._totalNum), 5 )),
            (100 * format_( (self._errNum / self._totalNum), 5 )) ) \
               + self._setTable( _one )
    
    def infoReport(self):
        
        return self._setTotalReport()



