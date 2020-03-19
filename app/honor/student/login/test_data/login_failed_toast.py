#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import random


# data.json base of login failed toast
# we can add a or multiple login failed toast in it, like this '{'toast': 'xxxxxxxxxxx'},'
_VALID_LOGIN_TOAST = (
    {'toast': '手机号或密码错误'},
)


class LoginFailedToast:
    def __init__(self):
        self.valid_toast = _VALID_LOGIN_TOAST[random.randint(0, len(_VALID_LOGIN_TOAST)) - 1]

    def login_failed(self):
        return self.valid_toast['toast']


# global variable
# a instance of login failed toast
# it can be used in any place via 'from App.student.test_data.login_failed_toast import VALID_LOGIN_TOAST'
VALID_LOGIN_TOAST = LoginFailedToast()
VALID_LOGIN_TOAST.login_failed()


