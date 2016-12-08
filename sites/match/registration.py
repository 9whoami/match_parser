# -*- coding: utf-8 -*-
from imports import base_error
from settings.api_conf import Status
from settings.match import signup as config
# from imports.logger import Logger

__author__ = 'whoami'
__version__ = '0.1.1'
__date__ = '26.02.16 18:53'
__description__ = """
Description for the python module
"""


def check(browser, xpath):
    text = browser.get_element_or_none(xpath)
    return not text


def step_1(browser, xpaths, **kwargs: "gender: str, zip: str") -> bool:
    try:
        assert browser.selection(xpaths['gender_seek'], kwargs['gender'])
        assert browser.filling_web_element(xpaths['zip_code'], kwargs['zip'])
        assert browser.btn_click(xpaths['step_1'])
    except AssertionError:
        return False
    else:
        return check(browser, xpaths['validation_text']['zip_code'])


def step_2(browser, xpaths, **kwargs: "email: str") -> bool:
    try:
        assert browser.filling_web_element(xpaths['email'], kwargs['email'])
        assert browser.btn_click(xpaths['step_2'])
    except AssertionError:
        return False
    else:
        return check(browser, xpaths['validation_text']['email'])


def step_3(browser, xpaths,
           **kwargs: "passwd: str, b_day: str, b_month, b_year") -> bool:
    try:
        assert browser.filling_web_element(xpaths['passwd'], kwargs['passwd'])
        assert browser.selection(xpaths['birth_day'], kwargs['b_day'])
        assert browser.selection(xpaths['birth_month'], kwargs['b_month'])
        assert browser.selection(xpaths['birth_year'], kwargs['b_year'])
        assert browser.btn_click(xpaths['step_3'])
    except AssertionError:
        return False
    else:
        return True


def step_4(browser, xpaths, **kwargs: "username: str") -> bool:
    try:
        assert browser.filling_web_element(
            xpaths['username'], kwargs['username'])
        assert browser.btn_click(xpaths['step_4'])
    except AssertionError:
        return False
    else:
        return True


def signup(browser, **kwargs):
    """
    Параметры kwargs
    zip - валидный индекс
    name - имя пользователя только буквы
    birthDay -целое число от 1 до 31
    birthMonth - целое число от 1 до 12
    birthYear - целое число от 1960 до 2008
    email - емайл адресс для регистрации
    password - пароль из цифр и букв
    SelfGender_GenderSeek - пол, текст из выпадающего списка, как на сайте

    :param browser:
    :param kwargs:
    :return:
    """
    url = config.url
    xpaths = config.xpaths
    api = kwargs['api']
    # logger = Logger(api)

    browser.get(url)

    api.change_status(Status.signup_process,
                                message='Начинаем регистрировать пользователя')
    working_data = dict(
        gender=kwargs['answer']['genderGenderSeek'],
        zip=kwargs['zip'],
        email=kwargs['email'],
        passwd=kwargs['acc_pass'],
        mail_passwd=kwargs['mail_pass'],
        b_day=kwargs['birthDay'],
        b_month=kwargs['birthMonth'],
        b_year=kwargs['birthYear'],
        username=kwargs['name']
    )

    if not step_1(browser, xpaths, **working_data):
        raise base_error.AccountSingnupFailedError(message="Не верный zip код",
                                                   api=api)

    if not step_2(browser, xpaths, **working_data):
        base_error.raising(base_error.AccountSingnupFailedError,
                           message="Этот email уже есть в системе", api=api)
        return False

    if not step_3(browser, xpaths, **working_data) or \
            not step_4(browser, xpaths, **working_data):
        raise base_error.AccountSingnupFailedError(
            message="Регистрация не удалась", api=api)

    return True
