#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Table, Column, Integer, ForeignKey
from xiaoli.models.base import Base

__author__ = 'zouyingjun'

# 用户好友关系表
# account_friends_rel_table = Table(
#     "account_friends_rel", Base.metadata,
#     Column("account_id", Integer, ForeignKey("accounts.id"), primary_key=True),
#     Column("friend_account_id", Integer, ForeignKey("accounts.id"), primary_key=True)
# )

# 方案和关键字关系表
plan_keyword_rel_table = Table(
    "plan_keyword_rel", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("plan_keyword_id", Integer, ForeignKey("plan_keywords.id"))
)


# 点赞表
account_plan_vote_rel_table = Table(
    "account_plan_vote_rel", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("account_id", Integer, ForeignKey("accounts.id"))
)

# 收藏表
account_plan_favorite_rel_table = Table(
    "account_plan_favorite_rel", Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id")),
    Column("operator_id", Integer, ForeignKey("accounts.id"))
)