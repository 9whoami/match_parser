# -*- coding: utf-8 -*-
import re
from imports.email import EmailBox
from imports import base_error
import settings as config
from imports.logger import Logger

__author__ = 'whoami'
__version__ = '0.0.0'
__date__ = '22.03.16 5:15'
__description__ = """
Description for the python module
"""


def activate(br, **kwargs):
    msg_cnt_limit = 10
    active = False
    api = kwargs['api']
    logger = Logger(api)

    logger.info("Приступаем к активации аккаунта")
    try:
        messages = EmailBox().get_emails(kwargs['email'], kwargs['mail_pass'])
    except Exception as e:
        logger.debug(e)
        raise base_error.AccountSingnupFailedError(
            message="Ошибка подключения к почте!", api=api)

    message = []
    for i, message_buff in enumerate(messages):
        if i == msg_cnt_limit:
            break

        try:
            results = set(re.findall(config.reg_exp_link_to_confirm, message_buff.lower()))
            message += results
        except Exception as e:
            logger.debug(e)
            continue

    for result in message:
        try:
            href = result.decode('utf-8')
            href = href.lower()
            if 'trackingid' not in href or 'bannerid' not in href or 'emailid' not in href:
                raise Exception
        except Exception:
            continue
        try:
            br.get(href)
        except Exception as e:
            logger.debug(e)
            return active
        else:
            active = True

    return active
