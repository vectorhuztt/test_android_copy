#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import os


class GetVariable(object):
    """参数化文档"""
    PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), p))  # 获取当前路径
    # 数据库信息
    # =====  dev ======

    # TEST_VERSION = 'dev'
    # HOST = '172.17.0.200'
    # USER_NAME = 'director'
    # PASSWORD = 'r0#pX8^V'
    # # DB = 'wordbook_rebuild'
    # DB = "b_vanthink_core"

    # ==== Test =====
    TEST_VERSION = 'test'
    HOST = '172.17.0.16'
    USER_NAME = 'tmp'
    PASSWORD = 'mysql#0056'
    DB = "b_vanthink_online"

    # 测试报告存放路径
    REPORT_ROOT = 'storges/test_report'

    # 以下为 devices.py 配置信息
    PACKAGE = 'student_env_devMasterDebug_1.4.8-5.apk'

    ID_TYPE = 'com.vanthink.student.debug:id/'
    # case统计 配置信息
    SUIT_PATH = 'app'
    CASE_INFO = [
        # ('app/honor/student/login/test_cases', 'test0*.py'),
        # ('app/honor/student/listen_everyday/test_cases', 'test0*.py'),
        # ('app/honor/student/user_center/test_cases', 'test*.py'),
        # ('app/honor/student/vanclass/test_cases', 'test0*.py'),
        # ('app/honor/student/library/test_cases', 'test002*.py'),
        # ('app/honor/student/test_paper/test_cases', 'test0*.py'),
        # ('app/honor/student/word_book_rebuild/test_cases', 'test011*.py'),
        # ('app/honor/student/word_book_rebuild/test_cases', 'test002*.py'),
        # ('app/honor/student/punch_activity/test_cases', 'test001*.py'),
        ('app/honor/student/homework_rebuild/test_cases', 'test001*.py'),
        # ('app/honor/student/homework_rebuild/test_cases', 'test002*.py')
            ]

    # CASE_PATH = 'app/student'
    # CASE_PATH = 'app/honor/student/login/test_cases'
    # CASE_PATH = 'app/honor/student/user_center/test_cases'
    # CASE_PATH = 'app/honor/student/vanclass/test_cases'
    # CASE_PATH = 'app/honor/student/listen_everyday/test_cases'
    # CASE_PATH = 'app/honor/student/library/test_cases'
    # CASE_PATH = 'app/honor/student/homework_rebuild/test_cases'
    # CASE_PATH = 'app/honor/student/test_paper/test_cases'
    # CASE_PATH = 'app/honor/student/word_book/test_cases'
    # CASE_PATH = 'app/honor/student/word_book_rebuild/test_cases'

    # 以下为 appium_server.py 配置信息
    SERVER_URL = 'http://127.0.0.1:%s/wd/hub/status'
    SERVER_LOG = 'appium_server_port_%s.log'
    KILL = 'taskkill /PID %d /F'

    # 做题情况统计 Excel表格存放路径
    EXCEL_PATH = 'storges/games_result_info.xlsx'

    # 学生的ID
    STU_ID = 0
    # 需要测试的单词熟练度
    LEVEL = 1
    # 需改动的时间数
    TIME_COUNT = 0
    # 年级
    GRADE = '四年级'
    # 试卷的索引
    EXAM_INDEX = -1