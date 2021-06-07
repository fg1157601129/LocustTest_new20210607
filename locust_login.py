# -*- coding: utf-8 -*-

import json

# @File    : locustfile-1.py
# @Date    : 2019-09-24-16:58
# @Author  : DanKeGeGe
# @Version : 1
from configobj import ConfigObj
from locust import HttpLocust, task, TaskSet
from locust.clients import HttpSession

from KelaEnum import UrlEnum
from Tool import Tool


class UserBehavior(TaskSet):  # TaskSet类

    def login_with_mobile_and_psw(self):
        """手机号密码登录，并重写配置文件"""
        log, lat = Tool().get_random_gps
        json_data = {
            'deviceInfo': {
                'deviceModel': Tool().deviceModel,
                'imei': Tool().imei,
                'latitude': log,
                'longitude': lat,
                'loginType': Tool().loginType,
                'os': Tool().os,
                'osVersion': Tool().osVersion,
                'softVersion': Tool().softVersion
            },
            'pwdLoginExtVo': {
                'areaCode': Tool().areaCode,
                'mobile': Tool().mobile,
                'password': Tool().password
            }
        }
        response = HttpSession(base_url=UrlEnum.KELA_USER_WEB.value).request(method='post',
                                                                             url='/member/mobilePwdLogin',
                                                                             json=json_data,
                                                                             headers=Tool().headers_login(),
                                                                             catch_response=True)
        print("Response content:", response.text)
        assert 200 == response.status_code
        r = response.json()
        # access_token = r['data']['kelaToken']
        # member_id = r['data']['memberId']
        # config = ConfigObj('config.txt', encoding='utf-8')
        # config['Header']['accessToken'] = access_token
        # config['Header']['member_id'] = member_id
        # config.write()

    def scan_face_login(self):
        """
        扫脸登录，传一张照片
        :return: member_id, access_token, rc_token
        """
        u = UrlEnum.KELA_USER_WEB.value + '/member/v1/scanFaceLogin'
        file = {"file": open('face.jpg', "rb")}
        response = HttpSession(base_url=UrlEnum.KELA_USER_WEB.value).request(method='post',
                                                                             url='/member/v1/scanFaceLogin',
                                                                             files=file,
                                                                             headers=Tool().headers(),
                                                                             catch_response=False)
        print("Response content:", response.text)
        assert 200 == response.status_code
        # # r = HttpRequests().send_post_upload(u=url, d=None, j=None, f=file, h=Tool().headers()).json()
        # if 200 == r['code']:
        #     print('扫脸登录成功')
        # else:
        #     print('扫脸登录失败')

    @task(1)  # 等同于LoadRunner事务
    def my_task_1(self):
        self.login_with_mobile_and_psw()

    @task(1)
    def my_task_2(self):
        self.scan_face_login()


class MobileUserLocust(HttpLocust):
    task_set = UserBehavior
    host = 'http://127.0.0.1:8089'
    min_wait = 2000
    max_wait = 5000
