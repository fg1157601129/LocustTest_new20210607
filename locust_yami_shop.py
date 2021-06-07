#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/13 21:32
# @Author : fanggang
# @File : locust_yami_shop.py
# @Software: PyCharm
# -------------------------------
from locust import HttpUser,task,between,SequentialTaskSet,tag
from locust.clients import HttpSession
#from locust.contrib.fasthttp import FastHttpUser
import yaml

"""
定义一个任务类，这个类名称自己随便定义
类继承SequentialTaskSet 或 TaskSet类，所以要从locust中，引入
SequentialTaskSet 或 TaskSet
当类里面的任务请求有先后顺序时，继承SequentialTaskSet类
没有先后顺序，可以继承TaskSet类
"""



import time
import hmac
import random
import hashlib

def get_timestamp():
    return str(int((time.time())))

def sign_alg(str_a,security):
    r_str_a = bytes((str_a).encode('utf-8'))
    r_security = bytes((security).encode('utf-8'))

    sign = (hmac.new(r_security, r_str_a, digestmod=hashlib.sha256)).hexdigest().upper()
    return sign

class MyUser(SequentialTaskSet):

    #   初始化方法 相当于 setup
    def on_start(self):
        pass

    @task
    @tag("tag_one")
    def egg_Smash(self):
        yami_url = "https://test02qygateway.xiaoniuhy.com/gateway/gift/shop/order"
        self.headers = {
        "Origin": "http//h5.qingyinlive.com",
        "Content-Type": "application/json;charset=utf-8"
        }

        self.data = {"pid": 35,
                "amount": 1,
                "customerId": "2008131533114005357",
                "receiverId": "2008131533114005357"
                }

        self.client.post(yami_url, json=self.data, headers=self.headers, catch_response=True)
        with self.client.post(yami_url,json=self.data,headers=self.headers,catch_response=True) as rsp:
            print(rsp.text)

class SendRedPacketLocust(HttpUser):
    tasks = [MyUser]   #指定用户行为的类或者一组任务
    wait_time = between(1,2)

if __name__ == "__main__":
    import os
    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    os.system("locust -f locust_yami_shop.py --host=http://192.168.201.3")
    #os.system("locust -f locust_zadan.py --host=192.168.90.164")