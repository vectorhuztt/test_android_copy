#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI

from conf.base_config import GetVariable as gv

# 学生名字由2~20位中文、英文组成
name_data = (
    {'name': '', 'count': '0', 'assert': '姓名不能为空'},  # 为空
    {'name': ' ', 'count': '1', 'assert': '名字由2-20位中文、英文组成'},  # 1个字符
    {'name': '万', 'count': '1', 'assert': '名字由2-20位中文、英文组成'},  # 1个字符
    {'name': '万w', 'count': '2'},  # 2个字符
    {'name': 'DE', 'count': '2'},  # 2个字符  区分大小写
    {'name': 'de', 'count': '2'},  # 2个字符  区分大小写
    {'name': 'van在线教育12', 'count': '10'},
    {'name': 'v@在线$123', 'count': '8', 'assert': '名字由2-20位中文、英文组成'},  # 8个字符 特殊字符
    {'name': '以VA2Nthink数字studeVANr', 'count': '21', 'assert': '名字由2-20位中文、英文组成'},   # 多于20个字符 - 21个
    {'name': 'V8AN7K4v     nkstu在线', 'count': '20'},   # 20个字符  5个连续空格
    {'name': 'q18 az12xQ ZS XE19在育', 'count': '20'},  # 20个字符  空格
)

class_data_dev = [
    {'class': ''},
    {'class': '123', 'assert': '班号为4-9位，请重新确认'},
    {'class': '74578'},   # 班级不存在
    {'class': '9820', 'assert': '该班级已申请'},
    {'class': '654644'},  # 班级不存在
    {'class': '123456789'},  # 班级不存在
    {'class': '1234567890', 'assert': '班号为4-9位，请重新确认'},
    {'class': '9420'}   # 班级正确
]


class_data_test = [
    {'class': ''},
    {'class': '123', 'assert': '班号为4-9位，请重新确认'},
    {'class': '74578'},   # 班级不存在
    {'class': '50497', 'assert': '该班级已申请'},
    {'class': '654644'},  # 班级不存在
    {'class': '1234567890', 'assert': '班号为4-9位，请重新确认'},
    {'class': '47215'}   # 班级正确
]

class_data = class_data_test if gv.TEST_VERSION == 'test' else class_data_dev