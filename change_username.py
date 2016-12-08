#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from imports import WebDriver
from imports import base_error
from imports import ApiMethods
from sites.match import signin
from sites.match import change_name


def main(uid):
    if uid is None:
        raise SystemExit('Требуется парамет для запуска')
    api = ApiMethods(custom_id=uid)

    try:
        api_params = api.get_change_user()['accs'][0]
    except Exception:
        raise SystemExit('Нет данных для работы')

    api_params['proxy'] = api_params.get('socks')
    api_params['api'] = api
    api_params['login'] = api_params['email']

    br = WebDriver(**api_params)

    signin(br, **api_params)
    change_name(br, **api_params)

    raise base_error.WorkingEnd(api=api, message='Работа завершена')


if __name__ == '__main__':
    try:
        uid = sys.argv[1]
    except Exception:
        raise SystemExit('Требуется парамет для запуска')

    main(uid)
