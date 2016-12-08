#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from imports import WebDriver


def main():
    """
    Удаляет все аккаунты в панели!!!
    :return:
    """
    br = WebDriver()
    while True:
        br.get('http://87.118.104.243:8380/acc.php')
        del_btn = br.find_element_by_partial_link('Del')
        if del_btn is None:
            break
        del_btn.click()
        br.switch_to_alert().accept()

if __name__ in '__main__':
    main()
