#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_update_items_PutInStorage.py
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

class UpdateItemsPutInStorage(FastHttpUser):
    wait_time = between(0.1, 0.2)

    def on_start(self):

        #   公共参数
        self.host = 'https://pre-power.medcloud.cn'   # 被测主机地址
        self.token = 'b685646b25f140febbaa376f82d6b34c'
        self.uid = 2681
        self._ut = 1
        self._t = 1
        self._s = 11
        self.mtId = 665
        self.tenantId = 452
        self.cmtId = 625
        self.cmtType = 2
        self._lang = 'zh_CN'

        self.path_update_items_putinstorage = f"/api/his/physical/inventory/input/update?_token={self.token}&_uid={self.uid}&_ut={self._ut}&_t={self._t}&_s={self._s}&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang={self._lang}"


    @tag("physical")
    @task(1)
    #   修改物品入库
    def func_update_items_putinstorage(self):

        # self.path_update_items_putinstorage =
        # "/api/his/physical/inventory/input/update

        fake_num = random.randint(1,10000)
        payload_data ={
            "inputInventoryType": 1,
            "medicalInstitutionId": "665",
            "merchandiseSupplierId": 142,
            "createTime": "2021-04-08T03:51:25.000Z",
            "inputInventoryTotalAmount": fake_num,
            "inputInventoryOrderItemCreateList": [
                {
                    "_index": "uxw5go",
                    "aliasName": "非OTC药品",
                    "availableNum": 0,
                    "chainMedicalInstitutionId": 625,
                    "commonName": "非OTC药品",
                    "createTime": "2021-04-08T05:28:58.000Z",
                    "expireTime": "2021-04-08T05:28:32.000Z",
                    "inputInventoryNum": 1,
                    "inputInventoryTotalAmount": fake_num,
                    "inputInventoryUnitAmount": 1,
                    "inventoryNum": 1,
                    "inventoryUnitStr": "袋",
                    "itemPrice": fake_num,
                    "itemQuantity": 1,
                    "medicalInstitutionId": 665,
                    "merchandise": {
                        "aliasName": "非OTC药品",
                        "aliasNamePinyin": "feiotcyaopin",
                        "aliasNamePy": "fotcyp",
                        "commonName": "非OTC药品",
                        "commonNamePinyin": "feiotcyaopin",
                        "commonNamePy": "fotcyp",
                        "costAmount": 0,
                        "dosageFrom": 3,
                        "freezeInventoryNum": 0,
                        "inventoryNum": 0,
                        "inventoryUnitId": 61706,
                        "isSale": True,
                        "merchandiseCategoryOneId": 111,
                        "merchandiseId": 1367,
                        "merchandiseNo": "I202103310006",
                        "merchandiseType": 1,
                        "prescriptionDosage": 0,
                        "prescriptionDosageUnit": 2,
                        "prescriptionDrugUsage": 1,
                        "prescriptionFrequency": 2,
                        "prescriptionTotal": 0,
                        "prescriptionTotalUnit": 1,
                        "purchaseUnitId": 61706,
                        "retailAmount": 5.67,
                        "specifications": "500ml",
                        "systemInner": 2,
                        "systemInnerId": 1365,
                        "unitSystem": 1
                    },
                    "merchandiseId": 1367,
                    "merchandiseInputInventoryOrderId": "1255",
                    "merchandiseInputInventoryOrderItemId": "2724",
                    "merchandiseInputInventoryOrderNo": "IN665202104080107",
                    "merchandiseNo": "I202103310006",
                    "modelOrDosageFormStr": "口服酊膏剂",
                    "producedBatchNo": "locust_20210408",
                    "producedTime": "2021-04-08T05:28:32.000Z",
                    "purchaseUnitIdStr": "袋",
                    "retailAmount": 1,
                    "specifications": "500ml",
                    "specificationsStr": "500ml*1袋/袋",
                    "unitSystem": 1,
                    "memo": None
                }
            ],
            "merchandiseInputInventoryOrderNo": "IN665202104080107",
            "merchandiseInputInventoryOrderId": 1255,
            "memo": "update_locust"
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
            path=f'{self.path_update_items_putinstorage}',
            headers=None, json=payload_data , catch_response=True) as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        #raise RescheduleTask()
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_update_items_putinstorage)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_update_items_putinstorage)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_update_items_putinstorage)

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
    os.system("locust -f locust_update_items_PutInStorage.py --host=http://localhost")
    #os.system("locust -f locust_h5.py --host=http://localhost -T physical_demo")

    #os.system("locust -f locust_zadan.py --host=192.168.90.164")