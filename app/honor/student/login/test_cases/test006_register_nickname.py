# coding=utf-8
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.register_data import phone_data, nick_data
from app.honor.student.punch_activity.object_page.punch_page import PunchActivityPage
from app.honor.student.user_center.object_page.user_center_page import Setting
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast


class Register(unittest.TestCase):
    """注册 - 昵称"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.set = Setting()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(Register, self).run(result)

    @testcase
    def test_register_nickname(self):
        # 判断APP当前状态
        PunchActivityPage().close_home_activity_tip()
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
        
        self.register_operate()  # 具体操作

    @teststeps
    def register_operate(self):
        """ 注册 具体操作"""
        index = 0
        if self.login.wait_check_login_page():
            for i in range(len(phone_data)):
                if index == len(nick_data) - 1:
                    break

                if self.login.wait_check_login_page():
                    self.login.register_button()  # 注册帐号 按钮
                    if self.login.wait_check_register_page():
                        phone = self.login.input_phone()
                        phone.click()  # 激活phone输入框
                        user_phone = phone_data[i]['account']
                        phone.send_keys(user_phone)  # 输入手机号

                        self.login.get_code_button().click()   # 获取验证码 按钮
                        value = verify_find(user_phone, 'register')  # 获取验证码

                        if Toast().find_toast('用户已经注册') or self.login.wait_check_login_page():
                            print('用户已经注册', user_phone)
                            continue
                        else:
                            self.login.send_code_operate(value)
                            if self.login.wait_check_register_nick_page():
                                print('账号:', phone_data[i]['account'])
                                print(value)
                                print('-----------------')

                                pwd = self.login.new_pwd()  # 设置密码
                                confirm = self.login.new_pwd_confirm()  # 密码再次确认

                                pwd.send_keys(nick_data[-1]['password'])  # 输入密码
                                print('密码:', nick_data[-1]['password'])

                                confirm.send_keys(nick_data[-1]['confirm'])  # 密码确认
                                print('密码确认:', nick_data[-1]['confirm'])

                                for j in range(len(nick_data)):
                                    if self.login.wait_check_register_nick_page():
                                        nickname = self.login.input_nickname()
                                        nickname.clear()
                                        nickname.send_keys(nick_data[index]['nick'])  # 输入昵称
                                        print('昵称:', nick_data[index]['nick'])

                                        self.login.register_button()  # 注册 按钮
                                        index = index + 1
                                        if len(nick_data[index]) == 4:
                                            if Toast().find_toast(nick_data[index]['assert']):
                                                print(nick_data[index]['assert'])
                                            print('❌❌❌ Error -注册失败')
                                            print('-' * 30, '\n')
                                        else:
                                            if self.login.wait_check_login_page():
                                                print('注册成功,请登录')
                                                print('-' * 30, '\n')
                                                break
                                            else:
                                                print('停留在注册页面')
                                                print('-' * 30, '\n')




                                # break
