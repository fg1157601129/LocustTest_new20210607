import json
import re
import time
import ast
from urllib.parse import urlparse
from pprint import pprint
s = "billStatus=1&size=10&current=1&createTimeStart=1620230400000&createTimeEnd=1620316799999&_uid=2681&_token=ab3ad3d0c5064ef78eef14eee0d13a13&_ut=1&_t=1&_s=5&_lang=zh_CN&_mtId=665&_cmtType=2&_tenantId=452&_cmtId=625"
# # 链式replace()
# r = s.replace('&',',').replace('=',':')
# print(r)
# d = r.split(',')
# print("d",d)
# result = {}
# # print(type(r),r)
# for i in r:
#     result[i[0]] = i[1]
# print(result)
#d = eval("{" + json.dumps(s.replace('&',',').replace('=',':')) + "}")
# d = ast.literal_eval(r)
# print(d)
#print(type(json.loads(r)),json.loads(r))
s1 = "key1=value1&key2=value2&key3=str"


def conversion(str):
    b_time = time.time()
    for i in range(1000000):
        pattern = r'&'
        reg = re.compile(pattern).split(str)
        pattern2 = r'='
        result = {}
        for i in reg:
            kv = re.compile(pattern2).split(i)
            result[kv[0]] = kv[1]
        #print(type(result),result)

    f_time = time.time()
    print("耗时：", f_time - b_time)

def conversion_1(_str):
    b_time = time.time()

    for i in range(1000000):
        result = json.loads('{"' + _str.replace('=', '": "').replace('&', '", "') + '"}')
        #result = '{"' + _str.replace('=', '": "').replace('&', '", "') + '"}'
        #pprint(result)

    f_time = time.time()
    print("耗时：", f_time - b_time)
    #r = eval(result)
conversion_1(s)
conversion(s)



# result = urlparse(s)
# print(result)

