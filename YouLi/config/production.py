#!-*- coding:utf-8 -*-

from youli.config.base import *

DEBUG = False

DATABASE = {
    'host': '0.0.0.0',
    'port': '37017',
    'db_name': 'youli',
    'user': 'eplus',
    'pwd': 'p@sswordmm',
    'replica_set_name': 'kreplset'
}

LOG_FILE_PATH = '/home/xingxin/log/youli/'

LOG_FILE = posixpath.join(LOG_FILE_PATH, 'youli.log')

MEMCACHED_MACHINES = ['115.159.102.199:11211']