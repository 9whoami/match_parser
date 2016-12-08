#!/usr/bin/python3
# -*- coding: utf-8 -*-
import settings as config
import sys
from argparse import ArgumentParser
from imports import base_error
from imports import Logger
from imports import ThreadPool
from imports import ApiMethods
from imports import WebDriver
from sites.match import signin
from sites.match import send_winks

__author__ = 'whoami'
__version__ = '0.0.0'
__date__ = '07.03.16 18:21'
__description__ = """
Description for the python module
"""


@ThreadPool.thread
def start_winks(**kwargs):
    api = kwargs['api'] = ApiMethods(custom_id=kwargs['uid'])
    logger = Logger(api)
    try:
        browser = WebDriver(**kwargs)
        if not api.winks_continue():
            raise base_error.WorkingEnd(
                message="Работа завершена пользователем", api=api)
        signin(browser, **kwargs)
        send_winks(browser, **kwargs)
    except Exception as e:
        logger.debug("Поймано исключение с сообщением {!r}".format(str(e)))
    finally:
        base_error.raising(base_error.WorkingEnd, api=api)
        return


def main(uid, btn_freeze):
    thread_pool = ThreadPool(max_threads=config.thread_count)
    api = ApiMethods()

    match_data = api.get_signin_data(**dict(id=uid))
    timeout_winks = [match_data.__next__(), match_data.__next__()]

    for signin_data in match_data:
        working_data = dict(
            uid=signin_data['id'],
            sleep=timeout_winks,
            login=signin_data['email'],
            acc_pass=signin_data['acc_pass'],
            name=signin_data['name'],
            # proxy="69.113.241.140:9752",
            proxy=signin_data.get('socks'),
            proxy_type=config.proxy_type,
            user_agent=signin_data['user_agent'],
            online=bool(signin_data.get('online')),
            btn_freeze=btn_freeze,
            answer=signin_data.get('answer'))

        start_winks(**working_data)

    thread_pool.loop()


def create_parser():
    parser = ArgumentParser(prog='WinksForFree',
                            description='Подмигивает пользователям на сайте',
                            epilog='''(c) April 2016. Автор программы, как всегда,
                            не несет никакой ответственности ни за что.''',
                            add_help=False
                            )
    parser.add_argument('-h', '--help', action='help', help='Справка')

    parser.add_argument('-i', '--id', nargs='?', default=None, type=int,
                        help='Параметр id', metavar='ID')
    parser.add_argument('-f', '--freeze', nargs='?', default=20, type=int,
                        help='Таймаут после нажатия на кнопку',
                        metavar='КОЛИЧЕСТВО')
    return parser


if __name__ in "__main__":
    arguments = create_parser().parse_args(sys.argv[1:])

    uid = arguments.id
    btn_freeze = arguments.freeze

    if uid is not None:
        config.thread_count = 1
    # uid = int(input('Type id:'))
    main(uid, btn_freeze)
