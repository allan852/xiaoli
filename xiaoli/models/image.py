#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy import Integer
from xiaoli.models.base import Base

__author__ = 'zouyingjun'


class ImageResource(Base):
    __tablename__ = "image_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 资源创建者id, 外键
    account_id = Column(Integer, ForeignKey("accounts.id"))
    # 资源存储路径
    path = Column(String(2048), nullable=False)
    # 资源格式, 图片后缀
    format = Column(String(16))

