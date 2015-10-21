#!-*- coding:utf-8 -*-

from xiaoli.config.base import *

DEBUG = False
# DEBUG = True

LOG_FILE_PATH = '/home/eplus/log/xiaoli/'

LOG_FILE = posixpath.join(LOG_FILE_PATH, 'xiaoli.log')
API_LOG_FILE = posixpath.join(LOG_FILE_PATH, '%s_api_v1.log' % APP_NAME)
LOG_LEVEL = "INFO"

MEMCACHED_MACHINES = ['115.159.102.199:11211']

DB_META = {
    "db_name": "xiaoli",
    "user": "xiaoli",
    "password": "xiaoli",
    "host": "127.0.0.1",
    "port": 3306
}

SMS = {
    'username':'youli',
    'password':'youli123',
    'apikey': '2fd8eb942e6a99f4715986605f7895f7'
}
