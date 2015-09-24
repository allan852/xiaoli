#!-*- coding:utf-8 -*-
import os
import posixpath

APP_NAME = 'youli'

BODY_TAG = 'athena'

SECRET_KEY = 'athena'

DEFAULT_INIT_LOCALE = 'zh_CN'

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "log")

ATHENA_PATH = os.path.dirname(posixpath.dirname(__file__.replace('\\', '/')))

VERSION = open(os.path.join(ATHENA_PATH, 'VERSION'), 'r').read()

TEMP_DIR = '/home/xingxin/tmp'
