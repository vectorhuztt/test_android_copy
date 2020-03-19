#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 9:15
# -----------------------------------------
import unittest

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.class_operate import QuitAddClass
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class NoClass(unittest.TestCase):
    """未加入班级"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.login.app_status()  # 判断APP当前状态
        BasePage().set_assert(cls.base_assert)

    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(NoClass, self).run(result)

    @testcase
    def test_no_class_word_data(self):
        """测试没有班级时候的"""
        if self.home.wait_check_home_page():
            QuitAddClass().quit_all_class_operate()
            stu_info = UserCenterPage().get_user_info()
            stu_id = stu_info[0]
            sys_trans_ids = WordDataHandlePage().get_sys_words_trans_id(stu_id)
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                    self.word_rebuild.word_start_button()  # 点击 Go按钮
                    word_info = FlashCard().scan_game_operate(is_exit=True)
                    WorldBookPublicPage().check_word_order_is_right(sys_trans_ids, word_info[0], sys_only=True)
                if self.word_rebuild.wait_check_continue_page():
                    self.word_rebuild.click_back_up_button()














