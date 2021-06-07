#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/26 15:23 
# @Author : Aries 
# @Site :  
# @File : locust_send_group_gift.py 
# @Software: PyCharm

# -*- coding: utf-8 -*-

# @File    : locust.py
# @Date    : 2019-09-25-17:19
# @Author  : DanKeGeGe
# @Version : 1
import locust
from locust import HttpLocust, task, TaskSet
from locust.clients import HttpSession
from KelaEnum import UrlEnum
from Tool import Tool
import time
import hmac
import random
import hashlib

import yaml
import pandas as pd



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

class GiftGroup(TaskSet):  # TaskSet类

    @task(1)
    def send_group_gift1(self):
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
            "hammerNum": 1,
            "roomId": anchor_for_roomId,
            "isAllLook": 2
        }

        response = HttpSession(base_url=UrlEnum.KELA_CLUB_WEB.value).request(method='post',
                                                                             url="http://qx-fat.qianshi188.com/gateway/activity/smashEggsAward/eggSmashSubmit",
                                                                             json=smash_eggs_data,
                                                                             headers=header,
                                                                             catch_response=False)
        # print("Response content:", response.text)
        # assert 200 == response.status_code

    # @task(1)
    # def send_group_gift2(self):
    #     json_data = {
    #         "giftId": 546,
    #         "memberId": 208,
    #         "sendType": 3,
    #         "groupId": 614
    #     }
    #     response = HttpSession(base_url=UrlEnum.KELA_CLUB_WEB.value).request(method='post',
    #                                                                          url='/gift/sendGift',
    #                                                                          json=json_data,
    #                                                                          headers=Tool().headers(),
    #                                                                          catch_response=False)
        # print("Response content:", response.text)
        # assert 200 == response.status_code


class SendRedPacketLocust(HttpLocust):
    task_set = GiftGroup
    wait_time =(1,1)


if __name__ == "__main__":
    import os
    os.system("locust -f locust_send_group_gift.py --host=192.168.90.164")

    """
    四、启动Locust

1、如果启动的locust文件名为locustfile.py并位于当前工作目录中，可以在编译器中直接运行该文件，或者通过cmd，执行如下命令：

 locust --host=https://www.cnblogs.com 

2、如果Locust文件位于子目录下且名称不是locustfile.py，可以使用-f命令启动上面的示例locust文件：

  

3、如果要运行分布在多个进程中的Locust，通过指定-master以下内容来启动主进程 ：

 locust -f testscript/locusttest.py --master --host=https://www.cnblogs.com 

4、如果要启动任意数量的从属进程，可以通过-salve命令来启动locust文件：

 locust -f testscript/locusttest.py --salve --host=https://www.cnblogs.com 

5、如果要运行分布式Locust，必须在启动从机时指定主机（运行分布在单台机器上的Locust时不需要这样做，因为主机默认为127.0.0.1）：

 locust -f testscript/locusttest.py --slave --master-host=192.168.0.100 --host=https://cnblogs.com 

6、启动locust文件成功后，编译器控制台会显示如下信息：

 [2018-10-09 01:01:44,727] IMYalost/INFO/locust.main: Starting web monitor at *:8089

[2018-10-09 01:01:44,729] IMYalost/INFO/locust.main: Starting Locust 0.8 

PS：8089是该服务启动的端口号，如果是本地启动，可以直接在浏览器输入http://localhost:8089打开UI界面，如果是其他机器搭建locust服务，则输入该机器的IP+端口即可；
    """
