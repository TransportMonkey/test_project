import os
from os.path import exists
import logging
from logging import INFO
from logging.handlers import TimedRotatingFileHandler
import time
from datetime import datetime


log_format = '[%(asctime)s]-p%(process)d-%(threadName)s{%(module)s:%(lineno)d}%(levelname)s-%(message)s'
log_datefmt = '%Y-%m-%d %H:%M:%S'


class DayRotatingFileHandler(TimedRotatingFileHandler):
    """ 每天0点整切割日志
    """

    def __init__(self, *args, **kwargs):
        # 强制替换时间为每天一次
        kwargs['when'] = 'D'
        super(DayRotatingFileHandler, self).__init__(
            *args,
            **kwargs
        )
        self.update_rollover_times()

    def update_rollover_times(self):
        """ 计算下次切割时间 """
        # 今天早上凌晨0点
        today_zero = int(time.mktime(datetime.now().date().timetuple()))
        self.rolloverAt = self.computeRollover(today_zero)

    def doRollover(self):
        super(DayRotatingFileHandler, self).doRollover()
        self.update_rollover_times()


class LogClass(object):
    def __init__(self):
        self.logger = None  # :type logging.Logger
        self.log_path = ''

    def init(self, log_path=None, level=logging.DEBUG):
        # k8s容器内考虑到不同pod需要输出到不同日志里
        self.log_path = log_path
        if log_path and not exists(self.log_path):
            os.makedirs(self.log_path)

        # 设置默认流输出日志信息
        logging.basicConfig(level=level,
                            format=log_format,
                            datefmt=log_datefmt,
                            # filename="%s/basic.log" % self.log_path if log_path else None,
                            )
        if not log_path:
            return
        logging.info('init log_path: %s', log_path)
        # 设置数据日志输出
        self.logger = server_logger  # logging.getLogger("server")
        self.logger.setLevel(level)
        logging.root = self.logger
        gl = globals()
        for op in ['debug', 'info', 'warning', 'error', 'exception']:
            f = getattr(self.logger, op)
            setattr(self, op, f)
            gl[op] = f

        # add default handler
        if not exists(self.log_path):
            # 输出到屏幕中
            ch = logging.StreamHandler()
            pass
        else:
            # 创建TimedRotatingFileHandler处理对象
            # 按天切割，保存180天
            # 设置日志文件后缀，以当前时间作为日志文件后缀名。
            ch = DayRotatingFileHandler(
                '%s/server.log' % self.log_path,
                # when='D', interval=1,
                backupCount=180,
                encoding='utf-8'
            )
            ch.suffix = "%Y%m%d.log"
        self.add_handler(ch, set_level=True)

    def add_handler(self, ch, set_level=None):
        if ch in self.logger.handlers:
            return
        if set_level:
            ch.setLevel(self.logger.level)
        # 设置日志输出格式
        formatter = logging.Formatter(log_format, datefmt=log_datefmt)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def del_handler(self, ch):
        self.logger.removeHandler(ch)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def exception(self, *args, **kwargs):
        self.logger.exception(*args, **kwargs)

    def setLevel(self, level):
        level = int(level)
        self.logger.setLevel(level)
        # logging.root.setLevel(level)


g_logger = LogClass()
g_logger.init()


def log_init(path, debug):
    global g_logger
    level = logging.DEBUG if debug else logging.INFO
    g_logger.init(path, level)


debug = lambda *args, **kwargs: None
info = debug
warning = debug
error = debug
exception = debug


def get_logger(name, level=logging.NOTSET):
    logger = logging.getLogger(name)
    if level == logging.NOTSET:
        if logger.level == logging.NOTSET:
            logger.setLevel(INFO)
    else:
        logger.setLevel(INFO)
    return logger


server_logger = get_logger(None)  # root
server_logger.setLevel(INFO)
