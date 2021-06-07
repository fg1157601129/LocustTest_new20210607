# -*- coding: utf-8 -*-

# @File    : readconfig.py
# @Date    : 2019-03-25-18:01
# @Author  : DanKeGeGe
import codecs
import configparser


class Read():
    """读取配置文件config.txt"""

    def __init__(self):
        fd = open("config.txt")
        data = fd.read()
        #  remove BOM（byte-order mark）文件编码头，即 字节顺序标记。一些特殊的编码下生成的文件会含有特殊字符而且文件打
        #  开不可见，但在对程序造成很大困扰
        if data[:3] == codecs.BOM_UTF8:  # 判断是否为带BOM文件
            data = data[3:]
            file = codecs.open("config.txt", "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read("config.txt")

    def get_header_config(self, name=None):
        value = self.cf.get("Header", name)
        return value
