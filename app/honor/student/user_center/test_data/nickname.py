#!/usr/bin/env python
# encoding:UTF-8

# 昵称：由2~20位中文、数字及英文组成，数字不能做首位；可以允许有字符【.】【@】【空格】
nickname_data = (
    {'nickname': ''},  # 为空
    {'nickname': 'VANTHINKvanthinkstude'},   # 多于20个字符 - 21个
    {'nickname': 'VANTH7INK4vanthink8stude'},   # 多于20个字符 - 24个

    {'nickname': '180qazwsx', 'assert': '昵称不能以数字开头'},  # 数字为首位
    {'nickname': '4212345678909876543', 'assert': '昵称不能以数字开头'},  # 数字  19个字符
    {'nickname': 'q#*azw180sx', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 其他特殊字符
    {'nickname': '  ', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 两个空格
    {'nickname': '          ', 'assert': '昵称由2~20位中文，数字，英文组成'},  # 多个空格 -10个
    {'nickname': 'q', 'assert': '昵称由2~20位中文，数字，英文组成'},   # 少于2个字符 - 1个

    {'nickname': 'We'},    # 2个字符
    {'nickname': '.@'},    # 2个字符
    {'nickname': 'VANTHINKVANTHINKVANT'},   # 20个字符 -大写字母
    {'nickname': 'vanthinkvanthink'},   # 纯小写字母 - 16个
    {'nickname': '你好万星在线教育平台学生端'},  # 纯中文 -13个
    {'nickname': '你好2018world'},  # 中文、数字、英文字符组合
    {'nickname': 'q12A z.w@S勿x'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
    {'nickname': 'sff'},  # 改回原来昵称
)

