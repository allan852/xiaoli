#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask.ext.script import Manager, prompt_bool
from xiaoli import create_app
from xiaoli.config import setting
from xiaoli.models import _db
from xiaoli import models

__author__ = 'zouyingjun'


app = create_app(setting)

manager = Manager(app)


@manager.shell
def make_shell_context():
    return dict(app=app, db=_db, models=models)


@manager.command
def show_config():
    u"""展示所有配置信息"""
    for key in sorted(dir(setting)):
        if key.isupper():
            print key, '=', getattr(setting, key)


@manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        _db.drop_all()


@manager.command
def create(default_data=True, sample_data=False):
    "Creates database tables from sqlalchemy models"
    _db.create_all()


@manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create(default_data, sample_data)


if __name__ == '__main__':
    manager.run()
