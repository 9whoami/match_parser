# -*- coding: utf-8 -*-
from time import sleep
from imports import base_error
from imports.logger import Logger
from settings.match import signin as resources

__author__ = 'whoami'
__version__ = '0.1.0'
__date__ = '26.02.16 20:51'
__description__ = """
Description for the python module
"""


def signin(browser, **kwargs):
    url = resources.url
    is_bloked = resources.is_bloked
    is_bad_proxy = resources.is_bad_proxy
    xpaths = resources.xpaths

    api = kwargs['api']
    logger = Logger(api)

    logger.info(
        "Пытаемся войти на сайт login: {!r} "
        "password: {!r}".format(kwargs['login'], kwargs['acc_pass']))

    browser.get(url)
    try:
        assert browser.filling_web_element(xpaths['login'], kwargs['login'])
        assert browser.filling_web_element(
            xpaths['password'], kwargs['acc_pass'])
        assert browser.btn_click(xpaths['btn'])
    except AssertionError:
        raise base_error.ProxyBadError(api=api)

    for i in range(0, 10):
        element_end = kwargs['name'] in browser.page_source
        if element_end:
            logger.info("Произведен вход в аккаунт")
            browser.take_screenshot()
            return
        sleep(3)

    browser.take_screenshot()

    if not browser.get_element_or_none(xpaths['signout']):

        error_text = browser.get_element_or_none(xpaths['error_text'])
        error_text = error_text.text if error_text else is_bad_proxy

        if is_bloked in error_text:
            raise base_error.AccountBannedError(message=error_text, api=api)
        elif is_bad_proxy in error_text:
            raise base_error.ProxyBadError(message=error_text, api=api)
        else:
            raise base_error.AccountSigninError(message=error_text, api=api)
    else:
        logger.info("Произведен вход в аккаунт")
        return
