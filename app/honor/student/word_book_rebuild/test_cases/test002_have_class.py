#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 8:50
# -----------------------------------------
import unittest

from ddt import ddt, data

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.web.object_pages.assign_word import AssignWord
from app.honor.web.object_pages.driver import Driver
from app.honor.student.word_book_rebuild.object_page.class_operate import QuitAddClass
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from app.honor.student.word_book_rebuild.test_data.account import *
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class HaveClass(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.login.app_status()   # 判断APP当前状态
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(HaveClass, self).run(result)

    @data(
        ['10411'],
        # ['10411', '10413']
    )
    @testcase
    def test_have_class(self, test_class_num):
        """测试有老师的情况， 一个班或者多个班的情况"""
        if self.home.wait_check_home_page():
            van_num = test_class_num.copy()
            QuitAddClass().apply_class_operate(van_num)
            web_driver = Driver()
            web_driver.set_driver()
            AssignWord().assign_wordbook_operate(test_class_num, TEACHER_ACCOUNT[0], STU_PASSWORD)
            web_driver.quit_web()
            if self.home.wait_check_home_page():
                stu_info = UserCenterPage().get_user_info()
                stu_id = stu_info[0]
                teacher_trans_ids = WordDataHandlePage().get_teacher_words_trans_id(stu_id)
                if self.home.wait_check_home_page():
                    self.home.click_hk_tab(1)  # 点击 背单词
                    if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                        self.word_rebuild.word_start_button()  # 点击 Go按钮
                        word_info = FlashCard().scan_game_operate(is_exit=True)
                        WorldBookPublicPage().check_word_order_is_right(teacher_trans_ids, word_info[0])
                    if self.word_rebuild.wait_check_continue_page():
                        self.word_rebuild.click_back_up_button()

