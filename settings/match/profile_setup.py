# -*- coding: utf-8 -*-

url = "http://www.match.com/Profile/Create/Welcome"

xpath_to = dict(
    next=".//*[@id='progress']/a[1]",
    next_alternate=".//input[@name='Next']",
    checkboxes=".//input[@type='checkbox']",
    file_upload=".//*[@id='create-cnt']/div[2]/div[1]/div/p/input",
    select=".//form[@id='create']/.//select",
    textarea=".//form[@id='create']/.//textarea",
    more_show=".//a[@class='btn-edit']",
    more_submit=".//*[@id='dialog-edit']/div/p/a[1]")

xpath_templates = dict(input=".//input[@id='{}']")

last_word = 'wowmatches'
