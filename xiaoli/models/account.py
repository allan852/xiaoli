#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from xiaoli.models import Base

__author__ = 'zouyingjun'


class Account(Base):
    __tablename__ = 'accounts'

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

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 昵称
    nickname = Column(String(64), unique=True, index=True)
    # 手机号
    cellphone = Column(String(32), unique=True, nullable=False, index=True)
    # email
    email = Column(String(128))
    # password, 加密后信息
    _password = Column(String(128), nullable=False)
    # salt 加密盐
    salt = Column(String(128))
    # 性别
    sex = Column(String(16))
    # 生日
    birthday = Column(DateTime)
    # 星座
    horoscope = Column(String(16))
    # 账户状态
    status = Column(String(64), nullable=False)
    # 账户类型
    type = Column(String(64), nullable=False)
    # 是否接受系统通知
    allow_notice = Column(Boolean, default=True)
    # 是否允许别人给自己打分
    allow_score = Column(Boolean, default=True)


friends = Table(
    "friends", Base.metadata,
    Column("account_id", Integer, ForeignKey("accounts.id"), primary_key=True),
    Column("friend_account_id", Integer, ForeignKey("accounts.id"), primary_key=True)
)

# class Friend(Base):
#     __tablename__ = "friends"
#
#     account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)
#     friend_account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)


class Avatar(Base):
    __tablename__ = "avatars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 头像所有者id，外键
    account_id = Column(Integer, ForeignKey("accounts.id"))
    # 头像存储路径
    path = Column(String(1024))
    # 头像格式，即图片后缀名
    format = Column(String(16))


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 被打分人id，外键
    target_id = Column(Integer, ForeignKey("accounts.id"))
    # 打分人id, 外键
    operator_id = Column(Integer, ForeignKey("accounts.id"))
    # 分数
    score = Column(Integer, default=0)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 被评论人id， 外键
    target_id = Column(Integer, ForeignKey("accounts.id"))
    # 评论人id, 外键
    operator_id = Column(Integer, ForeignKey("accounts.id"))
    # 评论内容
    content = Column(String(1024), nullable=False)


class Impress(Base):
    __tablename__ = "impresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 被添加影响人id， 外键
    target_id = Column(Integer, ForeignKey("accounts.id"))
    # 添加人id, 外键
    operator_id = Column(Integer, ForeignKey("accounts.id"))
    # 印象内容id
    content_id = Column(Integer, ForeignKey("impress_contents.id"))


class ImpressContent(Base):
    __tablename__ = "impress_contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 印象内容类型
    type = Column(String(16), nullable=False)
    # 印象内容
    content = Column(String(10), nullable=False)





