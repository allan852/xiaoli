#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from xiaoli.models.base import Base

__author__ = 'roc'

class Sms(Base):
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True, autoincrement=True)

    phone = Column(String(32),nullable=False)

    code = Column(String(32),nullable=False)

    def __init__(self, phone, code):
        self.phone = phone
        self.code = code
