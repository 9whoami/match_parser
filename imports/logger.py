# -*- coding: utf-8 -*-
import logging
from os.path import isfile
from datetime import datetime
import settings as config

__author__ = 'whoami'
__version__ = '0.0.0'
__date__ = '27.03.16 0:46'
__description__ = """
Оборачиваем работу проекта в лог
"""


class SingletonMetaclass(type):
    """
    Метаксласс для разовой инициализации класса Logger и возврата
    объекта логгера
    """
    def __init__(cls, *args, **kw):
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(
                SingletonMetaclass, cls).__call__(*args, **kw)
        return cls.instance


class Logger(metaclass=SingletonMetaclass):
    def __init__(self, api):
        self.api = api
        log_msg_format = '%(asctime)s.%(msecs)d %(levelname)s in ' \
                         '\'%(module)s\' at line %(lineno)d: %(message)s'

        level = logging.DEBUG if config.debug else logging.INFO


        log_filename = config.log_path + '{}.log'.format(str(datetime.now()))
        formatter = logging.Formatter(log_msg_format)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)

        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(formatter)

        self.logger.addHandler(console)
        if not isfile(log_filename):
            try:
                with open(log_filename, 'w') as _:
                    pass
                file_handler = logging.FileHandler(log_filename)
                file_handler.setFormatter(formatter)
                file_handler.setLevel(level)
                self.logger.addHandler(file_handler)
            except Exception:
                pass

    def info(self, msg):
        html_source = """
        <b style="color: #04B404">INFO:</b> <pre>{}</pre>
        """
        if self.api and self.api.session_id \
                and self.logger.isEnabledFor(logging.INFO):
            self.api._logger(html_source.format(msg))
        self.logger.info(msg)

    def error(self, msg):
        html_source = """
        <b style="color: #FE2E2E">ERROR:</b> <pre>{}</pre>
        """
        if self.api and self.api.session_id \
                and self.logger.isEnabledFor(logging.ERROR):
            self.api._logger(html_source.format(msg))
        self.logger.error(msg)

    def warning(self, msg):
        html_source = """
        <b style="color: #AEB404">WARNING:</b> <pre>{}</pre>
        """
        if self.api and self.api.session_id \
                and self.logger.isEnabledFor(logging.WARNING):
            self.api._logger(html_source.format(msg))
        self.logger.warning(msg)

    def critical(self, msg):
        html_source = """
        <b style="color: #FE2E2E">CRITICAL:</b> <pre>{}</pre>
        """
        if self.api and self.api.session_id \
                and self.logger.isEnabledFor(logging.CRITICAL):
            self.api._logger(html_source.format(msg))
        self.logger.critical(msg)

    def debug(self, msg):
        html_source = """
        <b style="color: #5882FA">DEBUG:</b> <pre>{}</pre>
        """
        if self.api and self.api.session_id \
                and self.logger.isEnabledFor(logging.DEBUG):
            self.api._logger(html_source.format(msg))
        self.logger.debug(msg)
