# -*- coding: utf-8 -*-

url = 'http://www.match.com/registration/registration.aspx'

xpaths = dict(
    gender_seek=".//select[@id='genderGenderSeek']",
    zip_code=".//input[@id='postalCode']",
    step_1=".//*[@id='progessive']/div[1]/fieldset[1]/button",

    validation_text=dict(
        zip_code=".//*[@id='progessive']/div[1]/div[1]/ul/li",
        email=".//*[@id='progessive']/div[1]/div[1]/ul/li"),

    email=".//*[@id='progessive']/div[1]/fieldset[2]/div[2]/input",
    step_2=".//*[@id='progessive']/div[1]/fieldset[2]/button",

    passwd=".//*[@id='progessive']/div[1]/fieldset[3]/div[1]/input",
    birth_day=".//*[@id='birthDay']",
    birth_month=".//*[@id='birthMonth']",
    birth_year=".//*[@id='birthYear']",
    step_3=".//*[@id='progessive']/div[1]/fieldset[3]/div[3]/button",

    username=".//*[@id='submit']/input",
    step_4=".//*[@id='submit']/button")
