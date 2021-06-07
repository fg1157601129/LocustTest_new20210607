#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/7 13:29
# @Author : Aries
# @Site :
# @File : locust_collection_point.py
# @Software: PyCharm
from json import JSONDecodeError
import json
from locust import HttpUser,task,TaskSet,SequentialTaskSet,between,tag,events
from locust.contrib.fasthttp import FastHttpUser,ResponseContextManager,FastResponse
import os
import random
import time
from locust.exception import RescheduleTask
from faker import Faker
import queue
import requests

from gevent._semaphore import Semaphore
# 实例化
all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()
# 创建等待方法
def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()
# 当用户加载完成是触发
events.hatch_complete += on_hatch_complete

# 定义用户压测前的一些行为

def func_select_visit_data():
    queue_data = queue.Queue()  # 实例化一个队列
    host = "https://power.medcloud.cn"
    path = "/api/his/patient/return/visit/customer/page"
    url_select_visit_data = f"{host}{path}"
    result_data = {
        "_token": "70ce2d26efb745fe843a6f125ba08fd0",
        "_uid": 2279,
        "_ut": 1,
        "_t": 1,
        "_s": 11,
        "_mtId": 553,
        "_tenantId": 376,
        "_cmtId": 546,
        "_cmtType": 2,
        "_lang": "zh_CN",
        "customerInfo": "新能",
        "visitStatus": 3,
        "planVisitStartTime": "2020-04-01+00:00:00",
        "planVisitEndTime": "2021-04-14+23:59:59",
        "sortName": "",
        "sort":False,
        "current": 1,
        "size": 10
    }
    #url_select_visit_data = f"{host}{path}?_token=70ce2d26efb745fe843a6f125ba08fd0&_uid=2279&_ut=1&_t=1&_s=11&_mtId=553&_tenantId=376&_cmtId=546&_cmtType=2&_lang=zh_CN&customerInfo=新能&visitStatus=3&planVisitStartTime=2020-04-01+00:00:00&planVisitEndTime=2021-04-14+23:59:59&sortName=&sort=false&current=1&size=10"
    res = requests.get(url=url_select_visit_data,data=result_data)
    print(res)

func_select_visit_data()