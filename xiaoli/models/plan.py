#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text, Table
from xiaoli.models import Base

__author__ = 'zouyingjun'

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table

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

# 方案和关键字关系表
plan_keyword_rel = Table(
    "plan_keyword_rel", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("plan_keyword_id", Integer, ForeignKey("plan_keywords.id"))
)


# 点赞表
stars = Table(
    "stars", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("account_id", Integer, ForeignKey("accounts.id"))
)

# 收藏表
collections = Table(
    "collections", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("operator_id", Integer, ForeignKey("accounts.id"))
)

