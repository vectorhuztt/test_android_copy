#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

form_sentence_dict = {'我有一个梦想。(自定义HAVE)': 'I HAVE a dream.', '我爱英语。（自定义English）': 'I love English.',
                      "我回来了。（自定义i'm）": "i'm home.", "有什么事吗?（自定义what's）": "what's up?",
                      "别担心。（自定义don't）": "don't worry."}


def form_sentence_operate(key):
    """根据句子找word"""
    print('key:', key)
    if key in form_sentence_dict.keys():
        value = form_sentence_dict[key]
        print('value:', value)
        return value
    else:   # 不在数据字典中的数据
        print('不在数据字典中的数据 ! !')
