#!-*- coding:utf-8 -*-

from xiaoli.config.base import *

DEBUG = False

DATABASE = {
    'host': '0.0.0.0',
    'port': '37017',
    'db_name': 'xiaoli',
    'user': 'eplus',
    'pwd': 'p@sswordmm',
    'replica_set_name': 'kreplset'
}

LOG_FILE_PATH = '/home/xingxin/log/xiaoli/'

LOG_FILE = posixpath.join(LOG_FILE_PATH, 'xiaoli.log')

MEMCACHED_MACHINES = ['115.159.102.199:11211']