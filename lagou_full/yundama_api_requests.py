#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: yundama_api_requests.py
@time: 2019/3/22 10:34
@desc:
'''

import json
import requests


class YDMHttp(object):
    # 调用api
    apiurl = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    appid = ''
    appkey = ''

    # 初始化时传递用户名, 密码, appid, appkey四个参数
    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    # balance, login和decode三个函数都调用的是apiurl这个接口, 只是传递的data不同.
    def balance(self):
        # 获取剩余积分
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response_data = requests.post(self.apiurl, data=data)
        ret_data = json.loads(response_data.text)
        # 获取积分成功
        if ret_data["ret"] == 0:
            print("获取剩余积分", ret_data["balance"])
            return ret_data["balance"]
        # 获取积分失败
        else:
            return None

    def login(self):
        # 登录
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response_data = requests.post(self.apiurl, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:
            print("登录成功", ret_data["uid"])
            return ret_data["uid"]
        else:
            return None

    # 验证码解码
    def decode(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        files = {'file': open(filename, 'rb')}
        response_data = requests.post(self.apiurl, files=files, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:  # 在此处添加断点调试.
            print("识别成功", ret_data["text"])
            return ret_data["text"]
        else:
            return None


# 这里可以直接传递一个文件, 也可以直接把验证码的响应内容传递进来

def indetify_by_response(response_content):
    # 用户名, 普通用户的用户名
    username = 'davidmount'
    # 密码, 普通用户的密码
    password = 's6u9p5e3r8'
    # 软件ID, 开发者分成必要参数. 登录开发者后台【我的软件】>软件代码获得！开发者注册之后开发软件, 提供给普通用户使用, 普通用户收费使用开发者提供的软件.
    appid = 5809
    # 软件密钥, 开发者分成必要参数. 登录开发者后台【我的软件】> 通讯密钥获得！
    appkey = 'd8af523c6fefbf9c70245bf94a39ed38'
    # 测试代码, 验证码图片文件
    filename = 'getimage.jpg'
    # 验证码类型, # 例: 1004表示4位字母数字, 不同类型收费不同. 请准确填写, 否则影响识别率. 在此查询所有类型 http://www.yundama.com/price.html, 如果不知道, 可以设置为5000
    codetype = 1004
    # 超时时间, 秒
    timeout = 60

    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化, 传递username, password, appid, appkey, appid和appkey在登录之后就可以得到.
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)

        # 开始识别, 图片路径, 验证码类型ID, 超时时间（秒）, 识别结果
        cid, result = yundama.decode(response_content, codetype, timeout)
        print('cid: %s, result: %s' % (cid, result))
        return result


def indetify_by_filepath(filename):
    # 用户名, 普通用户的用户名
    username = 'da_ge_da1'
    # 密码, 普通用户的密码
    password = 'da_ge_da'
    # 软件ID, 开发者分成必要参数. 登录开发者后台【我的软件】>软件代码获得！开发者注册之后开发软件, 提供给普通用户使用, 普通用户收费使用开发者提供的软件.
    appid = 3129
    # 软件密钥, 开发者分成必要参数. 登录开发者后台【我的软件】> 通讯密钥获得！
    appkey = '40d5ad41c047179fc797631e3b9c3025'
    # 测试代码, 验证码图片文件
    filename = 'getimage.jpg'
    # 验证码类型, # 例: 1004表示4位字母数字, 不同类型收费不同. 请准确填写, 否则影响识别率. 在此查询所有类型 http://www.yundama.com/price.html, 如果不知道, 可以设置为5000
    codetype = 1004
    # 超时时间, 秒
    timeout = 60

    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化, 传递username, password, appid, appkey, appid和appkey在登录之后就可以得到.
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login();
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance();
        print('balance: %s' % balance)

        # 开始识别, 图片路径, 验证码类型ID, 超时时间（秒）, 识别结果
        cid, result = yundama.decode(filename, codetype, timeout)
        print('cid: %s, result: %s' % (cid, result))
        return result


if __name__ == '__main__':
    # 生成验证码的网址
    url = "http://qian.sicent.com/Login/code.do"
    response_content = requests.get(url).content
    # 把验证码写入到本地文件中
    with open("test.png", "wb") as f:
        f.write(response_content)

    # 调用在线打码平台进行验证码的识别
    indetify_by_response(response_content)
    indetify_by_filepath("test.png")