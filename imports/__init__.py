# -*- coding: utf-8 -*-

from .logger import Logger
from .api_methods import ApiMethods
from .base_error import AccountBannedError, AccountSigninError, \
    AccountSingnupFailedError, ProxyBadError, WorkingEnd, raising
from .browser import WebDriver
from .email import EmailBox
from .threadpool import ThreadPool
from .virtual_display import VirtualDisplay


def prepare_working_data(**kwargs):
    gender = kwargs['answer']['genderGenderSeek']
    zip = kwargs['zip']
    email = kwargs['email']
    passwd = kwargs['password']
    b_day = kwargs['birthDay']
    b_month = kwargs['birthMonth']
    b_year = kwargs['birthYear']
    username = kwargs['name']
