# -*- coding: utf-8 -*-
import re
import settings as config
from settings.match import profile_setup as res
from os.path import isfile
from time import sleep
from imports import base_error
from imports.logger import Logger

__author__ = 'whoami'
__version__ = '0.1.0'
__date__ = '26.02.16 20:50'
__description__ = """
Description for the python module
"""


def filling_info(browser, **kwargs):
    def fill_search_by():
        search_by_radius = dict(
            radio=browser.get_element_or_none(
                ".//*[@id='ui-radio']/p[1]/label"),
            SeekGeo_Radius=kwargs['SeekGeo_Radius'] if
            'SeekGeo_Radius' in kwargs.keys() else None,
            SeekGeo_PostalCode=kwargs['SeekGeo_PostalCode'] if
            'SeekGeo_PostalCode' in kwargs.keys() else None
        )

        search_by_region = dict(
            radio=browser.get_element_or_none(".//*[@id='ui-radio']/label"),
            SeekGeo_Region=kwargs['SeekGeo_Region'] if
            'SeekGeo_Region' in kwargs.keys() else None
        )

        search_by = [None, search_by_radius, search_by_region]

        if search_by[search_by_value]['radio']:
            search_by[search_by_value]['radio'].click()
        else:
            raise base_error.ProxyBadError(message="Смените прокси",
                                           api=api)

        for key in search_by[search_by_value].keys():
            if 'radio' in key:
                continue

            if search_by[search_by_value][key] is None:
                logger.warning(
                    "Параметр {!r} не найден в списке настроек".format(key))
                continue

            logger.info("Заполняю {!r}".format(key))

            xpath = xpath_templates['input'].format(key)
            element = browser.get_element_or_none(xpath)
            if element is None:
                logger.error("Ой, эелемент {!r} не найден".format(key))
                continue

            if browser.filling_web_element(element, kwargs[key]):
                logger.info("Заполнен {!r}".format(key))
            else:
                logger.warning("Не удалось заполнить {!r}".format(key))

    def checkboxes_checked(more_btns_):
        nonlocal stop_list_buff
        is_target = lambda id, name, element: id in element or name in element

        while True:
            flag = False
            if more_btns_:
                more_btn = more_btns_.pop()
                try:
                    more_btn.click()
                    flag = True
                except Exception as e:
                    logger.debug(
                        "При попытке клика по кнопке возбуждено исключение "
                        "с сообщением {!r}".format(e))
                    continue

            all_checkboxes = browser.get_elements_by_xpath(
                xpath_to['checkboxes'])

            for checkbox in all_checkboxes:
                attr_id, attr_value = browser.get_element_info(
                    checkbox, ('id', 'value',))

                if is_target(attr_id, attr_value, target_checkboxes):
                    logger.info("Отмечаю {!r}".format(attr_id))

                    if browser.checkbox_checked(checkbox):
                        logger.info("Отметил {!r}".format(attr_id))
                    else:
                        logger.warning(
                            "Не удалось отметить {!r}".format(attr_id))

                    stop_list_buff.add(attr_id)
                else:
                    logger.warning(
                        "{!r} не указан в настройках".format(attr_id))

            if not flag:
                break
            else:
                browser.btn_click(xpath_to['more_submit'])

    def choice_selection(all_select_):
        nonlocal stop_list_buff

        for select in all_select_:
            attr_id = browser.get_element_info(select, 'id')
            logger.info("Попытка заполнить {!r}".format(attr_id))

            if kwargs.get(attr_id) is None:
                logger.warning("Упс! Параметр {!r} не указан в настройках"
                               "".format(attr_id))
                continue

            if browser.selection(select, kwargs.get(attr_id)):
                logger.info("{!r} присвоено значение {!r}"
                            "".format(attr_id, kwargs.get(attr_id)))
            else:
                logger.warning("Не удалось заполнить {!r}".format(attr_id))

            stop_list_buff.add(attr_id)

    def fill_textarea(all_textarea_):

        def clear_id(old_str):
            if isinstance(old_str, str):
                new_str = re.findall(r'self(.*)\_text', old_str.lower())
            else:
                new_str = None
            return new_str[0] if new_str else "None"

        nonlocal stop_list_buff

        for textarea in all_textarea_:
            attr_id = clear_id(browser.get_element_info(textarea, 'id'))
            value = kwargs.get(attr_id)

            logger.info("Пытаемся заполнить {!r}".format(attr_id))
            stop_list_buff.add(attr_id)

            if value is None:
                logger.warning(
                    "Параметр {!r} не указан в настройках".format(attr_id))
                continue

            if browser.filling_web_element(textarea, value):
                logger.info("{!r} заполнен".format(attr_id))
            else:
                logger.warning("{!r} не заполнен".format(attr_id))

    def photo_upload(photos_):
        nonlocal stop_list_buff
        stop_list_buff.add('fileupload')

        # TODO for test
        # _dir = '/home/oem/PycharmProjects/match_parser/img/Елена/'
        # photos_ = (_dir + '4XXbXxpQhKM.jpg',
        #            _dir + 'i1aeAU2S88s.jpg',)

        for photo in photos_:
            browser.refresh()

            logger.info("Начинаю загрузку картинки {!r}".format(photo))

            if not isfile(photo):
                logger.error('Файл {!r} не существует'.format(photo))
                break

            if browser.filling_web_element(xpath_to['file_upload'], photo):
                logger.info('Начинаем грузить картинку')
            else:
                logger.warning("Не удалось загрузить картинку")
                break

            for i in range(0, config.image_load_waits):
                sleep(1)
            else:
                logger.info("Картинка загружена")

            browser.take_screenshot()

    check_stop_list = lambda s1, s2: len(s1.difference(s2)) > 0

    url = res.url
    xpath_to = res.xpath_to
    xpath_templates = res.xpath_templates

    api = kwargs['api']
    logger = Logger(api)
    target_checkboxes = kwargs['checked']
    photos = kwargs['fileupload']
    search_by_value = int(kwargs['search_by_radius_or_region'])
    stop_list_buff = set()
    break_cnt_limit = 3

    logger.info("Приступаем к заполнению анкеты.")

    browser.get(url)

    fill_search_by()

    while True:
        stop_list = set(stop_list_buff)
        stop_list_buff.clear()

        element_upload_file = browser.get_element_or_none(
            xpath_to['file_upload'])

        if element_upload_file:
            photo_upload(set(photos))
        else:
            all_select = browser.get_elements_by_xpath(xpath_to['select'])
            all_textarea = browser.get_elements_by_xpath(xpath_to['textarea'])
            more_btns = browser.get_elements_by_xpath(xpath_to['more_show'])

            checkboxes_checked(more_btns)
            choice_selection(all_select)
            fill_textarea(all_textarea)

        working_end = res.last_word in browser.current_url.lower()

        if check_stop_list(stop_list, stop_list_buff):
            break_cnt_limit = 3
        else:
            break_cnt_limit -= 1

        if working_end:
            browser.take_screenshot()
            logger.info("Заполнение анкеты завершено")
            break

        if not bool(break_cnt_limit):
            raise base_error.AccountSingnupFailedError(
                api=api,
                message='Произошла какая-то ошибка. Регистрация прервана...')

        try:
            if not browser.btn_click(xpath_to['next']):
                browser.btn_click(xpath_to['next_alternate'])
        except Exception as e:
            raise base_error.AccountSingnupFailedError(
                api=api,
                message="Ошика с сообщением {!r} при попытке "
                        "перейти на следующую страницу настроек"
                        "".format(str(e)))
