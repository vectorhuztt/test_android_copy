# !/usr/bin/env python
# encoding:UTF-8
from conf.decorator import teststeps

noyb_dict_yb = {'a': '/A/', 'b': '/B/', 'c': '/C/', 'd': '/D/', 'e': '/E/', 'f': '/F/', 'g': '/G/', 'h': '/H/',
             'i': '/I/', 'o': '/O/', 's': '/S/', 'v': '/V/', 'w': '/W/', 'x': '/X/', 'y': '/Y/', 'z': '/Z/',
             'ew': '/?/'}

noyb_dict_word = {'/A/': 'a', '/B/': 'b', '/C/': 'c', '/D/': 'd', '/E/': 'e', '/F/': 'f', '/G/': 'g', '/H/': 'h',
             '/I/': 'i', '/O/': 'o', '/S/': 's', '/V/': 'v', '/W/': 'w', '/X/': 'x', '/Y/': 'y', '/Z/': 'z',
             '/?/': 'ew'}


yb_dict_yb = {'a': '/ɑ/', 'b': '/ɜ/', 'c': '/ɔ/', 'd': '/ð/', 'e': '/ə/', 'f': '/ɒ/', 'g': '/g/', 'h': '/ʊ/',
             'i': '/ɪ/', 'o': '/θ/', 's': '/ʃ/', 'v': '/ʌ/', 'w': '/ʒ/', 'x': '/ɛ/', 'y': '/ŋ/', 'z': '/æ/',
             'ew': '/ˈ/'}


yb_dict_word = {'/ɑ/': 'a', '/ɜ/': 'b', '/ɔ/': 'c', '/ð/': 'd', '/ə/': 'e', '/ɒ/': 'f', '/g/': 'g', '/ʊ/': 'h',
             '/ɪ/': 'i', '/θ/': 'o', '/ʃ/': 's', '/ʌ/': 'v', '/ʒ/': 'w', '/ɛ/': 'x', '/ŋ/': 'y', '/æ/': 'z',
             '/ˈ/': 'ew'}


@teststeps
def no_yb_operate_yb(key):
    """不设置yb字体-根据word找yb"""
    if key.lower() in noyb_dict_yb.keys():
        print('key:', key)
        value = noyb_dict_yb[key.lower()]
        print('value:', value)
        return value


@teststeps
def no_yb_operate_word(key):
    """不设置yb字体-根据yb找word"""
    if key in noyb_dict_word.keys():
        print('key:', key)
        value = noyb_dict_word[key]
        print('value:', value)
        return value


@teststeps
def yb_operate_yb(key):
    """yb字体-根据word找yb"""
    if key.lower() in yb_dict_yb.keys():
        print('key:', key)
        value = yb_dict_yb[key.lower()]
        print('value:', value)
        return value


@teststeps
def yb_operate_word(key):
    """yb字体-根据yb找word"""
    if key in yb_dict_word.keys():
        print('key:', key)
        value = yb_dict_word[key]
        print(("value:", value))
        return value

