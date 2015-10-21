#!-*- coding:utf-8 -*-

from xiaoli.config.base import *

DEBUG = True
# DEBUG = False

DATABASE = {
    'host': '127.0.0.1',
    'port': '27017',
    'db_name': APP_NAME
}

LOG_FILE_PATH = os.path.join(os.path.dirname(ATHENA_PATH), 'log')  # 开发环境下，log打到项目根目录下

LOG_FILE = posixpath.join(LOG_FILE_PATH, '%s.log' % APP_NAME)
API_LOG_FILE = posixpath.join(LOG_FILE_PATH, '%s_api_v1.log' % APP_NAME)
LOG_LEVEL = "DEBUG"

MEMCACHED_MACHINES = ['127.0.0.1:11211']

HOME_URL = 'http://127.0.0.1:5000'

DB_META = {
    "db_name": "xiaoli",
    "path":os.path.dirname(ATHENA_PATH)
}

SMS = {
    'username':'youli',
    'password':'youli123',
    'apikey': '2fd8eb942e6a99f4715986605f7895f7'
}