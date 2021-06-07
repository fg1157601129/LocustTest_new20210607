#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/8/1 15:59
# @Author : fanggang
# @File : locust_zadan.py
# @Software: PyCharm
# -------------------------------


#from locust import TaskSet,HttpUser,between,task
#from locust import User, constant
from locust import HttpUser,task,between,SequentialTaskSet,tag,TaskSet
from locust.clients import HttpSession
from locust.contrib.fasthttp import FastHttpUser
#from locust.contrib.fasthttp import FastHttpUser
import yaml
import json
from faker import Faker
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
#
# import yaml
# import pandas as pd



def sign_alg(str_a,security):
    r_str_a = bytes((str_a).encode('utf-8'))
    r_security = bytes((security).encode('utf-8'))

    sign = (hmac.new(r_security, r_str_a, digestmod=hashlib.sha256)).hexdigest().upper()
    return sign


def hmac_sha256(key, appSecret):
    """
    hmacsha256加密
    return:加密结果转成16进制字符串形式
    """
    message = appSecret.encode('utf-8')
    sign = hmac.new(key.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
    # print(sign.upper())
    return sign.upper()

def key_str(appId_str):
    str_a = appId_str + str(int(time.time()))
    return str_a

def get_timestamp():
    return str(int((time.time())))
#appId = '1149954699146534912'

# 内置函数，性能最优
def user_data():
    user_list = list(range(15499990001,15499990127))
    return user_list

#   将数据写入yaml文件
def write_data_for_yaml(path,customerId_list,token_list,roomId_list,liveDetailId_list):
    yamlpath = "r" + "'" + path + "'"
    tokenValue = {
        "customerId":customerId_list,
        "token":token_list,
        "roomId":roomId_list,
        "liveDetailId":liveDetailId_list
    }
    with open(yamlpath,"w",encoding="utf-8") as f:
        yaml.dump(tokenValue,f)

#   读取yaml文件里得数据
def read_yaml_token_data():
    customerId_result = []
    token_result = []

    yamlpath = r'E:\xiaoniu_work\KLMBInterface\others\token.yaml'
    with open(yamlpath, "r", encoding="utf-8") as f:
        read_data_init = (yaml.load(f.read(), Loader=yaml.Loader))
        #print(read_data_init.keys())
        # print(read_data_init.values())
        for i in read_data_init.keys():
            if i == "customerId":
                customerId_result = read_data_init[i]
            elif i == "token":
                token_result = read_data_init[i]
        #     print(i)
        #     print(read_data_init[i])
        # print(customerId_result)
        # print(token_result)
    return customerId_result,token_result




appId = "1149960309183299584"
deviceId = "A17EFC0B198941CBA693915B5A0B4472"

appSecret = "1acdf792a54511e993fc506b4bbe1bc4"

def zadan(x):
    time_str = get_timestamp()
    str_a = appId + time_str
    pay_user = "339b859c445d417ea7aa75f3a9e6394e"
    anchor_for_roomId = "eggs100"
    url = "http://qx-fat.qianshi188.com/gateway/activity/smashEggsAward/eggSmashSubmit"

    header = {
        "request-id": "7B142B65-A3A4-4F63-8C90-50FB9ADB6817-1590994839806",
        "request-agent": "2",
        "device-id": "A17EFC0B198941CBA693915B5A0B4472",
        "os-version": "1",
        "phone-model": "iPhone11,6",
        "sdk-version": "13.4",
        "market": "app_store",
        "app-version": "1.0.0",
        "app-version-code": "100",
        "app-name": "1",
        "app-clone-name": "001",
        "biz-code": "/gateway/activity/smashEggsAward/eggSmashSubmit",
        "app-id": "1149960309183299584",
        "timestamp": get_timestamp(),
        "sign": sign_alg(str_a, appSecret),
        "customer-id": pay_user,
        "access-token": None,
        "gps-lng": "23.26",
        "gps-lat": "23.26",
        "Content-Type": "application/json;charset=utf-8"
    }
    smash_eggs_data = {
        "hammerNum": 66,
        "roomId": anchor_for_roomId,
        "isAllLook": 2
    }

    #r = x.client.post(url = url,header = header,data =smash_eggs_data)
    response = HttpSession(base_url=url).request(method='post',url=url,json=smash_eggs_data,headers=header,catch_response=False)
    print(response)


class MyUser(SequentialTaskSet):
    """
        用给定的标记名标记任务和任务集的装饰器。你可以

        然后将测试限制为只执行带有任何

        由:code: '——tags '命令行参数提供的标记。例如::

        class ForumPage(TaskSet):
                @tag('thread')
                @task(100)
                def read_thread(self):
                    pass

                @tag('thread')
                @tag('post')
                @task(7)
                def create_thread(self):
                    pass

                @tag('post')
                @task(11)
                def comment(self):
                    pass
        """

    #   初始化方法 相当于 setup
    # def on_start(self):
    #     pass


    #@tag("tag_one")
    @task(1)
    def egg_Smash(self):
        #url = "/api/his/patient/patient/page?_token=c7aecb230e4c43bf84a0503e2148dc73&_uid=2681&_ut=1&_t=1&_s=11&_mtId=665&_tenantId=452&_cmtId=625&_cmtType=2&_lang=zh_CN&dateType=1&doctorType=1&doctorId=&current=1&size=10"
        url = "/api/his/pay/merchant-info/list"
        data = {'_token':'c7aecb230e4c43bf84a0503e2148dc73',
               '_uid':2279,
               '_ut':1,
               '_t':1,
               '_s':11,
               '_mtId':553,
               '_tenantId':376,
               '_cmtId':546,
               '_cmtType':2,
                '_lang':'zh_CN'
                }
        res = self.client.get(path=url, params=data,json=None, headers=None, catch_response=False)
        #res = self.client.get(path=url, json=None, headers=None, catch_response=False)
        print((json.loads(res.text))["code"])
        print(res.text)
        # try:
        #     assert  (json.loads(res.text))["code"] == 0
        #     print(res.text)
        #     print(get_timestamp(),"通过")
        # except Exception as err:
        #     print(res.text)
        #     print(get_timestamp(),"失败")

        # with self.client.post(url,json=self.smash_eggs_data,headers=self.headers,catch_response=True) as rsp:
        #     print(rsp.text)



    # tasks = zadan()
    # wait_time = constant(1)
    # def index(self):
    #     #res = self.client.get("www.baidu.com")
    #     zadan(self)

class SendRedPacketLocust(FastHttpUser):

    tasks = [MyUser]   #指定用户行为的类或者一组任务
    wait_time = between(0.1, 0.2)
    #host = "https://pre-power.medcloud.cn/"   # 被测主机地址

if __name__ == "__main__":
    import os
    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    os.system("locust -f locust_patient_create.py --host=http://localhost")
    #os.system("locust -f locust_zadan.py --host=192.168.90.164")

