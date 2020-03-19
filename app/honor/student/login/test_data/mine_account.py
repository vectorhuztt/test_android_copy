#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

# 11位手机号  dev
phone_data = [
    {'username': '18011111897', 'password': '456789', 'assert': '手机号未注册，请先注册'},  # 未注册手机号
    {'username': '81011111112', 'password': '456789'},  # 11位数字 - 非手机号
    {'username': '132345', 'password': '456789'},  # 少于11个数字  是否报错
    {'username': '', 'password': '456789'},  # 手机号为空
    {'username': '           ', 'password': '456789'},  # 11个空格
    {'username': '130你好8world', 'password': '456789'},  # 中文、数字、英文字符组合 -11位
    {'username': '180q2.w@S勿x', 'password': '456789'},  # 中文、数字、英文、大写字母、空格、@、'.'字符组合
    {'username': '15612341234', 'password': '123456'},  # 基础版学生
    {'username': '17711110000', 'password': '123456'},  # 已注册有老师身份又有学生身份
    ]

# 6-20位非空字符；只允许设置数字、英文字母（英文字母区分大小写）
pwd_data = [
    {'username': '17711110000', 'password': ''},   # 为空
    {'username': '17711110000', 'password': '      '},   # 6个空格
    {'username': '17711110000', 'password': '123ewr78', 'assert': '手机号或密码错误'},  # 数字 字母组合 区分大小写 正确密码为：123eWr78
    {'username': '17711110000', 'password': '3$#3r@#7r', 'assert': '手机号或密码错误'},  # 输入特殊字符
    {'username': '17711110000', 'password': '12as', 'assert': '手机号或密码错误'},   # 少于6位 数字、字母组合
    {'username': '17711110000', 'password': '456789sfsfwrzxcsad123sa', 'assert': '手机号或密码错误'},   # 多于20位 数字、字母组合
    {'username': '', 'password': ''},  # 手机号和密码均不输入
    {'username': '17711110000', 'password': '123456'},  # 正确密码 数字 6位
    ]
