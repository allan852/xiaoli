#!-*- coding:utf-8 -*-

from youli.config.base import *

DEBUG = True
# DEBUG = False

DATABASE = {
    'host': '127.0.0.1',
    'port': '27017',
    'db_name': APP_NAME
}

LOG_FILE_PATH = os.path.join(os.path.dirname(ATHENA_PATH), 'log')  # 开发环境下，log打到项目根目录下

LOG_FILE = posixpath.join(LOG_FILE_PATH, '%s.log' % APP_NAME)

MEMCACHED_MACHINES = ['127.0.0.1:11211']

HOME_URL = 'http://127.0.0.1:5000'