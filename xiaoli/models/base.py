#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from xiaoli.config import setting
from xiaoli.utils.date_util import format_date

__author__ = 'zouyingjun'

database_url = setting.DATABASE_URL
print "Using DB %s" % database_url
engine = create_engine(database_url)


class BaseModel(object):
    u"""A base model that will use our database"""
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, onupdate=datetime.datetime.now)

    @property
    def screen_create_time(self):
        return format_date(self.create_time)

    @property
    def screen_update_time(self):
        return format_date(self.update_time)

Base = declarative_base(bind=engine, cls=BaseModel)
del BaseModel
