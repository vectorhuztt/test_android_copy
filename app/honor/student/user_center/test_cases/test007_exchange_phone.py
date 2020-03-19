##!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.user_center.object_page.reset_phone_page import PhoneReset
from app.honor.student.user_center.test_data.reset_phone import reset_phone_data
from app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast


class ExchangePhone(unittest.TestCase):
    """更换手机号"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.user_center = UserCenterPage()
        cls.user_info = UserInfoPage()
        cls.phone = PhoneReset()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ExchangePhone, self).run(result)


    @testcase
    def test_exchange_phone(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user_center.wait_check_user_center_page():  # 页面检查点
                self.user_center.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

                for i in range(len(reset_phone_data)):
                    if self.user_info.wait_check_page():  # 页面检查点
                        phone1 = self.user_info.phone()  # 获取修改前手机号
                        self.user_info.click_phone_number()  # 点击手机号条目，进入设置页面
                        if self.home.wait_check_tips_page():
                            self.home.tips_title()
                            text = self.user_info.input()  # 验证之前密码
                            text.send_keys(reset_phone_data[0]['password'])
                            self.user_info.click_positive_button()  # 确定按钮

                            if self.phone.wait_check_page():  # 手机号 修改页面
                                phone = self.phone.et_phone()
                                phone.send_keys(reset_phone_data[i]['reset'])
                                print('修改为：', reset_phone_data[i]['reset'])

                                self.phone.count_time()  # 获取 验证码
                                if len(reset_phone_data[i]) == 3:
                                    if Toast().find_toast(reset_phone_data[i]["toast"]):
                                        print(reset_phone_data[i]["toast"])
                                    self.home.click_back_up_button()  # 返回个人信息 页面
                                else:
                                    value = verify_find(reset_phone_data[i]['reset'])  # 获取验证码
                                    if i == len(reset_phone_data)-1:
                                        self.phone.verify().send_keys('1234')
                                        self.phone.btn_certain()  # 确定按钮

                                        if Toast().find_toast('验证码验证失败'):
                                            print('验证码验证失败: 1234')

                                    self.phone.verify().send_keys(value)
                                    print('验证码:', value)
                                    self.phone.btn_certain()  # 确定按钮

                                    if self.user_info.wait_check_page():
                                        self.home.click_back_up_button()  # 数据更新需要刷新页面
                                        if self.user_center.wait_check_user_center_page():  # 页面检查点
                                            self.user_center.click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作
                                            if self.user_info.wait_check_page():
                                                phone2 = self.user_info.phone()  # 获取修改后的手机号
                                                if phone1 != phone2:
                                                    print('exchange phone success')
                                                else:
                                                    print('failed to exchange phone')
                            else:
                                print('未进入修改手机号页面')
                        else:
                            print('未进入 确认密码页面')
                    else:
                        print('未进入个人信息页面')
                    print('-'*30, '\n')
                self.user_info.back_up()
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")
