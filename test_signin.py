# -*- coding: utf-8 -*-
import settings as config
import sys
from imports import ApiMethods
from imports import WebDriver
from sites.match import signin

__author__ = 'whoami'
__version__ = '0.1.0'
__date__ = '15.03.16 6:57'
__description__ = """
Description for the python module
"""


def start_testing(**kwargs):
    """
    email, password, socks, user_agent
    :param browser:
    :param kwargs:
    :return:
    """
    working_data = dict(
        proxy=kwargs.get('socks'),
        proxy_type=config.proxy_type,
        user_agent=kwargs['user_agent'],
        login=kwargs['email'],
        password=kwargs['acc_pass'],
        name=kwargs['name'],
        api=kwargs['api'])

    br = WebDriver(**working_data)

    signin(br, **working_data)

    input("Type Enter to exit...")

    working_data['api'].working_end()


if __name__ == '__main__':
    try:
        uid = sys.argv[1]
    except Exception:
        raise SystemExit('Необходимо указать параметр')

    api = ApiMethods()

    accounts = api.get_signin_data(**dict(id=uid))

    try:
        while True:
            account = accounts.__next__()
            if isinstance(account, dict):
                break
    except StopIteration:
        raise SystemExit('Нет данных для работы')

    account['api'] = api

    start_testing(**account)
