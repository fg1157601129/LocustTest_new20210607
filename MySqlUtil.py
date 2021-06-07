# -*- coding: utf-8 -*-

# @File    : MySqlUtil.py
# @Date    : 2019-09-23-10:42
# @Author  : DanKeGeGe
# @Version : 1

#import pymysql
import pymssql

class MySqlUtil():
    """
    数据库相关操作类
    查询某个字段对应的字符串：mysql_get_string
    查询一组数据：mysql_get_rows
    创建游标：mysql_execute
    关闭 mysql 连接：mysql_close，每次使用完成调用mysql_close关闭连接
    """

    def __init__(self):
        # self.connection = pymysql.connect(host='47.103.7.92', port=3306, user='test', password='bobei123',
        #                                   database='kela_user')
        self.connection = pymssql.connect(host='192.168.1.104', port=1433, user='fg', password='t#vb@Pc.%u25.Cu',
                                          database='zhaoyu_dev')



    def mysql_execute(self, sql):
        """执行 sql 语句写入"""
        cur = self.connection.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            self.connection.rollback()  # sql 执行异常后回滚
            print("执行 SQL 语句出现异常：%s" % a)
        else:
            cur.close()
            self.connection.commit()  # sql 无异常时提交

    def mysql_get_rows(self, sql):
        """返回查询结果"""
        cur = self.connection.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            print("执行 SQL 语句出现异常：%s" % a)
        else:
            rows = cur.fetchall()
            cur.close()
            return rows

    def mysql_get_string(self, sql):
        """查询某个字段的对应值"""
        rows = self.mysql_get_rows(sql)
        if rows is not None:
            for row in rows:
                for i in row:
                    return i


    def mysql_get_result_list(self,sql):
        result = []
        rows = self.mysql_get_rows(sql)
        if rows is not None:
            for row in rows:
                result.append(row[0])
        return result

    def mysql_close(self):
        """关闭 close mysql"""
        try:
            self.connection.close()
        except Exception as a:
            print("数据库关闭时异常：%s" % a)

# if __name__ == "__main__":
    # s_sql = 'SELECT * FROM kela_user.member_info LEFT JOIN kela_user.union_mobile ON ' \
    #         'member_info.member_id=union_mobile.member_id WHERE union_mobile.mobile=18616296323;'
    # s_sql = "SELECT *FROM kela_user.member_info WHERE sex = 2"
    # s = MySqlUtil().mysql_get_rows(s_sql)
    # result = MySqlUtil().mysql_get_result_list(s_sql)
    #
    # print(result)
    # MySqlUtil().mysql_close()
