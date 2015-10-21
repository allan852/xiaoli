#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
from flask.ext.script import Manager, prompt_bool
from sqlalchemy.orm.exc import NoResultFound
from xiaoli import create_app
from xiaoli.config import setting
from xiaoli import models
from xiaoli.models import Account
from xiaoli.models.base import Base, engine
from xiaoli.models.session import db_session_cm

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


@manager.command
def build_sample_db():
    u"""初始化数据"""
    user_data = [
        {"cellphone": 18600000000, "nickname": "admin", "email": "admin@admin.com", "password": "admin", "type": Account.TYPE_ADMIN}
    ]

    with db_session_cm() as session:
        # init uses
        for ud in user_data:
            user = Account(ud.get("cellphone"), ud.get("password"))
            user.nickname = ud.get("nickname")
            user.email = ud.get("email")
            session.add(user)
        session.commit()


@manager.command
def set_admin_user(phone=None):
    u"""
    设置用户为管理员
    用法(在项目根目录执行下列命令)：
    线下：python console.py set_admin_user -p=手机号
    线上：XIAOLI_ENV=production PYTHONPATH=. python console.py set_admin_user -p=手机号
    """
    if not phone:
        print "No phone given! Exit"
        return

    with db_session_cm() as session:
        try:
            user = session.query(Account).filter(Account.cellphone == phone).one()
            if user.is_admin:
                print "phone %s is admin now!" % phone
                return
            user.type = Account.TYPE_ADMIN
            session.add(user)
            session.commit()
            print "Set user[%s] to admin" % phone
        except NoResultFound as e:
            print "phone %s not exists!" % phone
        except Exception as e:
            print traceback.format_exc(e)


if __name__ == '__main__':
    manager.run()
