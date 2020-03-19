#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.single_choice_page import SingleChoice
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class HwAnalysis(unittest.TestCase):
    """本班作业 - 全部tab 作业详情"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        cls.homework = Homework()
        cls.game = SingleChoice()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(HwAnalysis, self).run(result)

    @testcase
    def test_homework_analysis_all(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_test_vanclass()  # 班级tab
            if self.van.wait_check_page():  # 页面检查点

                van = self.van.vanclass_name()  # 班级名称
                for i in range(len(van)):
                    if van[i].text == gv.CLASS_NAME:
                        van[i].click()  # 进入班级详情页
                        break
                if self.van.wait_check_vanclass_page(gv.CLASS_NAME):  # 页面检查点

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                        print('%s 本班作业:' % gv.CLASS_NAME)
                        if self.van.empty_tips():
                            print('暂无数据')
                        else:
                            all_hw = self.detail.all_tab()  # 全部 tab
                            if self.detail.selected(all_hw) is False:
                                self.base_assert.except_error('❌❌❌ Error- 未默认在 全部页面')
                            else:
                                print('--------------全部tab-------------------')
                                if self.van.empty_tips():
                                    print('暂无数据')
                                else:
                                    self.hw_operate()  # 具体操作
                                if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                                    self.home.click_back_up_button()  # 返回 本班作业
                                    if self.van.wait_check_quit_vanclass(gv.CLASS_NAME):
                                        self.home.click_back_up_button()
                                    if self.van.wait_check_page():
                                        self.home.click_tab_hw()
                                else:
                                    print('未返回 本班作业页面')
                    else:
                        print('未进入班级 -本班作业tab')
                        self.van.click_back_up_button()
                        if self.van.wait_check_page():  # 班级 页面检查点
                            self.home.click_tab_hw()  # 返回主界面
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def hw_operate(self):
        """作业列表"""
        name = self.detail.hw_name()  # 作业name
        for i in range(len(name)):
            if name[i].text == gv.HW_ANALY_GAME:
                name[i].click()  # 进入作业
                break

        if self.detail.wait_check_page(gv.HW_ANALY_GAME):  # 页面检查点
            # todo 获取toast 无需答题报告  or
            self.answer_detail()
        else:
            print('未进入作业 %s 页面' % gv.HW_ANALY_GAME)
            self.home.click_back_up_button()

    @teststeps
    def answer_detail(self):
        """答题情况详情页"""
        mode = self.homework.games_type()  # 游戏类型
        name = self.homework.games_title()  # 游戏name
        status = self.homework.status()  # 题目状态
        count = self.homework.count()  # 共X题
        for x in range(len(mode)):
            if x > 6:
                break
            else:
                print('作业名称：', name[x].text)
                print('模式：', mode[x].text)
                print('题目个数：', count[x].text)
                print('题目进度：', status[x].text, '\n')
        mode_content = mode[0].text
        name[0].click()
        if not self.detail.wait_check_page(mode_content):
            self.base_assert.except_error('点击大题未进入相应大题页面')
        else:
            self.home.click_back_up_button()
            self.home.tips_operate_commit()
            if self.detail.wait_check_page(gv.HW_ANALY_GAME):
                self.home.click_back_up_button()
            else:
                self.base_assert.except_error('从大题做题过程中退出未退回大题列表页面')



