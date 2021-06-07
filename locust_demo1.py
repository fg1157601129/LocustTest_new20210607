#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/3/12 11:58
# @Author : Aries
# @Site :
# @File : locust_demo1.py
# @Software: PyCharm
import random
from locust import HttpUser, TaskSet, task
from locust.clients import HttpSession
# import pysnooper
import base64
import json
import time
import hashlib
import queue
import hmac
import os
import requests

def bs64_en(data):
    bytes_data = json.dumps(data).encode("utf-8")
    result_data = str(base64.b64encode(bytes_data),"utf-8")
    return result_data

def bs64_de(data):
    temp = str(base64.b64decode(data),"utf-8")
    return temp

def get_timestamp1():
    return str(int(time.time()))

def md5a(md5str=None):
    h1 = hashlib.md5()
    h1.update(md5str.encode(encoding="utf-8"))
    return h1.hexdigest()

def sign_alg(str_a,secuyrity):
    r_str_a = bytes((str_a).encode('utf-8'))
    r_secuyrity = bytes((secuyrity).encode('utf-8'))

    sign = (hmac.new(r_secuyrity,r_str_a,digestmod=hashlib.sha256)).hexdigest().upper()
    return sign


# 随机生成3-10个中文字符
def nickname_random():
    nick_name = ""
    for i in range(random.randint(3,10)):
        val = chr(random.randint(0x4e00, 0x9fbf))
        nick_name += val
    return nick_name

class ZhaoyuLogin(TaskSet):

    host = "http://qx-fat.qianshi188.com"

    #  替换数据

    def on_start(self):

        print("--------------------   Test start   --------------------")

    def on_stop(self):
        print("--------------------   Test over   --------------------")

    @task(1)
    #@pysnooper.snoop("D:\zhaoyulocust.log")

    # 注册登录
    def login_user(self):

        self.timestamp = get_timestamp1()
        self.login_url = "/gateway/customer/customer/registerLogin"

        try:
            self.user_data = self.locust.queue_data.get()  # 从队列中取出user赋值给user_data
            print(self.user_data)

        except queue.Empty:
            print("数据为空了......")
            exit()

        # base_data
        self.channel_1 = "android"
        self.machinecode_1 = "A000009C1C1FA3"
        self.send_code_service = "sms.send"
        self.login_service = "oauth.login"
        self.token_1 = ""
        self.version_1 = "v1.0"
        self.key_1 = "40a406d77d1b2ecc"

        self.send_code_data = {
            "Mobile":self.user_data,
            'SendType': 1
        }
        self.r_send_code_data = bs64_en(self.send_code_data)

        self.base_sign1 = "channel=" + self.channel_1 + "&data=" + self.r_send_code_data + \
                          "&machinecode=" + self.machinecode_1 + "&service=" + self.send_code_service + \
                          "&timestamp=" + self.timestamp + "&token=" + self.token_1 + "&version=" + \
                          self.version_1 + "&key=" + self.key_1

        self.sign1 = md5a(self.base_sign1)

        # result_data
        self.result_send_code_data = {
            "channel": self.channel_1,
            "data": self.r_send_code_data,
            "machinecode": self.machinecode_1,
            "service": self.send_code_service,
            "timestamp": self.timestamp,
            "token": self.token_1,
            "version": self.version_1,
            "sign": self.sign1
        }

        response1 = HttpSession(base_url=self.host).request(method='post',url=self.login_url,json=self.result_send_code_data,
                                                            headers=None,catch_response=False)
        print("Response content1:", response1.text, self.result_send_code_data)

        self.login_data = {
            "Mobile":self.user_data,
            "Code": "666666",
            "Longitude": "1223.232",
            "Latitude": "232.232"
        }
        self.r_login_data = bs64_en(self.login_data)

        self.base_sign2 = "channel=" + self.channel_1 + "&data=" + self.r_login_data + \
                          "&machinecode=" + self.machinecode_1 + "&service=" + self.login_service + \
                          "&timestamp=" + self.timestamp + "&token=" + self.token_1 + "&version=" + \
                          self.version_1 + "&key=" + self.key_1
        self.sign2 = md5a(self.base_sign2)

        self.result_login_data = {
            "channel": self.channel_1,
            "data": self.r_login_data,
            "machinecode": self.machinecode_1,
            "service": self.login_service,
            "timestamp": self.timestamp,
            "token": self.token_1,
            "version": self.version_1,
            "sign": self.sign2
        }

        response2 = HttpSession(base_url=self.host).request(method='post', url=self.login_url, json=self.result_login_data,
                                                      headers=None, catch_response=False)

        #with self.client.post("http://210.22.78.174:809/api/gateway",)
        print("Response content2:",response2.text,self.result_login_data)
    #
    #     #assert  200 == response1.status_code

    @task(1)
    # 完善DNA
    def edit_user_profile(self):
        self.edit_user_profile_url = ":80/api/gateway"
        self.edit_user_profile_data = {
            "NickName" : nickname_random(),
            "PhotoGraph":"http://imgcdn.zhaoyugf.com/FmWaTF5CbhwfxXQBhKgFvdMbGob6",
            "Gender":random.randint(1,2)
        }
        self.channel_2 = "android"
        self.machinecode_2 = "A000009C1C1FA3"
        self.edit_user_profile_service = "user.editbase"
        self.token_2 = random.choice(self.user_token)
        self.version_2 = "v1.0"
        self.key_2 = "40a406d77d1b2ecc"
        self.r_edit_user_profile_data = bs64_en(self.edit_user_profile_data)
        self.timestamp_2 = get_timestamp1()

        self.base_sign3 = "channel=" + self.channel_2 + "&data=" + self.r_edit_user_profile_data + "&machinecode=" + self.machinecode_2\
                          + "&service=" + self.edit_user_profile_service + "&timestamp=" + self.timestamp_2 + \
                          "&token=" + self.token_2 + "&version=" + self.version_2 + "&key=" + self.key_2

        self.sign3 = md5a(self.base_sign3)

        self.result_edit_user_profile_data = {
            "channel": self.channel_2,
            "data": self.r_edit_user_profile_data,
            "machinecode": self.machinecode_2,
            "service": self.edit_user_profile_service,
            "timestamp": self.timestamp_2,
            "token": self.token_2,
            "version": self.version_2,
            "sign": self.sign3
        }


        response3 = HttpSession(base_url=self.host).request(method='post', url=self.edit_user_profile_url,
                                                                             json=self.result_edit_user_profile_data,
                                                                             headers=None, catch_response=False)
        print("Response content3:", response3.text, self.result_edit_user_profile_data)

class Test_run(HttpUser):

    #task_set = ZhaoyuLogin

    queue_data = queue.Queue()   #实例化一个队列
    for i in range(200000):
        phone_num = str(14100000000 + i)
        print(phone_num)
        queue_data.put_nowait(phone_num)    #把每一个用户账号存到队列中
    task_set = ZhaoyuLogin
    min_wait = 0
    max_wait = 0


if __name__ == "__main__":
    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    os.system("locust -f locust_demo1.py --web-host=192.168.90.164")

    #os.system("locust -f locust_send_group_gift.py --host=192.168.99.110")

