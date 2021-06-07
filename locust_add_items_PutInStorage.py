#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_add_items_PutInStorage.py
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

class ItemsPutInStorage(FastHttpUser):
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

        self.path_add_items_putinstorage = f"/api/his/physical/inventory/input/create?_token={self.token}&_uid={self.uid}&_ut={self._ut}&_t={self._t}&_s={self._s}&_mtId={self.mtId}&_tenantId={self.tenantId}&_cmtId={self.cmtId}&_cmtType={self.cmtType}&_lang={self._lang}"


    @tag("physical")
    @task(1)
    #   新增物品入库
    def func_add_items_putinstorage(self):

        # self.path_add_items_putinstorage =
        # "/api/his/physical/inventory/input/create"

        payload_data = {
            "inputInventoryType": random.randint(1,3),
            "merchandiseSupplierId": 142,
            "medicalInstitutionId": 665,
            "inputInventoryOrderItemCreateList": [
                {
                    "aliasName": "非OTC药品",
                    "aliasNamePinyin": "feiotcyaopin",
                    "aliasNamePy": "fotcyp",
                    "availableNum": 0,
                    "avgUnitPrice": 0,
                    "brandName": "",
                    "commonName": "非OTC药品",
                    "commonNamePinyin": "feiotcyaopin",
                    "commonNamePy": "fotcyp",
                    "costAmount": 0,
                    "dosageFrom": 3,
                    "freezeInventoryNum": 0,
                    "hasBatchInformation": False,
                    "inventoryNum": 0,
                    "inventoryUnitId": 61706,
                    "inventoryUnitStr": "袋",
                    "isExistNoFreezeBatch": False,
                    "isSale": True,
                    "merchandiseCategoryOneId": 111,
                    "merchandiseCategoryOneName": "食品",
                    "merchandiseCategoryThreeName": "",
                    "merchandiseCategoryTwoName": "",
                    "merchandiseId": 1367,
                    "merchandiseNo": "I202103310006",
                    "merchandiseQualificationInformationArray": [

                    ],
                    "merchandiseType": 1,
                    "modelOrDosageFormStr": "口服酊膏剂",
                    "prescriptionDosageUnit": 2,
                    "prescriptionDrugUsage": 1,
                    "prescriptionFrequency": 2,
                    "prescriptionTotalUnit": 1,
                    "purchaseUnitId": 61706,
                    "purchaseUnitIdStr": "袋",
                    "retailAmount": 5.67,
                    "specifications": "500ml",
                    "specificationsStr": "500ml*1袋/袋",
                    "systemInner": 2,
                    "systemInnerId": 1365,
                    "totalInventoryAmount": 0,
                    "totalInventoryNum": 0,
                    "unitSystem": 1,
                    "_index": 0.011256758590106886,
                    "inputInventoryNum": 1,
                    "itemQuantity": 1,
                    "itemPrice": 11,
                    "inputInventoryTotalAmount": 11,
                    "producedBatchNo": "locust_20210408",
                    "producedTime": None,
                    "expireTime": None,
                    "memo": None
                }
            ],
            "inputInventoryTotalAmount": 11,
            "memo": "locust"
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
            path=f'{self.path_add_items_putinstorage}',
            headers=None, json=payload_data , catch_response=True,name="新增物品入库") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        #raise RescheduleTask()
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_items_putinstorage)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_items_putinstorage)


#   还需【确认入库】
#   /api/his/physical/inventory/input/update/confirm
if __name__ == "__main__":


    os.system("locust -f locust_add_items_PutInStorage.py --host=http://localhost")
    """
    @tag修饰符主要是用例管理测试方法的执行，在测试方法上加上一个或者多个@tag修饰符，就可以在执行测试时通过@tag修饰符运行指定测试集合，而且它不会影响全局的任务收集。

    在执行测试时，使用 -T 或者 -E 来挑选测试集合

    -T 选中的集合

    -E 排除选中的集合
    """

    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py


