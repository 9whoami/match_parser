# -*- coding: utf-8 -*-

try:
    from .login import signin
    from .modifire_about_info import change_name
    from .profile_setup import filling_info
    from .registration import signup
    from .wink_for_free import send_winks
except Exception as e:
    print(e)
