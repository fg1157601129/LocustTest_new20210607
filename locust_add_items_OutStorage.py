#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_add_items_OutStorage.py
# @Software: PyCharm

import random

import json
import os
import time

from faker import Faker
from locust import HttpUser,task,TaskSet,SequentialTaskSet,between,tag
from locust.contrib.fasthttp import FastHttpUser,ResponseContextManager,FastResponse
from locust.exception import RescheduleTask


fake = Faker(locale="zh_CN")

class ItemsOutStorage(FastHttpUser):
    wait_time = between(0.1, 0.2)

    def on_start(self):

        #   公共参数
        self.host = 'https://pre-power.medcloud.cn'   # 被测主机地址
        self.token = '3d5689e5b38f49ceac4c1dedc1c2bbd5'
        self.uid = 2681
        self._ut = 1
        self._t = 1
        self._s = 11
        self.mtId = 665
        self.tenantId = 452
        self.cmtId = 625
        self.cmtType = 2
        self._lang = 'zh_CN'

        self.path_add_items_outstorage = f"/api/his/physical/inventory/output/create?_token={self.token}" \
                                         f"&_uid={self.uid}&_ut={self._ut}&_t={self._t}&_s={self._s}&_mtId={self.mtId}" \
                                         f"&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}" \
                                         f"&_lang={self._lang}"


    @tag("physical")
    @task(1)
    #   新增物品出库
    def func_add_items_outstorage(self):

        # self.path_add_items_outstorage =
        # "/api/his/physical/inventory/output/create"

        payload_data ={
            "0": {
                "memo": "locust_20210408"
            },
            "outputInventoryType": 2,
            "medicalInstitutionId": 665,
            "medicalReceiveDepartment": "李俊",
            "outputInventoryOrderItemCreateList": [
                {
                    "merchandiseId": 1367,
                    "merchandiseNo": "I202103310006",
                    "merchandiseInventoryId": 18169,
                    "outputInventoryNum": 1,
                    "memo": "locust_20210408"
                }
            ]
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
            path=f'{self.path_add_items_outstorage}',
            headers=None, json=payload_data , catch_response=True,name="新增物品出库") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        #raise RescheduleTask()
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_items_outstorage)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_items_outstorage)

# 还需【出库确认】
# "/api/his/physical/inventory/output/confirm"

if __name__ == "__main__":

    """
    @tag修饰符主要是用例管理测试方法的执行，在测试方法上加上一个或者多个@tag修饰符，就可以在执行测试时通过@tag修饰符运行指定测试集合，而且它不会影响全局的任务收集。

    在执行测试时，使用 -T 或者 -E 来挑选测试集合

    -T 选中的集合

    -E 排除选中的集合
    """

    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_demo1.py --web-host=127.0.0.1")
    os.system("locust -f locust_add_items_OutStorage.py --host=http://localhost")
    #os.system("locust -f locust_h5.py --host=http://localhost -T physical_demo")

    #os.system("locust -f locust_zadan.py --host=192.168.90.164")