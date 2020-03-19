#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/8 11:42
# -----------------------------------------
import unittest

from app.honor.student.homework.object_page.wk_game_page import WKGamePage
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class WKGame(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.wk = WKGamePage()
        cls.login_page = LoginPage()
        cls.library = LibraryGamePage()
        BasePage().set_assert(cls.base_assert)
        cls.login_page.app_status()  # 判断APP当前状态


    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(WKGame, self).run(result)


    @testcase
    def test_wk_game(self):
        """测试微课"""
        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_hk_tab(2)  # 进入习题
            self.library.enter_into_game('微课测试', '微课')  # 获取大题元素与名称
            bank_list = self.library.bank_name_by_type('微课')  # 获取对应类型的大题个数
            bank_name = bank_list[0].text
            bank_list[0].click()
            self.wk.wk_game_operate()
            if self.library.wait_check_game_list_page('微课测试'):
                self.library.click_back_up_button()
                if self.library.wait_check_bank_list_page():
                    if self.library.bank_progress_by_name(bank_name) != '100%':
                        self.base_assert.except_error('微课退出后，题目进度不为100%')

                    self.library.click_back_up_button()
                    if self.library.wait_check_homework_list_page():
                        self.library.click_back_up_button()
