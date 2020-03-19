# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/27 11:59
# -------------------------------------------
import re
import time
import unittest
from ddt import ddt,data

from app.honor.student.homework_rebuild.object_pages.homework_game_page import HomeworkGameOperate
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.library.object_page.library_page import LibraryPage
from app.honor.student.library.object_page.game_result_page import ResultPage
from app.honor.student.library.object_page.library_data_handle import DataHandlePage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, teststeps
from utils.assert_func import ExpectingTest


@ddt
class BookGame(unittest.TestCase):
    """准确率"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.library = LibraryPage()
        BasePage().set_assert(cls.base_assert)
        cls.login.app_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(BookGame, self).run(result)

    @data(*[
            '单词',
            # '句子',
            # '文章',
           ])
    @teststeps
    def test_book_operate(self, book_name):
        """测试书籍游戏"""
        if self.home.wait_check_home_page():
            user_info = UserCenterPage().get_user_info()
            school_name = user_info[1]
            nickname = user_info[3]
            stu_id = user_info[0]

            if self.home.wait_check_home_page():
                self.home.screen_swipe_up(0.5, 0.9, 0.2, 1000)
                self.home.check_more()[0].click()
                label_name = '其他教材'

                # 进入其他教材标签，选择全题型书籍
                while True:
                    if self.library.wait_check_test_label_page(label_name):
                        self.library.course_more_btn(label_name).click()
                        break
                    else:
                        self.home.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                while not self.library.wait_check_test_book_page('全题型'):
                    self.home.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                self.library.test_book('全题型').click()

                #  进入书籍，获取书单进度，从数据库中查询此书籍的任一书籍是否已经学习过
                book_process, book_description = self.library.select_test_book_operate(book_name)
                print('书单数据库进度， 书籍描述：', book_process, book_description)
                today_has_studied = DataHandlePage().student_today_is_submit_bank_record(stu_id, '全题型', book_description)
                book_process = book_process if book_process != '完成' else '100%'

                # 书单操作，验证书单页面的排行、点赞、立即打卡功能
                book_set_info = self.library.bookset_page_operate(book_process, nickname, today_has_studied)
                bank_count = book_set_info[-1]
                if self.library.wait_check_book_set_page():
                    self.library.start_study_button().click()
                self.game_operate(bank_count, nickname)
                # 从书籍列表页面返回主页面操作
                self.library.from_bank_back_to_home_operate(school_name)


    @teststeps
    def game_operate(self, bank_count, nickname):
        if self.library.wait_check_bank_list_page():
            # 进入书籍， 遍历进入题型做题
            bank_name_list = []
            while len(bank_name_list) < bank_count:
                bank_name_eles = self.library.bank_name()
                for i, bank_ele in enumerate(bank_name_eles):
                    if self.library.wait_check_bank_list_page():
                        bank_name = self.library.bank_name()[i]
                        if bank_name.text in bank_name_list:
                            continue
                        else:
                            bank_name_list.append(bank_name.text)
                            if self.library.wait_check_bank_list_page():
                                bank_progress = self.library.bank_progress_by_name(bank_name.text)
                                print('============ 🌟🌟' + bank_name.text + "🌟🌟==========\n")
                                print("书籍进程：", bank_progress)
                                bank_name.click()
                                HomeworkGameOperate().homework_game_operate(nickname, judge_score=False, has_medal=True)
                if self.library.wait_check_bank_list_page():
                    self.home.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            self.library.click_back_up_button()
















