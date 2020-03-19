##!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.user_center.object_page.reset_password_page import PwdReset
from app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from app.honor.student.user_center.object_page.user_Info_page import UserCenterPage
from app.honor.student.user_center.test_data.reset_password import reset_pwd
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class ResetPwd(unittest.TestCase):
    """修改密码"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login_page = LoginPage()
        cls.home = HomePage()
        cls.user_center = UserCenterPage()
        cls.user_info = UserInfoPage()
        cls.pwd = PwdReset()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ResetPwd, self).run(result)

    @testcase
    def test_change_password(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user_center.wait_check_user_center_page():  # 页面检查点
                self.user_center.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                if self.user_info.wait_check_page():
                    self.user_info.click_password()  # 点击修改密码
                    if self.pwd.wait_check_page():  # 页面检查点
                        self.pwd.pwd_checkbox()  # 点击 显示密码

                        for i in range(len(reset_pwd)):
                            if self.pwd.wait_check_page():  # 页面检查点
                                old_pwd = self.pwd.pwd_origin()
                                old_pwd.send_keys(reset_pwd[i]['old'])

                                # 输入新的密码
                                new_pwd = self.pwd.pwd_new()
                                new_pwd.send_keys(r'' + reset_pwd[i]['new'])
                                print('修改密码为:', new_pwd.text)

                                # 再次输入密码
                                again_pwd = self.pwd.pwd_confirm()
                                again_pwd.send_keys(r'' + reset_pwd[i]['commit'])

                                self.pwd.confirm_button()  # 点击完成按钮
                                if self.user_info.wait_check_page():  # 页面检查点
                                    print('changed successfully')
                                    if i != len(reset_pwd)-1:
                                        self.user_info.click_password()  # 点击修改密码
                                        if self.pwd.wait_check_page():  # 页面检查点
                                            self.pwd.pwd_checkbox()  # 点击 显示密码
                                else:
                                    print('failed to change')
                                print('---------------------------------')
                else:
                    print('未进入个人信息页面')
                # self.user_info.back_up()
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")
