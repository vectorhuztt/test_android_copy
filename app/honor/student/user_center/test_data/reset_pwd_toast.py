#!/usr/bin/env python
# encoding:UTF-8
import random

# data base of password reset toast
# we can add a or multiple password reset toast in it, like this '{'toast': 'xxxxxxxxxxx'},'
_VALID_RESETPWD = (
    {'toast': ''},
    {'toast': ''},
    {'toast': ''}
)


class ResetPwdToast:
    def __init__(self):
        self.valid_toast = _VALID_RESETPWD[random.randint(0, len(_VALID_RESETPWD)) - 1]

    def reset_pwd(self):
        return self.valid_toast['toast']


# global variable
# a instance of password reset toast
# it can be used in any place via 'from App.student.test_data.reset_pwd_toast import VALID_RESETPWD'
VALID_RESETPHONE = ResetPwdToast()
VALID_RESETPHONE.reset_pwd()


