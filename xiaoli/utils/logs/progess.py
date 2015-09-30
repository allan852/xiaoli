# -*- coding: utf-8 -*-


"""
统计进度
"""

import time
import datetime

__author__ = 'yeshiming@gmail.com'

import sys


class Progress(object):
    """
    Measure Progress, print messages like:
    (1/100) 1.00% 0:00:49.500000
    (2/100) 2.00% 0:00:49
    (3/100) 3.00% 0:00:48.500000
    (4/100) 4.00% 0:00:48
    (5/100) 5.00% 0:00:47.500000
    (6/100) 6.00% 0:00:47

    import time
    p = Progress(100, 1, flash=True)
    for i in range(100):
        time.sleep(0.5)
        p.p()
    """

    def __init__(self, total, step=1, flash=False):
        self.total = total
        self.step = step
        self.i = 0
        self.start_time = time.time()
        self.i_v = 0
        self.flash = flash

    def _multi_step(self, msg=""):
        self.i += self.step
        remained = ((self.total - self.i) * 1.0 / self.i) * (time.time() - self.start_time)
        ret = "(%d/%d) %.2f%% %s " % (
            self.i, self.total, self.i * 100.0 / self.total, str(datetime.timedelta(seconds=remained)) + msg)

        self._print(ret)

    def _print(self, ret):
        if self.flash:
            sys.stdout.write("\r" + ret)
        else:
            print ret


    def p(self, msg=""):

        """
        执行相应的操作，再运行此方法。
        :param msg:
        :return: None
        """
        if self.step > 1:
            return self._multi_step(msg)
        self.i_v += 1
        _i = self.i_v
        if _i % self.step:
            return
        self_total = self.total
        remained = ((self_total - _i) * 1.0 / _i) * (time.time() - self.start_time)
        ret = "(%d/%d) %.2f%% %s " % (
            _i, self_total, _i * 100.0 / self_total, str(datetime.timedelta(seconds=remained)) + msg)

        self._print(ret)


if __name__ == '__main__':
    import time

    p = Progress(100, 1)
    for i in range(100):
        time.sleep(0.5)
        p.p()