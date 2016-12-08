#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from grab import Grab
from grab.error import GrabError
from imports import WebDriver
from imports import ThreadPool
from os import sys

__version__ = '1.1.2'


class Config:
    http = 'http://'
    split = ':'
    dog = '@'
    xpath = dict(
        ip_href="html/body/center/table[1]/tbody/tr/td[1]/a",
        proxy="html/body/center/"
              "table/tbody/tr[3]/td[2]/table/tbody/tr/td[2]/input")

    def __init__(self):
        _console_argumetns = self.create_parser().parse_args(sys.argv[1:])

        self.website = _console_argumetns.website
        self.count_limit = _console_argumetns.limit
        self.username = _console_argumetns.username
        self.password = _console_argumetns.password
        self.threads_count = _console_argumetns.thread

    @staticmethod
    def create_parser():
        parser = ArgumentParser(prog='ProxyGrabber',
                                description='Выдергивает и чекает прокси',
                                epilog='''(c) April 2016. Автор программы, как всегда,
                                не несет никакой ответственности ни за что.''',
                                add_help=False
                                )
        parser.add_argument('-h', '--help', action='help', help='Справка')
        parser.add_argument('--version', action='version',
                            help='Вывести номер версии',
                            version='%(prog)s {}'.format(__version__))
        parser.add_argument('-t', '--thread', nargs='?', default=1, type=int,
                            help='Количество потоков. По умолчанию 1',
                            metavar='КОЛИЧЕСТВО')
        parser.add_argument('-l', '--limit', nargs='?', default=1, type=int,
                            help='Количество выводимых на экран проксей. '
                                 'По умолчанию 1',
                            metavar='КОЛИЧЕСТВО')

        parser.add_argument('-u', '--username', nargs='?', default=None,
                            required=True, type=str,
                            help='Имя пользователя', metavar='ЛОГИН')
        parser.add_argument('-p', '--password', nargs='?', default=None,
                            required=True, type=str,
                            help='Пароль', metavar='ПАРОЛЬ')

        parser.add_argument(
            '-w', '--website', nargs='?',
            default="217.23.8.207/socks/?l1=US&l2=aa&l3=aa&ipmask=", type=str,
            help='Url сайта без http://. '
                 'По умолчанию 217.23.8.207/socks/?l1=US&l2=aa&l3=aa&ipmask=',
            metavar='URL')

        return parser


def checker(fun):
    def wrapper(p_list):
        for proxy in p_list:
            fun(page_load(proxy))

    return wrapper

@checker
@ThreadPool.thread
def proxy_validation(proxy):
    g = Grab()
    g.setup(proxy=proxy, proxy_type='socks5', connect_timeout=5, timeout=60)
    try:
        g.go('http://www.match.com/')
    except GrabError:
        return False
    else:
        proxy_list.append(proxy)
        return True
    finally:
        del g


@ThreadPool.in_lock
def page_load(url):
    br.get(url)
    web_element = br.get_element_or_none(xpath['proxy'])
    return br.get_element_info(web_element, 'value')


config = Config()
xpath = config.xpath
website = config.website
username = config.username
password = config.password
http = config.http
split = config.split
dog = config.dog
count_limit = config.count_limit

br = WebDriver()
br.get(http + username + split + password + dog + website)
hrefs = br.get_elements_by_xpath(xpath['ip_href'])
hrefs = [br.get_element_info(element, 'href') for element in hrefs]
proxy_list = []

tp = ThreadPool(max_threads=config.threads_count)
for i, href in enumerate(hrefs[::count_limit]):
    start = i * count_limit
    end = start + count_limit

    proxy_validation(hrefs[start:end])

    tp.loop()

    if count_limit and len(proxy_list) >= count_limit:
        print(proxy_list)

        if input("Continue? y/n: ") in 'n':
            break
        else:
            proxy_list.clear()
else:
    if proxy_list:
        print(proxy_list)
