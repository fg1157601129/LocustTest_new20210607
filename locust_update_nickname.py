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
import random


class UpdateNickname(TaskSet):  # TaskSet类
    @task(1)
    def send_red_packet(self):
        json_data = {
            "areaName": "",
            "birthday": "",
            "cityName": "",
            "constellation": "",
            "coverPhoto": "",
            "customtagName": "",
            "expecttagName": "",
            "friendlytagName": "",
            "headPhoto": "",
            "height": 0,
            "industryName": "",
            "memberId": 7,
            "nickname": "一只西瓜皮",
            "photos": [
                {
                    "fileName": "",
                    "id": 0,
                    "picUrl": "",
                    "sort": 0,
                    "type": 0
                }
            ],
            "provinceName": "",
            "socialStatus": "",
            "status": 0,
            "weight": 0
        }
        response = HttpSession(base_url=UrlEnum.KELA_USER_WEB.value).request(method='post',
                                                                             url='/memberinfo/nickname',
                                                                             json=json_data,
                                                                             headers=Tool().headers(),
                                                                             catch_response=False)
        print("Response content:", response.text)
        print(json_data)
        assert 200 == response.status_code



class SendRedPacketLocust(HttpLocust):
    task_set = UpdateNickname
    min_wait = 1000
    max_wait = 1000