#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zouyingjun'


class ErrorCode(object):

    # 服务器临时不可用
    CODE_SERVER_TEMPORARILY_UNUSABLE = 3000

    # 注册时手机号已经存在
    CODE_REGISTER_PHONE_EXISTS = 1500
    # 注册时两次密码不一致
    CODE_REGISTER_PASSWORD_NOT_EQUAL = 1501

    # 登陆是手机号不存在
    CODE_LOGIN_PHONE_NOT_EXISTS = 1601
    # 登陆时密码错误
    CODE_LOGIN_PASSWORD_INCORRECT = 1602

    # 用户TOKEN不存在
    CODE_TOKEN_NOT_EXISTS = 1701

    # 用户不存在
    CODE_ACCOUNT_NOT_EXISTS = 1801

    # 印象数量超过最大值
    CODE_IMPRESS_COUNT_BEYOND_MAX_COUNT = 1901
    # 印象长度超过最大值
    CODE_IMPRESS_LENGTH_BEYOND_MAX_LENGTH = 1902

