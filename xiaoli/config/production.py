#!-*- coding:utf-8 -*-

from xiaoli.config.base import *

DEBUG = False

LOG_FILE_PATH = '/home/xingxin/log/xiaoli/'

LOG_FILE = posixpath.join(LOG_FILE_PATH, 'xiaoli.log')

MEMCACHED_MACHINES = ['115.159.102.199:11211']

DB_META = {
    "db_name": "xiaoli",
    "user": "xiaoli",
    "password": "xiaolimm",
    "host": "",
    "port": 3306
}
