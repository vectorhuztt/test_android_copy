# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/14 14:24
# -------------------------------------------
import unittest

from app.honor.student.listen_everyday.object_page.level_page import LevelPage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststeps
from utils.assert_func import ExpectingTest


class SelectLevel(unittest.TestCase):
    """选择等级"""

    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.listen = ListenHomePage()
        cls.level = LevelPage()
        cls.login = LoginPage()
        cls.login.app_status()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(SelectLevel, self).run(result)

    @teststeps
    def test_select_level(self):
        if self.level.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            self.level.home.click_hk_tab(4)
            if self.listen.wait_check_listen_everyday_home_page():
                self.listen.level_button().click()
                if self.level.wait_check_listening_level_page():
                    self.level.level_page_ele_operate()

            if self.listen.wait_check_listen_everyday_home_page():
                self.level.click_back_up_button()




