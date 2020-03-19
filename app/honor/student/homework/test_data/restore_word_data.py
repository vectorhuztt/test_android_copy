#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

restore_word_dict = {'你好（首字母大写,自定义去除最后一个字母）': 'Hello', '结束（自定义去除最后一个字母）': 'over',
                     '苹果（首字母大写,自定义去除最后一个字母）': 'Apple', '喜欢（自定义去除最后一个字母）': 'like',
                     '但是（自定义去除最后一个字母）': 'but', '一样的单词': 'aa',
                     '喷泉': 'fountain', '见面': 'meet', '杂志': 'magazine', '台阶': 'stair', '在......旁边': 'beside ',
                     '观光': 'sightseeing', '围巾': 'scarf', '加拿大': 'Canada', '鲸鱼': 'whale', '旅行': 'cruise'}


def restore_word_operate(key):
    """根据word找解释"""
    print('key:', key)
    if key in restore_word_dict.keys():
        value = restore_word_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        return 'abc'
