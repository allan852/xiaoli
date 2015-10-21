# coding=utf8
from xiaoli.config import setting
from xiaoli.utils.logs.colored_logging import Logging

common_logger = Logging.getLogger('xiaolicommon', log_file=setting.LOG_FILE, log_level=setting.LOG_LEVEL)
api_logger = Logging.getLogger('xiaoliapi', log_file=setting.API_LOG_FILE, log_level=setting.LOG_LEVEL)
