#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_update_electronic_medical_records.py
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

class UpdateElectronicMedicalRecords(FastHttpUser):
    wait_time = between(0.1, 0.2)

    def on_start(self):

        #   公共参数
        self.host = 'https://pre-power.medcloud.cn'   # 被测主机地址
        self.token = '5d56d1a9d412491383a5c40fa7fa83ec'
        self.uid = 2681
        self._ut = 1
        self._t = 1
        self._s = 11
        self.mtId = 665
        self.tenantId = 452
        self.cmtId = 625
        self.cmtType = 2
        self._lang = 'zh_CN'

        self.path_update_electronic_medical_records = '/api/his/diagnosis/medical-record/update'


    @tag("physical")
    @task(1)
    #   更新电子病例
    def func_update_electronic_medical_records(self):

        # self.path_update_electronic_medical_records =
        # '/api/his/diagnosis/medical-record/update'

        now_time = int(time.time()*1000)
        tag_str = fake.password(length=6)
        fake_num = random.randint(10000000000, 19999999999)


        payload_data ={
            '_token': self.token,
            '_uid': '2681',
            '_ut': '1',
            '_t': '1',
            '_s': '11',
            '_mtId': 665,
            '_tenantId': 452,
            '_cmtId': 625,
            '_cmtType': 2,
            '_lang': 'zh_CN',
            'medicalRecordVOJson':json.dumps({"registerId": 43127, "registerTime": 1617947464000, "doctorStaffId": 3563, "visType": 1,
                 "mainComplaint": "红肿，松动，掉落，抛光", "presentIllnessHistory": "病史1，病史2，病史3", "pastIllnessHistory": "轻微出血",
                 "medicalRecordCheckNormalVOList": [
                     {"key": "b101a9ef-ac48-323e-fab1-e03fca6f20ec", "checkNormalSymptoms": "很健康",
                      "checkNormalToothPosition": "{\"teeth\":{\"11\":true,\"12\":true,\"13\":true,\"14\":true,\"15\":true,\"16\":true,\"17\":true,\"18\":true,\"21\":true,\"22\":true,\"23\":true,\"24\":true,\"25\":true,\"26\":true,\"27\":true,\"28\":true,\"31\":true,\"32\":true,\"33\":true,\"34\":true,\"35\":true,\"36\":true,\"37\":true,\"38\":true,\"41\":true,\"42\":true,\"43\":true,\"44\":true,\"45\":true,\"46\":true,\"47\":true,\"48\":true,\"51\":true,\"52\":true,\"53\":true,\"54\":true,\"55\":true,\"61\":true,\"62\":true,\"63\":true,\"64\":true,\"65\":true,\"71\":true,\"72\":true,\"73\":true,\"74\":true,\"75\":true,\"81\":true,\"82\":true,\"83\":true,\"84\":true,\"85\":true},\"activatedToothNumber\":48,\"activatedPartialList\":[]}"}],
                 "medicalRecordCheckRayVOList": [
                     {"key": "2f912f7b-ee5b-d12f-9b4a-5297824f438a", "checkRaySymptoms": "CT检查",
                      "checkRayToothPosition": "{\"teeth\":{\"11\":true,\"12\":true,\"13\":true,\"14\":true,\"15\":true,\"16\":true,\"17\":true,\"18\":true,\"21\":true,\"22\":true,\"23\":true,\"24\":true,\"25\":true,\"26\":true,\"27\":true,\"28\":true,\"31\":true,\"32\":true,\"33\":true,\"34\":true,\"35\":true,\"36\":true,\"37\":true,\"38\":true,\"41\":true,\"42\":true,\"43\":true,\"44\":true,\"45\":true,\"46\":true,\"47\":true,\"48\":true,\"51\":true,\"52\":true,\"53\":true,\"54\":true,\"55\":true,\"61\":true,\"62\":true,\"63\":true,\"64\":true,\"65\":true,\"71\":true,\"72\":true,\"73\":true,\"74\":true,\"75\":true,\"81\":true,\"82\":true,\"83\":true,\"84\":true,\"85\":true},\"activatedToothNumber\":48,\"activatedPartialList\":[]}"}],
                 "medicalRecordDiagnosisVOList": [
                     {"key": "a3f5e8d1-ce91-6f12-ae96-3bf228d194ff", "diagnosisDesc": "牙齿老化",
                      "diagnosisPosition": "{\"teeth\":{\"11\":true,\"12\":true,\"13\":true,\"14\":true,\"15\":true,\"16\":true,\"17\":true,\"18\":true,\"21\":true,\"22\":true,\"23\":true,\"24\":true,\"25\":true,\"26\":true,\"27\":true,\"28\":true,\"31\":true,\"32\":true,\"33\":true,\"34\":true,\"35\":true,\"36\":true,\"37\":true,\"38\":true,\"41\":true,\"42\":true,\"43\":true,\"44\":true,\"45\":true,\"46\":true,\"47\":true,\"48\":true,\"51\":true,\"52\":true,\"53\":true,\"54\":true,\"55\":true,\"61\":true,\"62\":true,\"63\":true,\"64\":true,\"65\":true,\"71\":true,\"72\":true,\"73\":true,\"74\":true,\"75\":true,\"81\":true,\"82\":true,\"83\":true,\"84\":true,\"85\":true},\"activatedToothNumber\":48,\"activatedPartialList\":[]}"}],
                 "medicalRecordTreatmentProgramVOList": [
                     {"key": "e76352a0-1fcf-66e6-2c0d-11e4356f41bf", "treatmentProgram": "需要持续观察",
                      "treatmentProgramPosition": "{\"teeth\":{\"11\":true,\"12\":true,\"13\":true,\"14\":true,\"15\":true,\"16\":true,\"17\":true,\"18\":true,\"21\":true,\"22\":true,\"23\":true,\"24\":true,\"25\":true,\"26\":true,\"27\":true,\"28\":true,\"31\":true,\"32\":true,\"33\":true,\"34\":true,\"35\":true,\"36\":true,\"37\":true,\"38\":true,\"41\":true,\"42\":true,\"43\":true,\"44\":true,\"45\":true,\"46\":true,\"47\":true,\"48\":true,\"51\":true,\"52\":true,\"53\":true,\"54\":true,\"55\":true,\"61\":true,\"62\":true,\"63\":true,\"64\":true,\"65\":true,\"71\":true,\"72\":true,\"73\":true,\"74\":true,\"75\":true,\"81\":true,\"82\":true,\"83\":true,\"84\":true,\"85\":true},\"activatedToothNumber\":48,\"activatedPartialList\":[]}"}],
                 "medicalRecordDisposeVOList": [{"key": "cfcad3c4-fe29-5a1e-bf5f-c1c01aad6a3d", "dispose": "先吃点药",
                                                 "disposePosition": "{\"teeth\":{\"11\":true,\"12\":true,\"13\":true,\"14\":true,\"15\":true,\"16\":true,\"17\":true,\"18\":true,\"21\":true,\"22\":true,\"23\":true,\"24\":true,\"25\":true,\"26\":true,\"27\":true,\"28\":true,\"31\":true,\"32\":true,\"33\":true,\"34\":true,\"35\":true,\"36\":true,\"37\":true,\"38\":true,\"41\":true,\"42\":true,\"43\":true,\"44\":true,\"45\":true,\"46\":true,\"47\":true,\"48\":true,\"51\":true,\"52\":true,\"53\":true,\"54\":true,\"55\":true,\"61\":true,\"62\":true,\"63\":true,\"64\":true,\"65\":true,\"71\":true,\"72\":true,\"73\":true,\"74\":true,\"75\":true,\"81\":true,\"82\":true,\"83\":true,\"84\":true,\"85\":true},\"activatedToothNumber\":48,\"activatedPartialList\":[]}"}],
                 "doctorAdvice": "一定要早晚记得刷牙" + tag_str, "createRegister": False,
                 "medicalRecordRegisterVO": {"visType": 1, "registerTime": 1617947464000, "createRegister": False,
                                             "doctorStaffId": 3563}, "medicalInstitutionId": 665, "patientId": 33256,
                 "medicalRecordId": 25971}),
            'registerPatientToothSymptomLoadMedicalRecordJson': {},
            'registerPatientToothSymptomDisposeDTOListJson': {}
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
            path=f'{self.path_update_electronic_medical_records}',
            headers=None, data=payload_data , catch_response=True,name="更新电子病例") as res:
            if res.status_code == 200:

                    if (json.loads(res.text))["code"] == 0:
                        res.success()
                    else:
                        #raise RescheduleTask()
                        res.failure(res.text)
                        print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_update_electronic_medical_records)

            else:
                res.failure(res.text)
                print(time.strftime('%Y年%m月%d日%H时%M分%S秒'), "失败------", self.path_update_electronic_medical_records)



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
    os.system("locust -f locust_update_electronic_medical_records.py --host=http://localhost")
    #os.system("locust -f locust_h5.py --host=http://localhost -T physical_demo")

    #os.system("locust -f locust_zadan.py --host=192.168.90.164")