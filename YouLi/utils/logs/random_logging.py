# -*- coding: utf-8 -*-
"""
按概率打log
"""
import random
import logging
from functools import wraps
from Libs.logs.colored_logging import Logging



class RandomLogger(object):

    def __init__(self, p, log_file=None):

        self.logger = Logging.getLogger(self.__class__.__name__, log_file=log_file)
        self.logger.setLevel(logging.DEBUG)
        self.p = p

    def __getattr__(self, item):
        if item not in ['debug', 'critical', 'error', 'warn', 'info']:
            return getattr(self.logger, item)

        @wraps(getattr(self.logger, item))
        def new_func(*args, **kwargs):
            random_random = random.random()
            if random_random < self.p:
                return getattr(self.logger, item)(*args, **kwargs)

        return new_func


if __name__ == '__main__':
    pass