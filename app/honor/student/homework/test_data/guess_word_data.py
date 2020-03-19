#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

guess_word_dict = {'你好（首字母大写,自定义去除最后一个字母）': 'hello', '结束（自定义去除最后一个字母）': 'over',
                   '苹果（首字母大写,自定义去除最后一个字母）': 'apple', '喜欢（自定义去除最后一个字母）': 'like',
                   '但是（自定义去除最后一个字母）': 'but', '词组': 'like is',
                   'Mr': '男士', 'boy': '男孩', 'girl': '女孩', 'box': '盒子', 'crayon': '彩色蜡笔',
                   'great': '非常好的', 'horse': '马', 'ice cream': '冰淇淋'}


def guess_word_operate(key):
    """根据word找解释"""
    print('key:', key)
    if key in guess_word_dict.keys():
        value = guess_word_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        return 'abcdefgh'
