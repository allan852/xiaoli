# coding=utf8
from xiaoli.config import setting
from xiaoli.utils.logs.colored_logging import Logging

print "common_logger to %s" % setting.LOG_FILE
print "api_logger to %s" % setting.API_LOG_FILE
common_logger = Logging.getLogger('xiaolicommon', log_file=setting.LOG_FILE, log_level=setting.LOG_LEVEL)
api_logger = Logging.getLogger('xiaoliapi', log_file=setting.API_LOG_FILE, log_level=setting.LOG_LEVEL)
