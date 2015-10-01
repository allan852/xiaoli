#!-*- coding:utf-8 -*-
import os
import posixpath

APP_NAME = 'xiaoli'

BODY_TAG = 'xiaoli'

SECRET_KEY = 'xiaoli'

DEFAULT_INIT_LOCALE = 'zh_CN'

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")

ATHENA_PATH = os.path.dirname(posixpath.dirname(__file__.replace('\\', '/')))

VERSION = open(os.path.join(ATHENA_PATH, 'VERSION'), 'r').read()

DB_META = {
    "db_name": "xiaoli",
    "user": "",
    "password": "",
    "host": "",
    "port": 3306
}


