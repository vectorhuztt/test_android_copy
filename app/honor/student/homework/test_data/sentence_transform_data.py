#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

sentence_transform_dict = {'I have a dream.（将原句改为否定句）': 'I have not a dream.',
                           'I have not a dream.（将原句改为肯定句）': 'I have a dream.'}


def sentence_transform_operate(key):
    """根据word找解释"""
    print('key:', key)
    if key in sentence_transform_dict.keys():
        value = sentence_transform_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        print('不在数据字典中的数据 ! !')
