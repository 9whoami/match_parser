# -*- coding: utf-8 -*-
import settings.api_conf as config
from .threadpool import ThreadPool
from .logger import Logger
from grab import Grab
from itertools import chain
from sys import exit

__author__ = 'whoami'
__version__ = '1.3.3'
__date__ = '19.02.16 23:14'
__description__ = """
Набот методов для работы с апи
"""


class ApiMethods:
    online_only = None
    acc_status = None

    def __init__(self, custom_id=None):
        self.session_id = custom_id
        self.logger = Logger(self)

    @ThreadPool.in_lock
    def _api_request(self, url, **kwargs):
        api_url = config.main_url.format(**dict(uri=url))

        g = Grab()
        try:
            g.go(api_url, post=kwargs)
            response = g.response.json
        except Exception as e:
            response = dict(error=e)
        finally:
            del g

        return response

    def get_signup_data(self, **kwargs: "pass id params"):

        uri_param = "?id={id}".format(**kwargs) if kwargs.get('id') else str()
        uri = config.signup + uri_param

        api_response = self._api_request(uri)
        self.session_id = api_response.get('id')
        if not self.session_id:
            self.logger.error("Нет данных для работы.")
            exit()

        return api_response

    def get_signin_data(self, **kwargs: "pass id params"):

        u_id = kwargs.get('id')
        if u_id:
            self.session_id = u_id

        uri_param = "?id={id}".format(**kwargs) if u_id else str()
        uri = config.signin + uri_param

        api_response = self._api_request(uri)

        if not api_response.get('status'):
            self.logger.error(
                "Работа завершена по причине {!r}".format(api_response))
            exit()

        for account_info in chain(api_response['sleep'], api_response['accs']):
            yield account_info

    def check_username(self, username: str):
        """
        method: GET

        response:
        {
        "status":true,
        "comment":"user search"
        }
        :param username:
        :return:
        """
        # uri = "/api/check_wink/{}".format(username)
        uri = config.check_user.format(**dict(username=username.lower()))

        try:
            api_response = not self._api_request(uri)['status']
        except KeyError:
            return True

        if api_response:
            self._store_username(username.lower())

        return api_response

    def get_change_user(self):
        uri = config.get_user_for_change.format(**dict(id=self.session_id))

        api_response = self._api_request(uri)

        if not api_response.get('status'):
            self.logger.error(
                "Работа завершена по причине {!r}".format(api_response))
            exit()

        return api_response

    def change_status(self, status: str, message: str = None):
        """
        method: GET/POST

        response:
        {
        "status":true,
        "id":"1",
        "comment":"change user status"
        }

        :param message:
        :param id:
        :param status:
        :return:
        """
        uri = config.change_status.format(
            **dict(id=self.session_id, status=status))
        if self.session_id is None:
            return None

        if message:
            self.logger.info(message)

        api_response = self._api_request(uri)
        self.acc_status = status
        return api_response

    def working_end(self):
        if self.session_id:
            return self._working_end_with_id()

        uri = config.working_end
        self._api_request(uri)

    def winks_continue(self):
        uri = config.working_check_with_id.format(
            **dict(id=self.session_id))
        api_response = self._api_request(uri)
        try:
            return int(api_response['status'])
        except KeyError:
            return False

    def store_statistics(self, user_name: str, tach: str) -> None:
        """
        POST:/api/stat/

        id:int
        user_name:string
        tach:wink

        :return: None
        """
        uri = config.statistics
        post_data = dict(id=self.session_id, user_name=user_name, tach=tach)

        api_response = self._api_request(uri, **post_data)

        return api_response

    def _logger(self, message):
        """
        method: POST

        request:
        {
        "message": "Регистрация прошла успешно"
        }

        response:
        {
        "status":true,
        "id":"1",
        "comment":"add new log line"
        }
        :param send_log:
        :param id:
        :param message:
        :return:
        """

        uri = config.logs.format(**dict(id=self.session_id))
        post_data = dict(message=message)

        api_response = self._api_request(uri, **post_data)

        return api_response

    def _store_username(self, username: str):
        """
        method: GET

        response:
        {
        "status":1,
        "comment":"new wink user"
        }
        :param username:
        :return:
        """
        uri = config.post_user.format(**dict(username=username))
        api_response = self._api_request(uri)
        return api_response

    def _working_end_with_id(self):
        if self.session_id:
            uri = config.working_end_with_id.format(
                **dict(id=self.session_id))
        else:
            return
        return self._api_request(uri)