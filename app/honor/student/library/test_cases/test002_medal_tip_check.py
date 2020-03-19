#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/30 16:37
# -----------------------------------------
import unittest

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.library.object_page.library_page import LibraryPage
from app.honor.student.library.object_page.medal_page import MedalPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.get_attribute import GetAttribute


class Medal(unittest.TestCase):
    """勋章测试"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login_page = LoginPage()
        cls.login = LoginPage()
        cls.medal = MedalPage()
        cls.library = LibraryPage()
        BasePage().set_assert(cls.base_assert)
        cls.login.app_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(Medal, self).run(result)

    @testcase
    def test_medal_tip(self):
        """测试勋章弹框"""
        if self.home.wait_check_home_page():
            self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
            self.home.check_more()[1].click()
            if self.library.wait_check_test_label_page('我的阅读'):
                self.medal.medal_icon().click()
                if self.medal.wait_check_medal_page():
                    medals = self.medal.medals()
                    for x in medals:
                        if self.medal.wait_check_medal_page():
                            if GetAttribute().get_selected(x) == 'false':
                                x.click()
                                if not self.medal.wait_check_medal_img_page():
                                    self.base_assert.except_error('点击置灰勋章未发现弹框')
                                else:
                                    print(self.medal.medal_content(), '\n')
                                    self.home.click_blank()
                            else:
                                x.click()
                                if not GameCommonEle().wait_check_punch_share_page():
                                    self.base_assert.except_error('点亮勋章点击后未进入分享页面')
                                else:
                                    GameCommonEle().share_page_operate()
                    if self.medal.wait_check_medal_page():
                        self.medal.click_back_up_button()
                    if LibraryPage().wait_check_test_label_page('我的阅读'):
                        self.medal.click_back_up_button()
                    if self.home.wait_check_home_page():
                        print('返回主页面')




