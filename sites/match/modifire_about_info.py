# -*- coding: utf-8 -*-
from time import sleep
from imports import base_error
from imports.logger import Logger


def change_name(browser, **kwargs):
    api = kwargs['api']
    logger = Logger(api)
    url = 'http://www.match.com/accountsettings/verifyPwd.aspx?lid=108'
    xpath = dict(
        pwd=".//*[@type='password']",
        go=".//*[@type='submit']",
        change_info=".//*[@id='ControlRegistrationConfirmation_btnContinue']",
        name=".//*[@id='ctl00_workarea_ChangeRegistrationPage1_ctl00_ShortRegistration1_ctl00_regHandle']",
        save=".//*[@id='ctl00_workarea_ChangeRegistrationPage1_ctl00_ShortRegistration1_ctl00_btnSubmitReg']",
    )
    browser.get(url)
    try:
        assert browser.filling_web_element(xpath['pwd'], kwargs['acc_pass'])
        logger.info("Заполнен пароль для доступа к настройкам")
        assert browser.btn_click(xpath['go'])

        assert browser.btn_click(xpath['change_info'])
        logger.info('Активированы поля для редактирования')
        sleep(3)
        assert browser.filling_web_element(xpath['name'], kwargs['name'])
        logger.info('Заполнен логин')
        assert browser.btn_click(xpath['save'])
        logger.info('Логин сохранен')
    except AssertionError:
        raise base_error.ProxyBadError(api=api,
                                       message='Не удалось сменить логин')
    else:
        return True
