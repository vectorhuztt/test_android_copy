# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/21 10:38
# -------------------------------------------
import unittest

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.listen_everyday.object_page.rank_page import RankPage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststeps
from utils.assert_func import ExpectingTest


class Ranking(unittest.TestCase):
    """排行"""

    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.listen = ListenHomePage()
        cls.rank = RankPage()
        cls.login = LoginPage()
        cls.login.app_status()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(Ranking, self).run(result)

    @teststeps
    def test_rank(self):
        if self.rank.home.wait_check_home_page():  # 页面检查点
            name = UserCenterPage().get_user_info()[-1]
            if self.rank.home.wait_check_home_page():
                print('进入主界面')
                self.rank.home.click_hk_tab(4)   # 点击 每日一听
                if self.listen.wait_check_listen_everyday_home_page():
                    excise_time = self.listen.excise_time()
                    print('已练听力：', excise_time.text, '\n')
                    self.listen.rank_button().click()
                    if self.rank.wait_check_rank_page():
                        self.rank.rank_ele_operate(name)
                    if self.rank.wait_check_rank_page():
                        self.rank.click_back_up_button()
                    if self.listen.wait_check_listen_everyday_home_page():
                        self.listen.click_back_up_button()
                    if self.rank.home.wait_check_home_page():
                        print('返回主页面')

