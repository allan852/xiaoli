# -*- coding: utf-8 -*-
import time

__author__ = 'yeshiming@gmail.com'

class TimeMarker(object):

    def __init__(self, title="default"):
        self.t = time.time()
        self.title = title

    def mark(self, msg = 'rubbish'):
        output = "Time mark(%s:%s): %.2f" % (self.title, msg, time.time() - self.t)
        print output
        self.t = time.time()

    def m(self, msg = 'rubbish'):
        return self.mark(msg)
