#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import requests
from xiaoli.config import setting
from xiaoli.utils.logs.logger import common_logger

__author__ = 'roc'


class SmsSender(object):
    u"""
    success:msgid
    提交成功,发送状态请见 4.1

    error:msgid
    提交失败

    error:Missing username
    用户名为空

    error:Missing password
    密码为空

    error:Missing apikey
    APIKEY 为空

    error:Missing recipient
    手机号码为空

    error:Missing message content
    短信内容为空

    error:Account is blocked
    帐号被禁用

    error:Unrecognized encoding
    编码未能识别

    error:APIKEY or password error
    APIKEY 或密码错误

    error:Unauthorized IP address
    未授权 IP 地址

    error:Account balance is insufficient
    余额不
    """

    URL = "http://m.5c.com.cn/api/send/index.php"
    SMS_MESSAGE = u"您的手机%s正在注册,您的验证码是:%s"

    def __init__(self, phone, content=None):
        self.phone = phone
        self.status = None
        self.message = None
        self.code = SmsSender.rand_code()
        self._content = None

    @property
    def content(self):
        return SmsSender.SMS_MESSAGE % (self.phone, self.code)

    @property
    def is_success(self):
        return self.status == 'success'

    def send(self, content=None):
        username = setting.SMS["username"]
        password = setting.SMS["password"]
        api_key = setting.SMS["apikey"]
        params = {
            'username': username,
            'password': password,
            'apikey': api_key,
            'mobile': self.phone,
            'content': content or self.content
        }
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        result = requests.post(SmsSender.URL, params=params, timeout=30, headers=headers)
        common_logger.debug(result.text)
        status, message = result.text.split(":")
        self.status = status
        self.message = message

    @staticmethod
    def rand_code():
        return random.randrange(100000, 999999)
