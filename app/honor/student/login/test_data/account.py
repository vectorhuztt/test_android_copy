import json
import os
import random


# data base of account
# we can add a or multiple account in it, like this '{'account': 'xxxxxxxxxxx', 'password': 'yyyyyyyy'},'
import yaml

current_path = os.path.abspath(os.path.dirname(__file__))
yaml_path = current_path.split('app\\')[0] + 'conf\\user_info.yaml'
yaml_info = json.dumps(yaml.load(open(yaml_path, 'r').read()))
user_info = json.loads(yaml_info)['userinfo']['AnyPhone']


class Account:
    def __init__(self):
        self.valid_account = user_info

    def account(self):
        return self.valid_account['userphone']

    def password(self):
        return self.valid_account['password']


# global variable
# a instance of account
# it can be used in any place via 'from App.student.test_data.account import VALID_ACCOUNT'
VALID_ACCOUNT = Account()
VALID_ACCOUNT.account()
VALID_ACCOUNT.password()
