#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask.ext.script import Manager
from youli import create_app
from youli.config import setting

__author__ = 'zouyingjun'


app = create_app(setting)

manager = Manager(app)


@manager.command
def show_config():
    u"""展示所有配置信息"""
    for key in sorted(dir(setting)):
        if key.isupper():
            print key, '=', getattr(setting, key)


if __name__ == '__main__':
    manager.run()
