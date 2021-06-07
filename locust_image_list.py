#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_image_list.py
# @Software: PyCharm
from json import JSONDecodeError
import json
from locust import HttpUser,task,TaskSet,SequentialTaskSet,between,tag
from locust.contrib.fasthttp import FastHttpUser,ResponseContextManager,FastResponse
import os
import random
import time
from locust.exception import RescheduleTask
from faker import Faker

fake = Faker(locale="zh_CN")

class TeethImageList(FastHttpUser):
    wait_time = between(0.1, 0.2)

    def on_start(self):

        #   公共参数
        self.host = 'https://pre-power.medcloud.cn'   # 被测主机地址
        self.token = '5d56d1a9d412491383a5c40fa7fa83ec'
        self.uid = 2681
        self._ut = 1
        self._t = 1
        self._s = 11
        self.mtId = 625
        self.tenantId = 452
        self.cmtId = 625
        self.cmtType = 2
        self._lang = 'zh_CN'
        self.imageType = ''
        self.teethImageStatus = ''
        self.toothPosition = ''
        self.toothPositionStr = ''
        self.patientId = 33256
        self.path_teeth_image_list = "/api/his/diagnosis/teeth-image/list"


    @tag("diagnosis")
    @task(1)
    #   影像列表
    def func_teeth_image_list(self):

        # self.path_teeth_image_list =
        # "/api/his/diagnosis/teeth-image/list"

        now_time = int(time.time()*1000)
        tag_str = fake.password(length=6)
        fake_num = random.randint(10000000000, 19999999999)

        payload_data ={
            '_token': self.token,
            '_uid': self.uid,
            '_ut': self._ut,
            '_t': self._t,
            '_s': self._s,
            '_mtId': self.mtId,
            '_tenantId': self.tenantId,
            '_cmtType': self.cmtType,
            '_lang': self._lang,
            'imageType':self.imageType,
            'teethImageStatus': self.teethImageStatus,
            'toothPosition': self.toothPosition,
            'toothPositionStr': self.toothPositionStr,
            'patientId': self.patientId
        }
        # with self.client.post("/", json={"foo": 42, "bar": None}, catch_response=True) as response:
        #     try:
        #         if response.json()["greeting"] != "hello":
        #             response.failure("Did not get expected value in greeting")
        #     except JSONDecodeError:
        #         response.failure("Response could not be decoded as JSON")
        #     except KeyError:
        #         response.failure("Response did not contain expected key 'greeting'")

        with self.client.post(
            path=f'{self.path_teeth_image_list}',
            headers=None, data=payload_data , catch_response=True,name="/api/his/diagnosis/teeth-image/list") as res:
            if res.status_code == 200:
                if (json.loads(res.text))["code"] == 0:
                    res.success()
                else:
                    #raise RescheduleTask()
                    res.failure(res.text)
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_teeth_image_list)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_teeth_image_list)


#   还需【确认入库】
#   /api/his/physical/inventory/input/update/confirm
if __name__ == "__main__":
    import os
    """
    @tag修饰符主要是用例管理测试方法的执行，在测试方法上加上一个或者多个@tag修饰符，就可以在执行测试时通过@tag修饰符运行指定测试集合，而且它不会影响全局的任务收集。

    在执行测试时，使用 -T 或者 -E 来挑选测试集合

    -T 选中的集合

    -E 排除选中的集合
    """

    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    os.system("locust -f locust_image_list.py --host=http://localhost")
    #os.system("locust -f locust_h5.py --host=http://localhost -T physical_demo")

    #os.system("locust -f locust_zadan.py --host=192.168.90.164")