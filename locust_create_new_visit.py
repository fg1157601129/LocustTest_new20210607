#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_create_new_visit.py
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

class CreateNewVisit(FastHttpUser):
    wait_time = between(0.1, 0.2)

    def on_start(self):

        #   公共参数
        self.host = 'https://power.medcloud.cn'   # 被测主机地址
        self.token = 'eee22d511a6e4da7aa7730c5918f92f2'
        self.uid = 2279
        self._ut = 1
        self._t = 1
        self._s = 11
        self.mtId = 553
        self.tenantId = 376
        self.cmtId = 546
        self.cmtType = 2
        self._lang = 'zh_CN'

        self.path_create_return_visit = f"/api/his/patient/return/visit/create?_token={self.token}&_uid={self.uid}&_ut={self._ut}&_t={self._t}&_s={self._s}&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang={self._lang}"


    @tag("patient")
    @task(1)
    #   新增回访
    def func_create_return_visit(self):

        # self.path_create_return_visit =
        # "/api/his/patient/return/visit/create"

        now_time = int(time.time()*1000)
        tag_str = fake.password(length=6)
        fake_num = random.randint(10000000000, 19999999999)


        payload_data = {
            "customerId": 3585075,
            "visitStatus": 3,
            "planVisitComment": "locust_FG",
            "planVisitTime": "2021-04-14T07:20:00.260Z",
            "planVisitorId": 2279,
            "planVisitorName": "李俊",
            "visitType": 3
        }

        with self.client.post(
            path=f'{self.path_create_return_visit}',
            headers=None, json=payload_data , catch_response=True,name="新增回访:/api/his/patient/return/visit/create") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        #raise RescheduleTask()
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_create_return_visit)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_create_return_visit)


#   还需【确认入库】
#   /api/his/physical/inventory/input/update/confirm
if __name__ == "__main__":

    """
    @tag修饰符主要是用例管理测试方法的执行，在测试方法上加上一个或者多个@tag修饰符，就可以在执行测试时通过@tag修饰符运行指定测试集合，而且它不会影响全局的任务收集。

    在执行测试时，使用 -T 或者 -E 来挑选测试集合

    -T 选中的集合

    -E 排除选中的集合
    """

    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    os.system("locust -f locust_create_new_visit.py --host=172.18.2.29 --master")
    #os.system("locust -f locust_h5.py --host=http://localhost -T physical_demo")
    #locust -f locust_create_new_visit.py --worker --master-host=172.18.2.29-port=8089
    #os.system("locust -f locust_zadan.py --host=192.168.90.164")