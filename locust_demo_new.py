# -*- coding: utf-8 -*-
import os,requests
from locust import TaskSet, task, HttpUser, between


# 任务类
class Testlocust(TaskSet):
    def on_start(self):
        print("------on start------")
        # access_token = self.userlogin()  # 返回登录token
        # self.headers = {}  # 定义headers
        # self.headers['x-api-key'] = 'fZkQSHC1dp2s0tL21EMtaNX3UjF7P6L9'  # 添加headers值
        # self.headers['Authorization'] = 'Bearer ' + access_token
        # self.headers['x-key-hash'] = '1607675936446;abcdefg;bca1ef2b5835e454a15929f7ce9cb5d7ebaf580377624019002'
        # self.headers['Content-Type'] = 'application/json'
        # self.params = {"name": "CDR", "page": "1", "size": "10", "series": "CDR80"}  # 查询接口参数

    def userlogin(self):  # 登录方法
        add_items_type = 'https://xxxxxx/v1/auth/users/login'  # 登录url
        data = {
            "account_name": "账号1",
            "user_name": "账号1",
            "hashed_password": "密码1"
        }  # 登录账号密码
        login_headers = {'x-client-id': '46bf882df2959ea2'}
        r = requests.request('POST', url=login_url, headers=login_headers, json=data)  # 登录
        return r.json()['access_token']  # 返回登录token

    @task()
    def search(self):  # 查询设备信息
        r = self.client.get(url='/v1/assets/device/search', headers=self.headers, params=self.params, name='查询',
                            verify=False)  # 查询
        assert r.status_code == 200 and r.json()['code'] == 0  # 结果断言


# 用户类
class WebsiteUser(HttpUser):  # locust1.0版本以前是HttpLocust
    tasks = [Testlocust]  # locust1.0版本以前是task_set=Testlocust
    host = 'https://xxxxxx.com'  # 被测主机地址
    wait_time = between(min_wait=1, max_wait=5)  # 任务之间的等待时间


if __name__ == "__main__":
    os.system("locust -f locust_XX.py")  # 执行参数
