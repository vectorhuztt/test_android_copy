#!/usr/bin/env python
# encoding:UTF-8
import unittest

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


class VanclassHw(unittest.TestCase):
    """本班作业 - 各tab信息"""

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
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(VanclassHw, self).run(result)

    @testcase
    def test_vanclass_homework_tab(self):
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

                    self.van.vanclass_hw()  # 进入 本班作业
                    if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                        print('%s 本班作业:' % gv.CLASS_NAME)
                        self.all_hw_operate()  # 全部 tab
                        self.incomplete_operate()  # 未完成 tab
                        self.complete_operate()  # 已完成 tab

                        self.home.click_back_up_button()
                        if self.van.wait_check_vanclass_page(gv.CLASS_NAME):  # 班级详情 页面检查点
                            self.home.click_back_up_button()
                            if self.van.wait_check_page():  # 班级 页面检查点
                                self.home.click_tab_hw()  # 返回主界面
                    else:
                        print('未进入 本班作业页面')
                        self.home.click_back_up_button()
                        if self.van.wait_check_page():  # 班级 页面检查点
                            self.home.click_tab_hw()  # 返回主界面
        else:
            try:
                Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            except Exception:
                print("未进入主界面")
                raise

    @teststeps
    def all_hw_operate(self):
        """全部tab 具体操作"""
        all_hw = self.detail.all_tab()  # 全部 tab
        if self.detail.selected(all_hw) is False:
            self.base_assert.except_error('Error- 未默认在 全部页面')
        else:
            print('-------------------全部tab-------------------')
            if self.van.empty_tips():
                print('暂无数据')
            else:
                self.hw_list_operate()

    @teststeps
    def incomplete_operate(self):
        """未完成tab 具体操作"""
        incomplete = self.detail.unfinished_tab()  # 未完成 tab
        if self.detail.selected(incomplete) is True:
            self.base_assert.except_error('Error- 默认在 未完成 tab页')
        else:
            incomplete.click()  # 进入 未完成 tab页
            if self.detail.selected(incomplete) is False:
                self.base_assert.except_error('Error- 未进入 未完成 tab页')
            else:
                print('-------------------未完成tab-------------------')
                if self.van.empty_tips():
                    print('暂无数据')
                else:
                    self.hw_list_operate()

    @teststeps
    def complete_operate(self):
        """已完成tab 具体操作"""
        complete = self.detail.finished_tab()  # 已完成 tab
        if self.detail.selected(complete) is True:
            self.base_assert.except_error('Error- 默认在 已完成 tab页')
        else:
            complete.click()  # 进入 已完成 tab页
            if self.detail.selected(complete) is False:
                self.base_assert.except_error('Error- 未进入 已完成 tab页')
            else:
                print('-------------------已完成tab-------------------')
                if self.van.empty_tips():
                    print('暂无数据')
                else:
                    self.hw_list_operate()

    @teststeps
    def hw_list_operate(self):
        """作业列表 具体操作"""
        homework_name = []
        while True:  # 如果list多于一页
            finish = self.detail.finish_status()  # 已经有x人完成
            hw_name = self.detail.hw_name()
            for i, x in enumerate(finish):
                if hw_name[i].text in homework_name:
                    continue
                else:
                    print(hw_name[i].text, x.text)
                    homework_name.append(hw_name[i].text)
                print('-'*30, '\n')

            if self.detail.wait_check_end_tips_page():
                break
            else:
                self.home.screen_swipe_up(0.5, 0.8, 0.2, 1000)
