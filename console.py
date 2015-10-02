#!/usr/bin/env python
# -*- coding:utf-8 -*-
import inspect
from flask.ext.script import Manager, prompt_bool
from xiaoli import create_app
from xiaoli.config import setting
from xiaoli.models import Base, engine
from xiaoli import models
from xiaoli.models.account import Account

__author__ = 'zouyingjun'


app = create_app(setting)

manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=engine, models=models)


@manager.command
def show_config():
    u"""展示所有配置信息"""
    for key in sorted(dir(setting)):
        if key.isupper():
            print key, '=', getattr(setting, key)


@manager.command
def create_db(default_data=True, sample_data=False):
    "Creates database from sqlalchemy models"
    connect = engine.connect()
    connect.execute("CREATE DATABASE %s;" % setting.DB_META["db_name"])
    connect.close()


@manager.command
def drop_tables():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        Base.metadata.drop_all()


@manager.command
def create_tables(default_data=True, sample_data=False):
    "Creates database tables from sqlalchemy models"
    Base.metadata.create_all()


@manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop_tables()
    create_tables(default_data, sample_data)


if __name__ == '__main__':
    manager.run()
