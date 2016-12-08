# -*- coding: utf-8 -*-
import os

try:
    from .advanced import *
    from .base import *
except Exception as e:
    raise SystemExit('Импорт настроек возбудил исключение с '
                     'сообщением {!r}'.format(str(e)))


def _prepare_path(path):
    if not path.endswith(os.sep):
        path += os.sep

    if not path.startswith(os.sep):
        path = os.sep + path

    if not os.path.isdir(path):
        path = os.getcwd() + path

    if not os.path.isdir(path):
        os.makedirs(path)

    return path


def _prepare_file(file):
    if not file.startswith(os.sep):
        file = os.sep + file

    if not os.path.isfile(file):
        file = os.getcwd() + file
        
    if not os.path.isfile(file):
        with open(file, 'w'): pass

    return file


def get_path_name(path):
    p_name = None
    path_name = path.split(os.sep)
    while True:
        p_name = path_name.pop()
        if p_name:
            break
    return p_name

try:
    log_path = _prepare_path(log_path)
    screen_dir = _prepare_path(screen_dir)

    if service_args:
        assert isinstance(service_args, list)

    driver_log = log_path + '/driver.log'
except AssertionError:
    raise SystemExit('Ошибка загрузки настроек! Убедитесь что '
                     'service_args задан верно!')
except Exception as e:
    raise SystemExit('Неизвестная ошибка! {!r}'.format(str(e)))
