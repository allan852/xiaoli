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
    # 昵称存在
    CODE_UPDATE_INFO_NICKNAME_EXISTS = 2104

    # 方案不存在
    CODE_PLAN_NOT_EXISTS = 2200

    # 上传文件大小超出限制
    CODE_UPLOAD_IMAGE_OVER_SIZE = 2300

    # 用户关闭评分
    CODE_SCORE_USER_CLOSED = 2400
    # 不可以多次评分
    CODE_SCORE_USER_MULTIPLE = 2401
    # 分数不合法
    CODE_SCORE_INVALID = 2402


