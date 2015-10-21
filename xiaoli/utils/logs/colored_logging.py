#coding=utf8
'''
Created on 2011-9-25

@author: of
'''
import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class Logging:
    @staticmethod
    def getLogger(name = __name__, log_level = "debug", log_file = None):
        ## get log level.
        log_level = Logging.getLogLevel(log_level)

        ## create logger
        logger = logging.getLogger(name)
        
        ## create log handler.
        print "colored_logging handlers length = %s" % len(logger.handlers)
        if len(logger.handlers) <= 0:
            print "colored_logging add handler"
            if log_file is not None:
                handler = logging.FileHandler(log_file)
            else:
                handler = logging.StreamHandler()
                
            formatter = ColoredFormatter("%(asctime)s\t%(process)d|%(thread)d\t%(levelname)s\t%(module)s\t%(funcName)s:%(lineno)d\t%(message)s", "%Y-%m-%d@%H:%M:%S")
            #formatter = ColoredFormatter("%(thread)d\t%(levelname)s\t%(module)s\t%(funcName)s:%(lineno)d\t%(message)s", "%Y-%m-%d@%H:%M:%S")
            handler.setFormatter(formatter)
            
            logger.addHandler(handler)
            logger.setLevel(log_level)
        return logger


    @staticmethod
    def getLogLevel(log_level):
        log_level = getattr(logging, log_level.upper(), None)
        if log_level is None: raise Exception("No such log level.")
        return log_level



if __name__ == '__main__':
    logger = Logging.getLogger(log_level = "debug")
    
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    logger.setLevel(Logging.getLogLevel("error"))

    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    
    ## The output looks like this:
    # 2011-05-26@13:54:05    10006|-1215969600    DEBUG    testLogger    <module>:33    debug message
    # 2011-05-26@13:54:05    10006|-1215969600    INFO    testLogger    <module>:34    info message
    # 2011-05-26@13:54:05    10006|-1215969600    WARNING    testLogger    <module>:35    warn message
    # 2011-05-26@13:54:05    10006|-1215969600    ERROR    testLogger    <module>:36    error message
    # 2011-05-26@13:54:05    10006|-1215969600    CRITICAL    testLogger    <module>:37    critical message
    # 2011-05-26@13:54:05    10006|-1215969600    ERROR    testLogger    <module>:45    error message
    # 2011-05-26@13:54:05    10006|-1215969600    CRITICAL    testLogger    <module>:46    critical message