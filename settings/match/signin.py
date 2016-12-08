# -*- coding: utf-8 -*-

url = "https://secure.match.com/login/index/#/"

is_bloked = "has been blocked"

is_bad_proxy = 'Упс, кажется упали прокси'

xpaths = dict(
    login=".//input[@id='email']",
    password=".//input[@id='password']",
    btn=".//button[@type='submit']",
    error_text='.//dd[@class="ng-scope ng-binding"]',
    signout=".//*[@id='ctl00_matchHeader_ctl00_PrimaryNavigationRepeater1_ctl09_Repeater1_ctl03_HyperLink4']")
