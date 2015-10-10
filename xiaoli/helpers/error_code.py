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

    # 导入好友参数格式错误
    CODE_IMPORT_FRIENDS_PARAMS_FORMAT_ERROR = 2001

    # 更新用户基本信息
    # 参数取值错误
    CODE_UPDATE_INFO_PARAMS_VALUE_ERROR = 2100
    # 密码不正确
    CODE_UPDATE_INFO_INCORRECT_PASSWORD = 2101
    # 没有新密码
    CODE_UPDATE_INFO_NO_PASSWORD = 2102
    # 新密码不一致
    CODE_UPDATE_INFO_PASSWORD_NOT_EQUAL = 2103
    # 新密码和旧密码一致
    CODE_UPDATE_INFO_USE_OLD_PASSWORD = 2103


