import random


# data base of account
# we can add a or multiple account in it, like this '{'account': 'xxxxxxxxxxx', 'password': 'yyyyyyyy'},'
_VALID_ACCOUNT = (
    {'username': '18711111134', 'password': '456789'},  # 结果页
    {'username': '18711111234', 'password': '456789'},  # YB字体
    {'username': '18711111113', 'password': '1113'},  #
    {'username': '18700000001', 'password': '567890'},  # 所有小游戏 - 26种模式
    {'username': '13020670521', 'password': ' '},
    {'username': '18011111134', 'password': '456789'},
)


class Account:
    def __init__(self):
        self.valid_account = _VALID_ACCOUNT[random.randint(0, len(_VALID_ACCOUNT)) - 1]

    def account(self):
        return self.valid_account['username']

    def password(self):
        return self.valid_account['password']


# global variable
# a instance of account
# it can be used in any place via 'from App.student.test_data.account import VALID_ACCOUNT'
VALID_ACCOUNT = Account()
VALID_ACCOUNT.account()
VALID_ACCOUNT.password()

