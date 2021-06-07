# -*- coding: utf-8 -*-

# @File    : HttpRequests.py
# @Date    : 2019-05-14-18:10
# @Author  : FangGang
# @Version : 1
import requests
from HTMLReport import logger



class HttpRequests:
    """封装get和post请求"""

    def send_r(self, method, u, d, j, h):
        """
        接口访问方式和数据
        :param method: post/get
        :param u: url
        :param d: data数据
        :param j: json数据
        :param h: headers中的多个公用参数
        :return result:未经处理的接口返回数据
        """
        result = None
        if method == 'post':
            result = self.send_p(u, d, j, h)
            logger().info('\n【接口返回数据】:------\n%s' % result.text)
        elif method == 'get':
            result = self.send_g(u, d, h)
            logger().info('\n【接口返回数据】:------\n%s' % result.text)
        else:
            logger().error('错误!!!')
        return result

    def send_post_upload(self, u, d, j, f, h):
        """
        上传文件附件
        :param u: url
        :param d: data数据
        :param j: json数据
        :param f: file文件
        :param h: headers中的多个公用参数
        :return result:未经处理的接口返回数据
        """
        res = requests.post(url=u, data=d, json=j, files=f, headers=h)
        logger().info('post: %s,\n 从请求到接口返回信息耗时:%s秒' % (u, res.elapsed.total_seconds()))
        logger().info(res.text)
        return res

    def send_delete(self, u, d, j, h):
        res = requests.delete(url=u, data=d, json=j, headers=h)
        logger().info('delete: %s,\n 从请求到接口返回信息耗时:%s秒' % (u, res.elapsed.total_seconds()))
        logger().info(res.text)
        return res

    @staticmethod
    def send_p(u, d, j, h):
        """
        post请求
        :param u: url
        :param d: data数据
        :param j: json数据
        :param h: headers中的多个公用参数
        :return res: 未经处理的接口返回数据
        """
        if d is None:
            res = requests.post(url=u, json=j, headers=h)
            logger().info('post: %s,\n json数据:%s,\n 从请求到接口返回信息耗时:%s秒' % (u, j, res.elapsed.total_seconds()))
        else:
            res = requests.post(url=u, data=d, json=j, headers=h)
            logger().info(
                'post: %s,\n data数据:%s,\n json数据:%s,\n 从请求到接口返回信息耗时:%s秒' % (u, d, j, res.elapsed.total_seconds()))
        return res

    @staticmethod
    def send_g(u, d, h):
        """
        get请求
        :param u: url
        :param d: body中的data
        :param h: headers中的多个公用参数
        :return res: 未经处理的接口返回数据
        """
        if d is None:
            res = requests.get(u, headers=h)
            logger().info('get: %s,\n 从请求到接口返回信息耗时:%s秒' % (u, res.elapsed.total_seconds()))
        else:
            res = requests.get(u, data=d, headers=h)
            logger().info('get: %s,\n data数据:%s,\n 从请求到接口返回信息耗时:%s秒' % (u, d, res.elapsed.total_seconds()))
        return res
