#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/3/12 11:58
# @Author : Aries
# @Site :
# @File : locust_demo1.py
# @Software: locust_sql.py
from locust import HttpLocust,TaskSet,task
#from locust.clients import HttpSession
import pymssql
import time
import random
import os


def open_start(sql_str):
    db = pymssql.connect(host="192.168.1.104", port=1433, user="fg", password="t#vb@Pc.%u25 .Cu",
                         databese="zhaoyu_dev")
    cursor = db.cursor()
    cursor.execute(sql_str)
    data = cursor.fetchall()

    print("--------------------   Test start   --------------------")
    print(data)


class ZhaoyuSql(TaskSet):

    # def on_stop(self):
    #     print("--------------------   Test over   --------------------")

    @task(1)
    def select_sql(self):


        select_sql = "SELECT *FROM zhaoyu_dev.dbo.Base_UserVipCardV1 WHERE CardType = 1"
        open_start(select_sql)
        # cursor.execute("INSERT INTO [zhaoyu_dev].[dbo].[Base_UserVipCardV1] ([Id], [UserId], [CardType], [ExpireTimexpireTime], [IsTrial], [CreateTime], [UpdateTime], [IntId]) VALUES ('7FEE1ED9-3BE2-41B1-B64C-A75DC6D6BA81', '2626b434-0368-4433-8e59-c4fd68be354b', '1', '2021-03-12 11:08:32.273', '0', '2020-03-12 11:08:32.273', '2020-03-12 11:08:32.273', '2');")
        # cursor.execute(select_sql)
        # self.data = cursor.fetchall()
        # db.close()
        #self.bindstudents()

        # ZhaoyuSql().on_start(select_sql)
    @task(1)
    def insert_sql(self):
        insert_sql = "SELECT *FROM zhaoyu_dev.dbo.Base_UserVipCardV1 WHERE CardType = 2"
        open_start(insert_sql)
        return insert_sql
    # def insert_sql(self):
    #     db = pymssql.connect(host="192.168.1.104", port=1433, user="fg", password="t#vb@Pc.%u25.Cu",
    #                          databese="zhaoyu_dev")
    #     cursor = db.cursor()
    #     insert_sql = "SELECT *FROM zhaoyu_dev.dbo.Base_UserVipCardV1 WHERE CardType = 2"
    #     # cursor.execute("INSERT INTO [zhaoyu_dev].[dbo].[Base_UserVipCardV1] ([Id], [UserId], [CardType], [ExpireTime], [IsTrial], [CreateTime], [UpdateTime], [IntId]) VALUES ('7FEE1ED9-3BE2-41B1-B64C-A75DC6D6BA81', '2626b434-0368-4433-8e59-c4fd68be354b', '1', '2021-03-12 11:08:32.273', '0', '2020-03-12 11:08:32.273', '2020-03-12 11:08:32.273', '2');")
    #     cursor.execute(insert_sql)
    #     self.data = cursor.fetchall()
    #     db.close()

        #ZhaoyuSql().on_start(insert_sql)

class WebsiteUser(HttpLocust):
    #host = ""
    task_set = ZhaoyuSql
    min_wait = 0
    max_wait = 0


if __name__ == "__main__":
    # os模块执行系统命令，相当于在cmd切换到当前脚本目录，执行locust -f locust_login.py
    #os.system("locust -f locust_sql.py --host=192.168.1.90")
    #open_start("select")
    ZhaoyuSql().select_sql
