#!/usr/bin/env python
# encoding:UTF-8
import random

# data.json base of username reset toast
# we can add a or multiple password reset toast in it, like this '{'toast': 'xxxxxxxxxxx'},'
_VALID_RESETUSERNAME = (
    {'toast': '用户名重复'},
    {'toast': '手机号不能与原号码相同'},
    {'toast': ''}
)


class ResetUsernameToast:
    def __init__(self):
        self.valid_toast = _VALID_RESETUSERNAME[random.randint(0, len(_VALID_RESETUSERNAME)) - 1]

    def reset_username(self):
        return self.valid_toast['toast']


# global variable
# a instance of username reset toast
# it can be used in any place via 'from App.student.test_data.reset_username_toast import VALID_RESETUSERNAME'
VALID_RESETUSERNAME = ResetUsernameToast()
VALID_RESETUSERNAME.reset_username()


