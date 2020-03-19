# coding=utf-8
import unittest

import time

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.user_center.test_data.nickname import nickname_data
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest
from utils.screen_shot import ScreenShot
from utils.toast_find import Toast


class ChangeNickName(unittest.TestCase):
    """修改昵称"""

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
        cls.screen_shot = ScreenShot()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ChangeNickName, self).run(result)


    @testcase
    def test_nickname(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user_center.wait_check_user_center_page():  # 页面检查点
                self.user_center.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作
                if self.user_info.wait_check_page():  # 页面检查点

                    for i in range(len(nickname_data)):
                        if self.user_info.wait_check_page():  # 页面检查点
                            name1 = self.user_info.nickname()  # 昵称条目

                            self.user_info.click_nickname()  # 点击昵称条目，进入设置页面
                            if self.home.wait_check_tips_page():
                                self.home.tips_title()
                                nick = self.user_info.input()  # 输入框
                                nick.send_keys(r'' + nickname_data[i]['nickname'])  # 输入昵称
                                print('修改为：', nick.text)

                                if i == len(nickname_data)-2:
                                    print('----------不保存修改----------')
                                    self.user_info.click_negative_button()  # 取消按钮

                                    if self.user_info.wait_check_page():
                                        name2 = self.user_info.nickname()  # 昵称条目
                                        if name2 == name1:
                                            print('cancel change nickname success')
                                        else:
                                            print('cancel change nickname failed')
                                else:
                                    if self.user_info.positive_button() == 'true':
                                        self.user_info.click_positive_button()  # 确定按钮

                                        if self.user_info.wait_check_page():  # 页面检查点
                                            if len(nickname_data[i]) == 2:
                                                # print('toast:', Toast().find_toast(nickname_data[i]['assert']))
                                                # todo 获取toast
                                                name2 = self.user_info.nickname()  # 昵称条目
                                                if name2 == name1:
                                                    print('not change nickname')
                                                else:
                                                    self.base_assert.except_error('❌❌❌ Error- nickname is changed' + nickname_data[i]['nickname'] +
                                                                                  ' ' + name2)
                                            else:
                                                time.sleep(2)
                                                name2 = self.user_info.nickname()  # 昵称条目
                                                if name2 == name1:
                                                    self.base_assert.except_error('❌❌❌ Error- failed change nickname'+  nickname_data[i][
                                                        'nickname'] + ' ' + name2)
                                        else:
                                            print('未返回个人信息页面')
                                    else:
                                        self.user_info.click_negative_button()  # 取消按钮

                                        if self.user_info.wait_check_page():  # 页面检查点
                                            name2 = self.user_info.nickname()  # 昵称条目
                                            if name2 == name1:
                                                print('not change nickname')
                                            else:
                                                self.base_assert.except_error('❌❌❌ Error- nickname is changed' +  nickname_data[i]['nickname'] + ' '+
                                                                              name2)
                                        else:
                                            print('未返回个人信息页面')
                        print('-----------------------------------')
                else:
                    print('未进入个人信息页面')
                self.user_info.back_up()  # 返回
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")
