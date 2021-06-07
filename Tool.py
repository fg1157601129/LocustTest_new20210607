# -*- coding: utf-8 -*-

import hashlib
import math
# @File    : Tool.py
# @Date    : 2019-03-25-18:01
# @Author  : DanKeGeGe
# @Version  : 1
import random
import time
from readconfig import Read
import pymysql

random_num = str(random.randint(100000, 999999))


class Tool:
    """工具类"""

    def __init__(self):
        self.imei = Read().get_header_config('imei')
        self.os = Read().get_header_config('os')  # 1=IOS,2=android,3=企业版，脚本用户 2
        self.request_key = Read().get_header_config('requestIdKey')
        self.mobile = Read().get_header_config('mobile')  # 手机号，目前仅支持中国区
        self.password = Read().get_header_config("password")  # 密码，8-16位
        self.member_id = Read().get_header_config('member_id')  # 用户ID
        self.versionCode = Read().get_header_config('versionCode')  # APP版本号：11
        self.accessToken = Read().get_header_config('accessToken')  # 登录状态的token
        self.deviceModel = Read().get_header_config('deviceModel')  # 设备类型
        self.osVersion = Read().get_header_config('osVersion')  # 设备系统版本号
        self.softVersion = Read().get_header_config('softVersion')  # 克拉版本号
        self.loginType = Read().get_header_config('loginType')  # 1=扫脸登录，2=手机号一键登录，3=Token登录，4=手机号+密码登录
        self.areaCode = Read().get_header_config('areaCode')
        self.women_user = Read().get_header_config("women_user")
        self.num_len = len(Read().get_header_config("women_user"))
        # self.sign = None  # 目前没有用上，可以不传

    def headers_login(self):
        timestamp = self.get_timestamp()
        h = {
            'os': self.os,
            'imei': self.imei,
            'timestamp': timestamp,
            'versionCode': self.versionCode,
            'random': random_num,
            'requestId': self.get_request_id(timestamp)
        }
        return h

    def headers(self):
        timestamp = self.get_timestamp()
        h = {
            'os': self.os,
            'imei': self.imei,
            'timestamp': timestamp,
            'versionCode': self.versionCode,
            'random': random_num,
            'requestId': self.get_request_id(timestamp),
            'accessToken': self.accessToken
        }
        return h

    def get_request_id(self, timestamp):
        before_str = self.os + self.imei + timestamp + random_num + self.request_key
        return self.md5(before_str)



    @staticmethod
    def md5(md5str=None):
        """
        :param md5str:需要加密的字符串
        :return: md5后的字符串（大写）
        """
        hl = hashlib.md5()  # 创建md5对象
        hl.update(md5str.encode(encoding='utf-8'))  # 生成加密字符串
        return hl.hexdigest()

    @staticmethod
    def get_timestamp():
        return str(int(round(time.time() * 1000)))

    @property
    def get_random_gps(self):
        """以公司所在经纬度为圆心，100公里为半径，随机产生一个经纬度"""
        radius_in_degrees = 100000 / 111300  # 半径100公里
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))
        w = radius_in_degrees * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
        longitude = y + 121.516203  # 公司附近经度
        latitude = x + 31.069320  # 公司附近维度
        # 这里是想保留6位小数点
        log = '%.6f' % longitude
        lat = '%.6f' % latitude
        return log, lat


def add_friends():
    friend_list = list(eval(Read().get_header_config("women_user"))) #一行解决读取配置文件字符串类型转换列表类型
    return friend_list


    # user_list = [208, 213, 214, 216, 224, 228, 229, 232, 233, 236, 241, 246, 250, 252, 263, 264, 265, 266, 267, 268, 271, 277, 281, 282, 285, 286, 287, 292, 329, 330, 345, 358, 361]
    # add_user = random.choice(user_list)
    #add_user = ''
    # for i in user_list:
    #     add_user = i
    # women_user_list = random.choice(Tool().women_user)
    # #for i in range(len(Tool().women_user)):
    #
    # return women_user_list


if __name__ == '__main__':
    #print(Tool().women_user,type(Tool().women_user),len(Tool().women_user),"---------------------")
    add_friends()

