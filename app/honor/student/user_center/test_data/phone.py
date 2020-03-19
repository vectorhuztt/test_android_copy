#!/usr/bin/env python
# encoding:UTF-8
import random

# data base of  phone
# we can add a or multiple phone in it, like this '{'phone': 'xxxxxxxxxxx'},'
_VALID_PHONE = (
    {'phone': '18011111111'},  # 原手机号
    {'phone': '18011111112'},  # 已注册其他手机号
    {'phone': '18011111234'},  # 未注册手机号
    {'phone': '  '},  # 两个空格
    {'phone': '           '},  # 11个空格
    {'phone': ''},  # 为空
    {'phone': '1'},  # 1个数字
    {'phone': '180111111112'},  # 12位数字
    {'phone': '81011111111'},  # 11位数字 - 非手机号
    {'phone': '你好万星在线教育学生端'},  # 中文、数字、英文字符组合 -11位
    {'phone': '20182018201'},  # 中文、数字、英文字符组合 -11位
    {'phone': 'helloworlds'},  # 中文、数字、英文字符组合 -11位
    {'phone': '你好2018world'},  # 中文、数字、英文字符组合 -11位
    {'phone': 'q12 a.w@S勿x'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
)


class Phone:
    def __init__(self):
        self.valid_phone = _VALID_PHONE[random.randint(0, len(_VALID_PHONE)) - 1]

    def username(self):
        return self.valid_phone['username']


# global variable
# a instance of phone
# it can be used in any place via 'from App.student.test_data.phone import VALID_PHONE'
VALID_PHONE = Phone()
VALID_PHONE.username()


