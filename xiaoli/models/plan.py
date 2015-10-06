#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from xiaoli.models import collections_table, stars_table
from xiaoli.models.base import Base


__author__ = 'zouyingjun'


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 方案名称
    title = Column(String(1024), nullable=False)
    # 方案状态
    status = Column(String(64), nullable=False)
    # 发布日期
    publish_date = Column(DateTime)
    # 作者id
    author_id = Column(Integer, ForeignKey("accounts.id"))
    # 封面图片id
    cover_image_id = Column(Integer, ForeignKey("image_resources.id"))
    # 阅读次数
    view_count = Column(BigInteger)
    # 分享次数
    share_count = Column(BigInteger)

    contents = relationship("PlanContent",backref='plan',cascade="all, delete-orphan")
    keywords = relationship("PlanKeyword",backref='plan',secondary="plan_keyword_rel")

    collectors = relationship("Account", secondary=collections_table, lazy="dynamic")
    starters = relationship("Account", secondary=stars_table, lazy="dynamic")

class PlanContent(Base):
    __tablename__ = "plan_contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 方案id， 外键
    plan_id = Column(Integer, ForeignKey("plans.id"))
    # 方案内容
    content = Column(Text, nullable=False)


class PlanKeyword(Base):
    __tablename__ = "plan_keywords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 关键字内容
    content = Column(String(128), nullable=False)
