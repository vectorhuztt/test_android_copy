#!/usr/bin/env python
# encoding:UTF-8
import time
import unittest

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast


class QuitVanclass(unittest.TestCase):
    """退出班级"""

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
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(QuitVanclass, self).run(result)

    @testcase
    def test_quit_vanclass(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_test_vanclass()  # 班级tab
            if self.van.wait_check_page():  # 页面检查点

                van = self.van.vanclass_name()  # 班级名称
                for i in range(len(van)):
                    if van[i].text == gv.DEL_VANCLASS:
                        van[i].click()  # 进入班级详情页
                        break
                self.quit_tips_operate()  # 退出班级提示框

                if self.van.wait_check_page():  # 班级 页面检查点
                    if self.van.wait_check_quit_vanclass(gv.DEL_VANCLASS):
                        self.base_assert.except_error('Error-- 班级未退出')
                    else:
                        print('班级退出成功')
                    self.home.click_tab_hw()  # 返回主界面
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def quit_tips_operate(self):
        """退出班级 具体操作"""
        if self.van.wait_check_vanclass_page(gv.DEL_VANCLASS):  # 页面检查点
            self.van.quit_vanclass()  # 退出班级 按钮
            self.home.tips_operate_cancel()  # 提示框
            print('取消 退出')
            print('------------------------------')

            if self.van.wait_check_vanclass_page(gv.DEL_VANCLASS):  # 页面检查点
                self.van.quit_vanclass()  # 退出班级 按钮
                self.home.tips_operate_commit()  # 提示框
                print('确定 退出')
                time.sleep(3)
                print('------------------------------')

            print('wait_check_quit_page:', self.van.wait_check_quit_page())
            if self.van.wait_check_quit_page():
                self.van.phone_name()  # 提示
                value = verify_find(gv.PHONE, 'quitClass')  # 获取验证码
                self.van.code_input().send_keys(value)  # 输入验证码
                print(gv.PHONE)
                print('验证码:', value)
                self.van.quit_button()  # 退出班级 按钮
