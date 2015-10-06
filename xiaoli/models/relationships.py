#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Table, Column, Integer, ForeignKey
from xiaoli.models.base import Base

__author__ = 'zouyingjun'

friends_rel = Table(
    "friends_rel", Base.metadata,
    Column("account_id", Integer, ForeignKey("accounts.id"), primary_key=True),
    Column("friend_account_id", Integer, ForeignKey("accounts.id"), primary_key=True)
)

# class FriendRel(Base):
#     __tablename__ = "friends_res"
#
#     account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)
#     friend_account_id = Column(Integer, ForeignKey("accounts.id"), primary_key=True)

# 方案和关键字关系表
plan_keyword_rel = Table(
    "plan_keyword_rel", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("plan_keyword_id", Integer, ForeignKey("plan_keywords.id"))
)


# 点赞表
stars_table = Table(
    "stars", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("account_id", Integer, ForeignKey("accounts.id"))
)

# 收藏表
collections_table = Table(
    "collections", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("operator_id", Integer, ForeignKey("accounts.id"))
)