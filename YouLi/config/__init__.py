#!-*- coding:utf-8 -*-

from youli.config import production, development, testing

__all__ = ['setting']

setting = development

import os

current_evn = os.environ.get("ATHENA_ENV") or "development"

if current_evn in ['production']:
    setting = production
elif current_evn in ['development']:
    setting = development
elif current_evn in ['testing']:
    setting = testing
else:
    setting = development

del development
del production
del testing

print "current_env = %s " % current_evn
