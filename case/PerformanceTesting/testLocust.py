# -*- coding:utf-8 -*-
__author__ = 'zeding'
__mtime__ = '2017/11/21'

from locust import HttpLocust ,TaskSet,task

#脚本增强无非就要涉及到四个方面
# 关联
# 参数化
# 检查点
# 集合点





#两种方式
class UserBehavior(TaskSet):
    
    @task(1)
    def login(self):
        self.client.get()

    @task( 2 )
    def login2(self):
        self.client.get()