# -*- coding: utf-8 -*-

# @File    : Login.py
# @Date    : 2019-09-24-16:51
# @Author  : DanKeGeGe
# @Version : 1
import time
import random
from configobj import ConfigObj
from HttpRequests import HttpRequests
from KelaEnum import UrlEnum
from Tool import Tool
from MySqlUtil import MySqlUtil

config = ConfigObj('config.txt', encoding='utf-8')
def login_with_mobile_and_psw():
    """手机号密码登录，并重写配置文件"""
    url = UrlEnum.KELA_USER_WEB.value + '/member/mobilePwdLogin'
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
            'password': Tool().md5(Tool().password)
        }
    }
    r = HttpRequests().send_r(method='post', u=url, d=None, j=json_data, h=Tool().headers_login()).json()
    if 200 == r['code']:  # 成功才重写配置文件
        access_token = r['data']['kelaToken']
        rc_token = r['data']['rcToken']
        member_id = r['data']['memberId']
        #config = ConfigObj('config.txt', encoding='utf-8')
        config['Header']['accessToken'] = access_token
        config['Header']['rcToken'] = rc_token
        config['Header']['member_id'] = member_id
        config.write()
        time.sleep(1.0)
        scan_face()  # 登录成功后再调用扫脸接口
        time.sleep(1.0)
        return member_id, access_token, rc_token
    elif 203 == r['code']:
        print('')
        return False
    else:
        return False


def scan_face():
    """
    扫脸登录，传一张照片
    :return: member_id, access_token, rc_token
    """
    url = UrlEnum.KELA_USER_WEB.value + '/member/v1/scanFaceLogin'
    file = {"file": open('face.jpg', "rb")}
    r = HttpRequests().send_p(u=url, d=file, j=None, h=Tool().headers()).json()
    if 200 == r['code']:  # 成功才重写配置文件
        access_token = r['data']['kelaToken']
        rc_token = r['data']['rcToken']
        member_id = r['data']['memberId']
        config = ConfigObj('config.txt', encoding='utf-8')
        config['Header']['accessToken'] = access_token
        config['Header']['rcToken'] = rc_token
        config['Header']['member_id'] = member_id
        config.write()
        return member_id, access_token, rc_token


def get_women_user():
    str_sql = "SELECT *FROM kela_user.member_info WHERE sex = 2"
    #result_list = random.choice(MySqlUtil().mysql_get_result_list(str_sql))
    #config = ConfigObj(ProjectPath().config_path, encoding='utf-8')
    result_list = MySqlUtil().mysql_get_result_list(str_sql)
    config = ConfigObj('config.txt', encoding='utf-8')
    config['Header']['women_user'] = result_list
    config.write()
    MySqlUtil().mysql_close()
    print("获取成功，并成功写入----------config")
    print(type(result_list),result_list)


# def get_women_user():
#     url = UrlEnum.KELA_CLUB_WEB.value + '/app/getActives'
#     json_data = {
#             "latitude": 0,
#             "longitude": 0,
#             "pageNum": 1,
#             "sex": 2
#                 }
#     r = HttpRequests().send_r(u = url,d = None,j = json_data,h = Tool().headers()).json()





get_women_user()
login_with_mobile_and_psw()
