#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

match_dict = {'Hello': '你好（首字母大写,自定义去除最后一个字母）', 'over': '结束（自定义去除最后一个字母）',
              'Apple': '苹果（首字母大写,自定义去除最后一个字母）', 'like': '喜欢（自定义去除最后一个字母）',
              'like is': '词组', 'but': '但是（自定义去除最后一个字母）',
              'Ms': '女士', 'Mr': '男士', 'boy': '男孩', 'girl': '女孩', 'box': '盒子', 'crayon': '彩色蜡笔',
              'great': '非常好的', 'horse': '马', 'ice cream': '冰淇淋'}


def match_operate(key):
    """根据word找解释"""
    print('key:', key)
    if key in match_dict.keys():
        value = match_dict[key]
        print('value:', value)
        return value
    else:
        return 'abc'
    # Todo不在数据字典中的数据
