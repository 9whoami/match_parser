# -*- coding: utf-8 -*-
import re
from random import randint
from time import sleep
from imports import base_error
import settings as config

__author__ = 'whoami'
__version__ = '0.0.1'
__date__ = '15.03.16 0:57'
__description__ = """
This module contains for winks
"""


def take_online_users(browser, xpath):
    results = list()
    web_elements = browser.get_elements_by_xpath(xpath)
    for web_element in web_elements:
        href = web_element.get_attribute('href')
        uname = re.search(r'handle\=(.*?)\&', href)
        if uname:
            results.append(uname.group()[7:-1])
    return results


def take_link_to_winks(browser: "selenium.webdriver instance",
                       xpath: str) -> tuple:
    web_elements = browser.get_elements_by_xpath(xpath)
    results = [web_element.get_attribute('href') for web_element in
               web_elements]
    return results


def go_to_next_page(browser: "selenium.webdriver instance",
                    xpath: str) -> bool:
    web_element = browser.get_element_or_none(xpath)
    if web_element:

        try:
            web_element.click()
        except:
            return False

        return True
    else:
        return False


def take_username(browser: "selenium.webdriver instance", xpath: str) -> tuple:
    web_elements = browser.get_elements_by_xpath(xpath)
    results = [web_element.text for web_element in web_elements]
    return results


def seporator(key, value):
    key = key if seporator.api.check_username(key) else None
    if seporator.api.online_only and key and key not in seporator.online_users:
        raise AssertionError
    return key, value


def sends_winks(browser, **kwargs):
    api = kwargs['api']

    seporator.api = api
    is_not_empty = lambda key: bool(key[0])

    users = {}
    api = api
    url_online_short = '?sb=4'
    url = 'http://www.match.com/search/youmightlike.aspx'
    xpath = dict(
        username=".//span[@class='username']",
        winks=".//a[@class='wink winkPlus']",
        next_page=".//*[@id='ctl00_workarea_ymlSearch_ctl00_dspager2_"
                  "lnkNextBottom']",
        online=".//*[@id='resultsWrap']/ul/li/div/a",
    )

    if api.online_only:
        url += url_online_short

    browser.get(url)
    api.msg_info('Подготовка списка пользователей...')

    while len(users) < config.winks_cnt:
        if not api.winks_continue():
            raise base_error.WorkingEnd(
                message="Завершение работы по инициатеве пользователя.",
                api=api)

        username = take_username(browser, xpath['username'])
        link_to_winks = take_link_to_winks(browser, xpath['winks'])
        seporator.online_users = take_online_users(browser, xpath['online'])

        if not username or not link_to_winks:
            break

        try:
            users.update(dict(filter(
                is_not_empty,
                map(seporator, username, link_to_winks))))
        except AssertionError:
            break

        if not go_to_next_page(browser, xpath['next_page']):
            api.msg_info("Подготовка завершена. "
                         "Пользователей собрано: {!r}".format(str(len(users))))
            break

    if not users:
        raise base_error.WorkingEnd(message="Нет пользователей для winks",
                                    api=api)

    for cnt, user in enumerate(users):
        if not api.winks_continue():
            raise base_error.WorkingEnd(
                message="Завершение работы по инициатеве пользователя.",
                api=api)
        time_out = randint(kwargs['sleep'][0], kwargs['sleep'][1])
        api.msg_info("Уходим в ожидание в течении "
                     "{!r} секунд".format(time_out))
        sleep(time_out)
        api.msg_info('Отмечаем пользователя '
                     '{}/{}'.format(str(cnt), str(len(users))))
        try:
            browser.get(users[user])
            # .//*[@id='cta_title'] A wink is just the beginning…
            # .//*[@id='lblMessage1'] You've already winked at dadybent in the last 30 days.
            # result_text = get_text_from_element(browser,
            #                                    "//*[contains(text(),'wow')]")
            # interested
            # result_text = get_text_from_element(browser,
            #                                     "//*[contains(text(),'interested')]")

            wow_error = browser.text_contains('Wow!')
            error = browser.text_contains('Even dating has its difficulties')

            msg_error = wow_error if wow_error else error

            if msg_error:
                raise base_error.WorkingEnd(api=api, message=msg_error)
            browser.get(url)
        except base_error.BaseError:
            continue

    raise base_error.WorkingEnd(message='Подмигивания расставлены',
                                api=api)
