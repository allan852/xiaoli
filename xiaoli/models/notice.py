#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, ForeignKey, String, Boolean, Text
from sqlalchemy import Integer
from xiaoli.models import Base

__author__ = 'zouyingjun'


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 通知接受者id, 外键
    receiver_id = Column(Integer, ForeignKey("accounts.id"))
    # 通知类型
    type = Column(String(32), nullable=False)
    # 是否已经阅读
    is_read = Column(Boolean)
    # 通知内容
    content = Column(String(2048))
    # 通知额外参数
    param = Column(Text)

