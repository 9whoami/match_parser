#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import settings as conf
from imports import base_error
from imports.logger import Logger
from random import randint
from time import sleep


def send_winks(browser, **kwargs):
    def sleep_with_interval(_from, _to=None):
        timeout = randint(_from, _to if _to else _from)
        logger.info('Уходим в ожидание на {} секунд'.format(timeout))
        sleep(timeout)

    def go_to_user_page():
        logger.info(
            'Отмечаем пользователя {}/{}'.format(_cnt, conf.winks_cnt))
        if browser.btn_click(xpath=element, freeze=btn_freeze):
            logger.info(
                'Перешли на страницу пользователя {!r}'.format(user_name))
            sleep_with_interval(*kwargs['sleep'])
            return True
        else:
            logger.error(
                'Не удалось перейти на страницу '
                'пользователя {!r}'.format(user_name))
            return False

    def search_customize(**kwargs):
        xpath = dict(
            search_by_zip=[".//*[@id='app']/.//label[@data-uia-checkbox='searchByZip']",
                           ".//*[@id='searchzip']"],
            online=[".//*[@id='app']/.//label[@data-uia-checkbox='onlineNow']",
                    ".//*[@id='basic-onlinenow']"],
            gender=[".//select[@data-uia-select='genderSeek']",
                    ".//*[@id='basic-seek']"],
            age_lower=[".//*[@id='app']/.//div/select[@data-uia-select='minAge']",
                       ".//*[@id='basic-lower']"],
            age_upper=[".//*[@id='app']/.//div/select[@data-uia-select='maxAge']",
                       ".//*[@id='basic-upper']"],
            txtmilesfrom=[".//*[@id='app']/.//input[@data-uia-text-input='distance']",
                          ".//*[@id='txtmilesfrom']"],
            txtziplocation=[".//*[@id='app']/.//input[@data-uia-text-input='zipCode']",
                            ".//*[@id='txtziplocation']"],

        )

        web_methods = dict(
            text=browser.filling_web_element,
            select=browser.selection,
            radio=browser.btn_click,
            checkbox=browser.btn_click
        )

        if bool(XPATH_INDEX) and web_methods['radio'](xpath['search_by_zip'][XPATH_INDEX]):
            logger.info('Отмечен поиск по радиусу')
        else:
            logger.error('Не удалось выбрать поиск по радиусу')

        if web_methods['select'](xpath['gender'][XPATH_INDEX], kwargs['basic-seek']):
            logger.info('Выбран пол {!r}'.format(kwargs['basic-seek']))
        else:
            logger.error('Не удалось указать пол')

        if web_methods['select'](xpath['age_lower'][XPATH_INDEX], kwargs['basic-lower']):
            logger.info('Указан возрас от {!r}'.format(kwargs['basic-lower']))
        else:
            logger.error('Не удалосьуказать возраст от...')

        if web_methods['select'](xpath['age_upper'][XPATH_INDEX], kwargs['basic-upper']):
            logger.info('Указан возрас по {!r}'.format(kwargs['basic-upper']))
        else:
            logger.error('Не удалосьуказать возраст по...')

        if kwargs.get('basic-onlinenow'):
            if web_methods['checkbox'](xpath['online'][XPATH_INDEX]):
                logger.info('Отмечен чекбокс "только онлайн"')
            else:
                logger.error('Не удалось отметить чекбокс "только онлайн"')

        if web_methods['text'](xpath['txtmilesfrom'][XPATH_INDEX], kwargs['txtmilesfrom']):
            logger.info('Радиус {!r}'.format(kwargs['txtmilesfrom']))
        else:
            logger.error('Не удалось указать радиус')

        if web_methods['text'](xpath['txtziplocation'][XPATH_INDEX], kwargs['txtziplocation']):
            logger.info('Зип код {!r}'.format(kwargs['txtziplocation']))
        else:
            logger.error('Не удалось указать ЗИП')

        # Please enter a valid postal code
        if browser.get_element_by_partial_text('//*[contains(text(),"enter a valid postal code")]'):
            raise base_error.WorkingEnd(api=api, message='Please enter a valid postal code')

    def wink_for_free():
        nonlocal _cnt
        if browser.btn_click(xpath=xpath['wink_for_free'][XPATH_INDEX], freeze=btn_freeze):
            logger.info('Подмигнули пользователю {!r}'.format(user_name))
            api.store_statistics(user_name=user_name, tach='wink')
            _cnt += 1
            return True
        else:
            logger.error(
                'Не удалось подмигнуть {!r}'.format(user_name))
            return False

    def check_error():
        wow_error = browser.text_contains('Wow!')
        error = browser.text_contains('Even dating has its difficulties')

        msg_error = wow_error if wow_error else error

        if msg_error:
            raise base_error.WorkingEnd(api=api, message=msg_error)

    xpath = dict(
        go_search=".//a[@id='ctl00_matchHeader_ctl00_PrimaryNavigationRepeater1_ctl03_HyperLink3']",
        basic_edit=[".//*[@id='app']/.//div/a[@class='_2sgcTrcNS4A2fp0i5RYket']",
                    ".//*[@id='Basics']/div[1]"],

        # online_now=".//*[@id='basic-onlinenow']",
        apply="Apply",
        results_member=[".//*[@id='app']/.//div[@class='_1IGJeGQR8Gdyljv-Irj2MI']/a",
                        ".//*[@id='form-search-results']/div[3]/div/div/dl/dd[1]/a"],
        wink_for_free=[".//*[@id='app']/.//div[@data-uia-wink-sent='false']/button",
                       ".//*[@id='module-user']/div[2]/div[2]/a"],
        next_page="Next"
    )

    api = kwargs['api']
    # TODO for test
    kwargs['sleep'] = [1, 5]
    btn_freeze = kwargs['btn_freeze']
    logger = Logger(api)
    _cnt = 1

    # prepare for search
    if browser.btn_click(xpath=xpath['go_search'], freeze=btn_freeze):
        logger.info("Перешли на страницу поиска")
    else:
        return logger.error("Не удалось перейти на страницу поиска!")


    if browser.btn_click(xpath=xpath['basic_edit'][0], freeze=btn_freeze):
        XPATH_INDEX = 0
    elif browser.btn_click(xpath=xpath['basic_edit'][1], freeze=btn_freeze):
        XPATH_INDEX = 1
    else:
        raise base_error.WorkingEnd(api=api,
            message="Не удалось подобрать xpath :(")

    if kwargs.get('answer'):
        search_customize(**kwargs['answer'])

    browser.btn_click(browser.get_element_by_partial_text(xpath['apply']), freeze=btn_freeze)
    # search user for wink
    while True:
        sleep_with_interval(*kwargs['sleep'])
        logger.info('Собираем результаты поиска')
        elements = browser.get_elements_by_xpath(xpath=xpath['results_member'][XPATH_INDEX])

        for element in elements:
            user_name = element.text
            if api.check_username(user_name):
                break
        else:
            element = None
            user_name = None

        # check the search results and the completion of work in the panel
        # and over limit
        # if not element:
        #     logger.error("Нет пользователей для подмигивания")
        #     break

        if not api.winks_continue():
            logger.info("Вы сами завершили работу скрипта")
            break
        elif _cnt >= conf.winks_cnt:
            logger.info("Превышение лимита на подмигивания")
            break

        if user_name:
            # wink for user
            if not go_to_user_page():
                logger.warning("Не удалось перейти на страницу пользователя")
                continue

            if not wink_for_free():
                logger.warning('Не удалось подмигнуть пользователю')
                if kwargs['name'] not in browser.page_source:
                    raise base_error.BaseError(
                        api=api, message='Меня выкинуло из аккаунта')
                browser.back()
                continue
            # check error
            try:
                check_error()
            except base_error:
                return

            browser.back()
            sleep_with_interval(btn_freeze)
            browser.back()
        else:
            if browser.btn_click(
                    browser.get_element_by_partial_text(xpath['next_page']),
                    freeze=btn_freeze):
                logger.info('Перешли на следующую страницу')
                continue
            else:
                logger.info('Нет пользователей для подмигивания')
                break

    raise base_error.WorkingEnd(api=api, message='Работа программы завершена')
