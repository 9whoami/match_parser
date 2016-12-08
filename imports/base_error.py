# -*- coding: utf-8 -*-
from settings.api_conf import Status
from .logger import Logger

__author__ = 'whoami'
__version__ = '0.0.0'
__date__ = '20.03.16 1:18'
__description__ = """
Description for the python module
"""


class BaseError(Exception):
    def __init__(self, message: str, api: "class instance"):
        self.api = api
        self.logger = Logger(self.api)
        self.message = message
        self.exception = self.__class__.__name__
        self._post_status()
        self._post_log()
        self._working_end()

    def __str__(self):
        return 'Raise an exception {!r} ' \
               'with the message {!r}'.format(self.exception, self.message)

    def _post_status(self):
        if hasattr(self, 'status') and isinstance(self.status, str) \
                and self.api:
            self.api.change_status(self.status)

    def _post_log(self):
        if hasattr(self, 'message') and isinstance(self.message, str):
            self.logger.error(self.message)

    def _working_end(self):
        if self.api:
            self.api.working_end()


class ProxyBadError(BaseError):
    def __init__(self, api, message: str = None):
        if message is None:
            message = "bad proxy"

        self.status = Status.bad_proxy
        super().__init__(message, api)


class AccountSigninError(BaseError):
    def __init__(self, api, message: str = None):
        if message is None:
            message = "account signin error"

        self.status = Status.signin_denied
        super().__init__(message, api)


class AccountBannedError(BaseError):
    def __init__(self, api, message: str = None):
        if message is None:
            message = "account banned"

        self.status = Status.acc_is_banned
        super().__init__(message, api)


class AccountSingnupFailedError(BaseError):
    def __init__(self, api, message: str = None):
        if message is None:
            message = "signup failed"

        self.status = Status.signup_failed
        super().__init__(message, api)


class WorkingEnd(BaseError):
    def __init__(self, api, message=None, status=None):
        if status:
            self.status = status

        super().__init__(message=message, api=api)


def raising(exception: "class BaseError", api=None, message: str = None):
    try:
        raise exception(message=message, api=api)
    except BaseError as e:
        return e
