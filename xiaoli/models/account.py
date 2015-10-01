#!/usr/bin/env python
# -*- coding:utf-8 -*-
from peewee import CharField, DateTimeField, BooleanField
from xiaoli.models import BaseModel

__author__ = 'zouyingjun'


class Account(BaseModel):

    HOROSCOPE_CHOICES = (
        ("Aries", "牡羊座"),
        ("Taurus", "金牛座"),
        ("Gemini", "雙子座"),
        ("Cancer", "巨蟹座"),
        ("Leo", "獅子座"),
        ("Virgo", "處女座"),
        ("Libra", "天秤座"),
        ("Scorpio", "天蠍座"),
        ("Sagittarius", "射手座"),
        ("Capricorn", "魔羯座"),
        ("Aquarius", "水瓶座"),
        ("Pisces", "雙魚座"),
    )

    STATUS_CHOICES = (
        ("active", "激活"),
        ("freeze", "冻结"),
    )

    TYPE_CHOICES = (
        ('user', "普通用户"),
        ('admin', "系统管理员")
    )

    # 昵称
    nickname = CharField(max_length=54, unique=True)
    # 手机号
    cellphone = CharField(max_length=32, unique=True, null=False)
    # email
    email = CharField(max_length=128)
    # password, 加密后信息
    _password = CharField(max_length=128, null=False)
    # salt 加密盐
    salt = CharField(max_length=128)
    # 性别
    sex = CharField(max_length=16)
    # 生日
    birthday = DateTimeField()
    # 星座
    horoscope = CharField(max_length=16, choices=HOROSCOPE_CHOICES)
    # 账户状态
    status = CharField(max_length=64, choices=STATUS_CHOICES)
    # 账户类型
    type = CharField(max_length=64, choices=TYPE_CHOICES)
    # 是否接受系统通知
    allow_notice = BooleanField(default=True)
    # 是否允许别人给自己打分
    allow_score = BooleanField(default=True)