#!-*- coding:utf-8 -*-

from youli.config.base import *

DEBUG = False

DB = {
    'host': '0.0.0.0',
    'port': '37017',
    'db_name': 'athena',
    'user': 'eplus',
    'pwd': 'p@sswordmm',
    'replica_set_name': 'kreplset'
}

LOG_FILE_PATH = '/home/xingxin/log/athena/'

LOG_FILE = posixpath.join(LOG_FILE_PATH, 'athena.log')

MEMCACHED_MACHINES = ['115.159.102.199:11211']