#!/usr/bin/python3
# -*- coding: utf-8 -*-
import settings as config
import settings.api_conf as api_config
import sys
from imports import base_error
from imports import ApiMethods
from imports import Logger
from imports import WebDriver
from sites.match import signup
from sites.match import signin
from sites.match import filling_info
from sites.match.commons import activate

__author__ = 'whoami'
__version__ = '0.1.0'
__date__ = '07.03.16 18:20'
__description__ = """
Description for the python module
"""


def prepare_working_data(account_id):
    api = ApiMethods()
    reg_data = api.get_signup_data(**dict(id=account_id))

    name = reg_data['name'][:16].lower()
    email_splited = reg_data['email'].split('@')[0].lower()
    reg_data['answer']['SeekGeo_PostalCode'] = reg_data['zip']

    if email_splited in name or name in email_splited:
        raise base_error.AccountSingnupFailedError(
            message="Имя не должно содержать логин от email`a!", api=api)
    return dict(proxy=reg_data.get('socks'), proxy_type=config.proxy_type,
                login=reg_data['email'], api=api, **reg_data)


def main(uid):
    working_data = prepare_working_data(uid)
    api = working_data['api']
    logger = Logger(api)

    br = WebDriver(**working_data)

    if not signup(br, **working_data):
        signin(br, **working_data)

    try:
        filling_info(br, api=api, **working_data['answer'])
    except base_error:
        raise base_error.WorkingEnd(api=api, message='Работа завершена')

    try:
        activation = activate(br, **working_data)
    except Exception as e:
        activation = False
        logger.debug(e)

    if activation:
        logger.info("Аккаунт активирован")
        api.change_status(api_config.Status.signup_success)
    else:
        logger.error("Не удалось активировать аккаунт...")
        api.change_status(api_config.Status.signup_failed)

    raise base_error.WorkingEnd(api=api, message='Работа завершена')


if __name__ in "__main__":
    try:
        uid = sys.argv[1]
    except:
        uid = None

    main(uid)
