#!/usr/bin/env python
# encoding:UTF-8

# 验证当前密码、新密码与确认密码输入要一致；密码由6~20位英文及数字组成
reset_pwd = (
    {'old': '123456', 'new': ' ', 'commit': ' ', 'assert': ' 密码 格式不正确'},  # 1个空格
    {'old': '123456', 'new': '      ', 'commit': '      '},  # 多个空格 -6个
    {'old': '123456', 'new': '', 'commit': ''},  # 为空
    {'old': '123456', 'new': '180we', 'commit': '180we'},   # 少于6个字符 - 5位
    {'old': '123456', 'new': '456789342423443213423', 'commit': '456789342423443213423'},  # 多于20个字符 - 21个数字
    {'old': '123456', 'new': 'VANTHINKvanthinkstude', 'commit': 'VANTHINKvanthinkstude'},  # 多于20个字符 - 21个字母
    {'old': '123456', 'new': '456789sfsfwrzxcsad1sa', 'commit': '456789sfsfwrzxcsad1sa'},  # 多于20个字符 - 21个数字、字母组合
    {'old': '123456', 'new': 'q12a z.w@S勿x', 'commit': 'q12a z.w@S勿x'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
    {'old': '123qwe', 'new': '你好2018world', 'commit': '你好2018world'},   # 原密码验证不通过
    {'old': '123456', 'new': 'We2018', 'commit': 'We2018'},  # 6个字符 - 字母、数字
    {'old': 'We2018', 'new': '201801', 'commit': '201801'},  # 6个字符 - 数字
    {'old': '201801', 'new': 'VAnthi', 'commit': 'VAnthi'},  # 6个字符 - 大、小写字母
    {'old': 'VAnthi', 'new': 'VANTHINK201801VANTHK', 'commit': 'VANTHINK201801VANTHK'},  # 20个字符
    {'old': 'VANTHINK201801VANTHK', 'new': '123321', 'commit': '123321'},  # 中文、数字、英文字符组合
    {'old': '123321', 'new': '123456', 'commit': '123456'},  # 改回原来密码
)
