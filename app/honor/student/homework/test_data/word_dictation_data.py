import random


# data base of study_word dictation
# we can add a or multiple expalin_word in it, like this '{'explain': 'xxxxxxxxxxx', 'study_word': 'yyyyyyyy'},'
dictation_dict = (
    {'explain': '你好（首字母大写，自定义去除最后一个字母）', 'study_word': 'Hello'},
    {'explain': '结束（自定义去除最后一个字母）', 'study_word': 'over'},
    {'explain': '苹果（首字母大写，自定义去除最后一个字母）', 'study_word': 'Apple'},
    {'explain': '喜欢（自定义去除最后一个字母）', 'study_word': 'like'},
    {'explain': '但是（自定义去除最后一个字母）', 'study_word': 'but'},
    {'explain': '一样的单词', 'study_word': 'aabbcd'},

)


def dictation_operate(i):
    """根据句子找word"""
    value = dictation_dict[i]['study_word']
    return value
