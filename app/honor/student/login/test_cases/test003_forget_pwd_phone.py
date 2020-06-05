# coding=utf-8
import time
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.forget_pwd_data import phone_data, pwd_data
from app.honor.student.punch_activity.object_page.punch_page import PunchActivityPage
from app.honor.student.user_center.object_page.user_center_page import Setting
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast


class LoginForgetPhone(unittest.TestCase):
    """忘记密码 -手机号"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.punch = PunchActivityPage()
        cls.set = Setting()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(LoginForgetPhone, self).run(result)

    @testcase
    def test_forget_pwd(self):
        # 判断APP当前状态
        self.punch.close_home_activity_tip()
        if self.home.wait_check_home_page():  # 在主界面
            print('已登录')
            self.set.logout_operate()  # 退出登录
        elif self.login.wait_check_login_page():  # 在登录界面
            print('在登录界面')
        else:
            print('在其他页面')
            self.login.close_app()  # 关闭APP
            self.login.launch_app()  # 重启APP
            if self.home.wait_check_home_page():  # 在主界面
                print('已登录')
                self.set.logout_operate()  # 退出登录
            elif self.login.wait_check_login_page():  # 在登录界面
                print('在登录界面')
        
        self.forget_pwd_operate()  # 具体操作

    @teststeps
    def forget_pwd_operate(self):
        """ 忘记密码 具体操作"""
        if self.login.wait_check_login_page():
            self.login.forget_password()  # 忘记密码按钮
            if self.login.wait_check_forget_page():
                for i in range(len(phone_data)):
                    print('---------------------------')
                    phone = self.login.input_phone()
                    phone.send_keys(phone_data[i]['account'])  # 输入手机号
                    print('账号:', phone_data[i]['account'])

                    self.login.get_code_button().click()  # 点击 获取验证码 按钮
                    if self.login.wait_check_forget_page():
                        if len(phone_data[i]) == 2:
                            if Toast().find_toast(phone_data[i]['toast']):
                                print(phone_data[i]['toast'])
                        else:
                            if i == 0:
                                value = self.login.verification_code_operate(phone_data[-1]['account'], 'resetPassword')  # 获取验证码
                            else:
                                value = verify_find(phone_data[i]['account'], 'resetPassword')  # 获取验证码

                            self.login.send_code_operate(value)
                            if self.login.wait_check_reset_page():
                                pwd = self.login.new_pwd()  # 设置密码
                                confirm = self.login.new_pwd_confirm()  # 密码再次确认

                                pwd.send_keys(pwd_data[-1]['password'])  # 输入密码
                                print('新密码:', pwd_data[-1]['password'])

                                confirm.send_keys(pwd_data[-1]['confirm'])  # 再次输入密码
                                print('新密码确认:', pwd_data[-1]['confirm'])

                                self.login.reset_button()  # 重置 按钮
                                print('--------------------')
                                if Toast().find_toast('修改成功,请登录'):
                                    print('修改成功,请登录')
                                else:
                                    print('❌❌❌ Error -修改失败')


