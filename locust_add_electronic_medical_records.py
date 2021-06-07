#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_add_electronic_medical_records.py
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

class AddElectronicMedicalRecords(FastHttpUser):
    wait_time = between(0.1, 0.2)

    def on_start(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        #   公共参数
        self.host = 'https://pre-power.medcloud.cn'   # 被测主机地址
        self.token = '266749c0745f4ae7ad89ceb6d63b9f07'
        self.uid = 2681
        self._ut = 1
        self._t = 1
        self._s = 11
        self.mtId = 665
        self.tenantId = 452
        self.cmtId = 625
        self.cmtType = 2
        self._lang = 'zh_CN'

        self.path_add_electronic_medical_records = '/api/his/diagnosis/medical-record/insert'


    @tag("physical")
    @task(1)
    #   新增电子病例
    def func_add_electronic_medical_records(self):

        # self.path_add_electronic_medical_records =
        # '/api/his/diagnosis/medical-record/insert'

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
            '_tenantId': self.cmtType,
            '_cmtId': self.cmtId,
            '_cmtType': self.cmtType,
            '_lang': self._lang,
            'medicalRecordVOJson':json.dumps({
    "registerId":44059,
    "registerTime":1617961209000,
    "doctorStaffId":3563,
    "visType":2,
    "mainComplaint":"红肿，松动，掉落",
    "medicalRecordCheckNormalVOList":[
        {
            "key":"943c5b7f-3440-1009-6895-587da931a071",
            "checkNormalSymptoms":"很健康",
            "checkNormalToothPosition":'{"teeth":{"11":true,"12":true,"13":true,"14":true,"15":true,"16":true,"17":true,"18":true,"21":true,"22":true,"23":true,"24":true,"25":true,"26":true,"27":true,"28":true,"31":true,"32":true,"33":true,"34":true,"35":true,"36":true,"37":true,"38":true,"41":true,"42":true,"43":true,"44":true,"45":true,"46":true,"47":true,"48":true,"51":true,"52":true,"53":true,"54":true,"55":true,"61":true,"62":true,"63":true,"64":true,"65":true,"71":true,"72":true,"73":true,"74":true,"75":true,"81":true,"82":true,"83":true,"84":true,"85":true},"activatedToothNumber":48,"activatedPartialList":[]}'
        }
    ],
    "medicalRecordCheckRayVOList":[
        {
            "key":"1ddfcebe-5338-8529-30a0-a8b439365bcc",
            "checkRaySymptoms":"我用激光治疗，CT检查",
            "checkRayToothPosition":'{"teeth":{"11":true,"12":true,"13":true,"14":true,"15":true,"16":true,"17":true,"18":true,"21":true,"22":true,"23":true,"24":true,"25":true,"26":true,"27":true,"28":true,"31":true,"32":true,"33":true,"34":true,"35":true,"36":true,"37":true,"38":true,"41":true,"42":true,"43":true,"44":true,"45":true,"46":true,"47":true,"48":true,"51":true,"52":true,"53":true,"54":true,"55":true,"61":true,"62":true,"63":true,"64":true,"65":true,"71":true,"72":true,"73":true,"74":true,"75":true,"81":true,"82":true,"83":true,"84":true,"85":true},"activatedToothNumber":48,"activatedPartialList":[]}'
        }
    ],
    "medicalRecordDiagnosisVOList":[
        {
            "key":"b0df2698-2304-1b1d-b722-9047a7cc115a",
            "diagnosisDesc":"牙齿老化",
            "diagnosisPosition":'{"teeth":{"11":true,"12":true,"13":true,"14":true,"15":true,"16":true,"17":true,"18":true,"21":true,"22":true,"23":true,"24":true,"25":true,"26":true,"27":true,"28":true,"31":true,"32":true,"33":true,"34":true,"35":true,"36":true,"37":true,"38":true,"41":true,"42":true,"43":true,"44":true,"45":true,"46":true,"47":true,"48":true,"51":true,"52":true,"53":true,"54":true,"55":true,"61":true,"62":true,"63":true,"64":true,"65":true,"71":true,"72":true,"73":true,"74":true,"75":true,"81":true,"82":true,"83":true,"84":true,"85":true},"activatedToothNumber":48,"activatedPartialList":[]}'
        }
    ],
    "medicalRecordTreatmentProgramVOList":[
        {
            "key":"f046b43f-fc94-4dcc-000a-dea6c04df582",
            "treatmentProgram":"需要持续观察",
            "treatmentProgramPosition":'{"teeth":{"11":true,"12":true,"13":true,"14":true,"15":true,"16":true,"17":true,"18":true,"21":true,"22":true,"23":true,"24":true,"25":true,"26":true,"27":true,"28":true,"31":true,"32":true,"33":true,"34":true,"35":true,"36":true,"37":true,"38":true,"41":true,"42":true,"43":true,"44":true,"45":true,"46":true,"47":true,"48":true,"51":true,"52":true,"53":true,"54":true,"55":true,"61":true,"62":true,"63":true,"64":true,"65":true,"71":true,"72":true,"73":true,"74":true,"75":true,"81":true,"82":true,"83":true,"84":true,"85":true},"activatedToothNumber":48,"activatedPartialList":[]}'
        }
    ],
    "medicalRecordDisposeVOList":[
        {
            "key":"60baaa2c-3461-fb83-90cb-56fc27c9e0bd",
            "dispose":"先吃点药",
            "disposePosition":'{"teeth":{"11":true,"12":true,"13":true,"14":true,"15":true,"16":true,"17":true,"18":true,"21":true,"22":true,"23":true,"24":true,"25":true,"26":true,"27":true,"28":true,"31":true,"32":true,"33":true,"34":true,"35":true,"36":true,"37":true,"38":true,"41":true,"42":true,"43":true,"44":true,"45":true,"46":true,"47":true,"48":true,"51":true,"52":true,"53":true,"54":true,"55":true,"61":true,"62":true,"63":true,"64":true,"65":true,"71":true,"72":true,"73":true,"74":true,"75":true,"81":true,"82":true,"83":true,"84":true,"85":true},"activatedToothNumber":48,"activatedPartialList":[]}'
        }
    ],
    "doctorAdvice":"一定要早晚记得刷牙",
    "createRegister":False,
    "medicalRecordRegisterVO":{
        "visType":2,
        "registerTime":1617961209000,
        "createRegister":False,
        "doctorStaffId":3563
    },
    "medicalInstitutionId":665,
    "patientId":33256,
    "medicalRecordId":None,
    "presentIllnessHistory":None,
    "pastIllnessHistory":None
}),
            'registerPatientToothSymptomLoadMedicalRecordJson': json.dumps({}),
            'registerPatientToothSymptomDisposeDTOListJson': json.dumps({})
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
            path=self.path_add_electronic_medical_records,
            headers=None, data=payload_data , catch_response=True,name="新增电子病例") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        #raise RescheduleTask()
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_electronic_medical_records)
                else:
                    res.failure("接口未返回任何数据！")
                    print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_electronic_medical_records)
            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_add_electronic_medical_records)



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
    os.system("locust -f locust_add_electronic_medical_records.py --host=http://localhost")
    #os.system("locust -f locust_h5.py --host=http://localhost -T physical_demo")

    #os.system("locust -f locust_zadan.py --host=192.168.90.164")