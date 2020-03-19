#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI

phone_data = (
    {'account': '182111', 'toast': ''},  # 无错误提示信息
    {'account': '18764552343', 'toast': '手机号,不存在'},
    {'account': '11111111111', 'toast': '手机号 格式不正确'},
    {'account': '17711110000'},
)

pwd_data = [
    {'password': '', 'confirm': '', 'assert': ''},
    {'password': '        ', 'confirm': '        ', 'assert': ''},
    {'password': '456789', 'confirm': '123546', 'assert': '密码 输入不一致'},
    {'password': '123', 'confirm': '123', 'assert': '密码 格式不正确'},
    {'password': 'ab45678912345cde67890', 'confirm': 'ab45678912345cde67890', 'assert': '密码 格式不正确'},
    {'password': 'ab123#$/345cde89', 'confirm': 'ab123#$/345cde89', 'assert': '密码 格式不正确'},
    {'password': '123456', 'confirm': '123456'},
]
