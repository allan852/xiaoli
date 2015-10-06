#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, ForeignKey, String, Boolean, Text
from sqlalchemy import Integer
from xiaoli.models.base import Base

__author__ = 'zouyingjun'


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 反馈用户id, 外键
    account_id = Column(Integer, ForeignKey("accounts.id"))
    # 反馈类型
    type = Column(String(32), nullable=False)
    # 是否已经处理完成
    is_disposed = Column(Boolean)
    # 反馈内容
    content = Column(String(2048))

