# -*- coding: utf-8 -*-

__author__ = 'whoami'
__date__ = '16.03.16 12:11'
__description__ = """
Методы для работы с апи
"""


class Status:
    # Зарегистрированный пользователь
    signup_success = "2"

    # В процессе регистрации
    signup_process = "1"

    # Добавленный пользователь
    added_user = "0"

    # Не смог зарегистрировать
    signup_failed = "-1"

    # Плохая прокси
    bad_proxy = "-2"

    # не подходит логи/пасс
    signin_denied = "-3"

    # аккаунт в бане
    acc_is_banned = "-4"

# Фигурные скобки вконце обязательны
with open('server_conf.cfg', 'r') as f:
    main_url = f.read()

# Получение данных для регистрации
signup = "api/for_reg.php"

# Получение данных для лайков
signin = "api/login"

# Отправка юзерагента. Вместо фигурных скобок подставляется id
post_useragent = "api/acc/{id}/user-agent"

# Проверка на подмигивания.
# Вместо фигурных скобок подставляется имя пользователя.
check_user = "api/check_wink/{username}"

# Добавление пользователя
post_user = "api/wink/{username}"

# Завершение работы
working_end = "api/power/off"

# Остановка работы по ид
working_end_with_id = "api/login/power/stop/{id}"

# Проверка работы
working_check = "api/power"

# Проверка работы с id. Вместо {} подставится id
working_check_with_id = "api/login/power/check/{id}"

# Отправка логов. Вместо скобок подставится id. Метод POST
logs = "api/log/acc/{id}"

# Изменеие статуса. Вместо 0 будет подставлен id, вместо 1 - статус
change_status = "api/acc/{id}/status/{status}"

# Изменение логина
get_user_for_change = 'api/login?id={id}'

# URI для статистики
statistics = "api/stat/"
