#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI

# 手机号：11位手机号
# 昵称：由2~20位中文、数字及英文组成，数字不能做首位；可以允许有字符【.】【@】【空格】
# 密码：6-20位非空字符；只允许设置数字、英文字母（英文字母区分大小写）
import random
phone_data = [{'account': '18022' + str(x) + str(random.randint(1000, 9999))} for x in range(10, 25)]


pwd_data = [
    {'nick': 'sffq12a z.w@S万x', 'password': '', 'confirm': ''},   # 0字符
    {'nick': 'sffq12a z.w@S万x', 'password': '        ', 'confirm': '        '},    # 空格 8字符
    {'nick': 'sffq12a z.w@S万x', 'password': 'qwe23', 'confirm': 'qwe23', 'assert': '密码 格式不正确'},  # 5字符
    {'nick': 'sffq12a z.w@S万x', 'password': 'ab45678912345cDE67890', 'confirm': 'ab45678912345cDE67890', 'assert': '密码 格式不正确'},  # 21字符
    {'nick': 'sffq12a z.w@S万x', 'password': 'Ab123#$/345cde89', 'confirm': 'Ab123#$/345cde89', 'assert': '密码 格式不正确'},
    {'nick': 'sffq12a z.w@S万x', 'password': '1we456', 'confirm': '1wE789', 'assert': '密码 输入不一致'},
    {'nick': 'sffq12a z.w@S万x', 'password': '456789', 'confirm': '456789'},
    {'nick': 'sffq12a z.w@S万x', 'password': 'QWe123', 'confirm': 'QWe123'},  # 中文、数字、英文字母组合 6字符
    {'nick': 'sffq12a z.w@S万x', 'password': 'wanxingzaixianjiaoyu', 'confirm': 'wanxingzaixianjiaoyu'},  # 英文字母 20字符
    {'nick': 'sffq12a z.w@S万x', 'password': '123zXc6', 'confirm': '123zXc6'},  # 数字、英文字母组合 7字符

]

nick_data = [
    {'nick': '', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 0个字符
    {'nick': '  ', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 2个字符
    {'nick': '          ', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 10个字符
    {'nick': '万', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 1个字符
    {'nick': 'VA7INK4van万星ink8stude', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 21个字符
    {'nick': '180qa万wsx', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 数字为首位
    {'nick': 'q#*a星w180sx', 'password': '456789', 'confirm': '456789', 'assert': '2-20位中文、数字、英文及【空格】【.】【@】组成，不能首数字'},  # 其他特殊字符

    {'nick': 'We', 'password': '456789', 'confirm': '456789'},  # 2个字符
    {'nick': '. @', 'password': '456789', 'confirm': '456789'},  # @、'.'字符组合 2个字符
    {'nick': 'VANTHINKVANTHINKVANT', 'password': '456789', 'confirm': '456789'},  # 英文大写  20个字符
    {'nick': 'vanthinkvanthink', 'password': '456789', 'confirm': '456789'},  # 英文小写  20个字符
    {'nick': '你好万星在线教育平台学生端', 'password': '456789', 'confirm': '456789'},  # 中文
    {'nick': '你好2018VANworld', 'password': '456789', 'confirm': '456789'},  # 中文、数字、英文字母组合
    {'nick': 'q12a z.w@S万x', 'password': '456789', 'confirm': '456789'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合

    {'nick': 'sffq12a z.w@S万x', 'password': '456789', 'confirm': '456789'},
]
