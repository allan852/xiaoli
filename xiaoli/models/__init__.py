#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from xiaoli.config import setting
from playhouse.db_url import connect
from peewee import Model, DateTimeField

__author__ = 'zouyingjun'

if setting.DEBUG:
    database_url = "sqlite://%(path)s/%(db_name)s.db" % setting.DB_META
    print "Using DB %s" % database_url
else:
    database_url = "mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db_name)" % setting.DB_META

_db = connect(database_url)


class BaseModel(Model):
    u"""A base model that will use our database"""

    class Meta:
        database = _db

    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField()

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
