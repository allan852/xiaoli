#!-*- coding:utf-8 -*-

from xiaoli.config.base import *

DEBUG = False

LOG_FILE_PATH = '/home/eplus/log/xiaoli/'

LOG_FILE = posixpath.join(LOG_FILE_PATH, 'xiaoli.log')
API_LOG_FILE = posixpath.join(LOG_FILE_PATH, '%s_api_v1.log' % APP_NAME)

MEMCACHED_MACHINES = ['115.159.102.199:11211']

DB_META = {
    "db_name": "xiaoli",
    "user": "xiaoli",
    "password": "xiaoli",
    "host": "127.0.0.1",
    "port": 3306
}
