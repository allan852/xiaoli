#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from xiaoli.config import setting

__author__ = 'zouyingjun'
__all = ["engine", "Session", "Base"]

if setting.DEBUG:
    database_url = "sqlite:///%(path)s/%(db_name)s.db" % setting.DB_META
    print "Using DB %s" % database_url
else:
    database_url = "mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db_name)" % setting.DB_META

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)


class BaseModel(object):
    u"""A base model that will use our database"""
    create_time = Column(DateTime, default=datetime.datetime.now)
    update_time = Column(DateTime, onupdate=datetime.datetime.now)

Base = declarative_base(bind=engine, cls=BaseModel)

del BaseModel
