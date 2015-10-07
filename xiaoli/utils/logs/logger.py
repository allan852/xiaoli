# coding=utf8

import time

from flask import abort
from functools import wraps
import traceback

from xiaoli.config import setting
from xiaoli.utils.logs.colored_logging import Logging


common_logger = Logging.getLogger('xiaoli', log_file=setting.LOG_FILE)
api_logger = Logging.getLogger('xiaoli', log_file=setting.API_LOG_FILE)


def log_error(debug=False):

    def _log_error(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if debug:
                    return traceback.format_exc(e)

                common_logger.error(traceback.format_exc(e))
                abort(500)

        return wrapper

    return _log_error


def _log(log_str, debug=False):
    if debug:
        print log_str
    else:
        common_logger.info(log_str)


def log_time(tip, debug=False):
    global_vars = globals()

    if "log_time_total_start_time" not in global_vars:
        global_vars["log_time_total_start_time"] = time.time()

    if "log_time_start_time" not in global_vars:
        global_vars["log_time_start_time"] = time.time()
        _log("\n\n", debug)
        _log(tip, debug)
        return

    now = time.time()
    log_str = "%s: %s" % (tip, now - global_vars["log_time_start_time"])
    global_vars["log_time_start_time"] = now

    _log(log_str, debug)


def log_out(debug=False):
    del globals()["log_time_start_time"]

    total_start_time = globals()["log_time_total_start_time"]
    del globals()["log_time_total_start_time"]

    _log("共用时: %s" % (time.time() - total_start_time), debug)