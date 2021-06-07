#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/3/12 11:58
# @Author : Aries
# @Site :
# @File : locust_demo1.py
# @Software: locust_sql.py

import pymssql
import time
import random
import os
import queue
import threading


def conn(sql_str):
    #db = pymssql.connect(host="192.168.1.104",port=1433,user="fg",password="t#vb@Pc.%u25 .Cu",database="zhaoyu_dev",charset="utf-8")
    db = pymssql.connect(host="192.168.1.104", port=1433, user="fg", password="t#vb@Pc.%u25 .Cu")
    cursor = db.cursor()
    if not cursor:
        print("连接失败")
    else:
        cursor.execute(sql_str)
        data = cursor.fetchall()
        print(data)


def insert_sql():
    for i in range(100):
        intId = 70000 + i
        userId = "522d2f8d-61e5-4214-9d62-2c945e7da99" + str(i)
        Account = 14650000000 + i
        password = "12b69fecff33bd72a1a185abf9eec269"
        Secretkey = "0c6bfb6e3d31c140"
        UniqueCode = "44a78602-75dd-446a-be41-ed072ebcd75" + str(i)
        UserType = 0
        Mobile = 14650000000 + i
        NickName = "insert" + str(i)
        Gender = 1
        PhotoGraph = 'http://imgcdn.zhaoyugf.com/2928a188fb4d41229a6378afe216df35'
        Enabled = 0
        Online = 1
        IsEmployee = 0
        IsMerchant = 0
        IsPerfect = 0
        IsVideo = 1
        IsSpeak = 0
        CreateDate = '2020-03-25 10:00:18.000'
        LastTime = '2020-03-25 14:17:07.970'
        LastIp = '210.22.78.174'
        Remark = None
        SorCode = 0
        insert_sql_str = "INSERT INTO [zhaoyu_dev].[dbo].[Base_UserMasterV1] ([IntId],[UserId], [Account],[Password],[Secretkey],[UniqueCode],[UserType],[Mobile],[NickName],[Gender],[PhotoGraph],[Enabled],[Online],[IsEmployee], [IsMerchant],[IsPerfect], [IsVideo],[IsSpeak], [CreateDate],[LastTime],[LastIp],[Remark], [SortCode]) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'".format(intId,userId,Account,password,Secretkey,UniqueCode,UserType,Mobile,NickName,Gender,PhotoGraph,Enabled,Online,IsEmployee,IsMerchant,IsPerfect,IsVideo,IsSpeak,CreateDate,LastTime,LastIp,Remark,SorCode) + ")"

        print(insert_sql_str)
        conn(insert_sql_str)


def select_sql():
    for i in range(100):
        mobeil_str = str(13100000000 + i)
        select_sql_str = "select "
        conn(select_sql_str)

#threads = []

#t1 = threading.Thread(target=insert_sql())

sql_str = "INSERT INTO [zhaoyu_dev].[dbo].[Base_UserMasterV1] ([IntId],[UserId], [Account],[Password],[Secretkey],[UniqueCode],[UserType],[Mobile],[NickName],[Gender],[PhotoGraph],[Enabled],[Online],[IsEmployee], [IsMerchant],[IsPerfect], [IsVideo],[IsSpeak], [CreateDate],[LastTime],[LastIp],[Remark], [SortCode]) VALUES ('70099','522d2f8d-61e5-4214-9d62-2c945e7da9999','14650000099','12b69fecff33bd72a1a185abf9eec269','0c6bfb6e3d31c140','44a78602-75dd-446a-be41-ed072ebcd7599','0','14650000099','insert99','1','http://imgcdn.zhaoyugf.com/2928a188fb4d41229a6378afe216df35','0','1','0','0','0','1','0','2020-03-25 10:00:18.000','2020-03-25 14:17:07.970','210.22.78.174','None','0')"
conn(sql_str)
#insert_sql()