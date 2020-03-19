# coding=utf-8
import time
import unittest

from ddt import ddt, data

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.account import VALID_ACCOUNT
from app.honor.student.word_book.object_page.flash_card_game import FlashCardProcess
from app.honor.student.word_book.object_page.other_game_process import GameOperate
from app.honor.student.word_book.object_page.recite_word_operate import ReciteWordPage
from app.honor.student.word_book.object_page.result_page import WordResultPage
from app.honor.student.word_book.object_page.wordbook_sql import WordBookSql
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.decorator import teardown, testcase, setup

@ddt
class Word (unittest.TestCase):
    """单词本"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.stu_id = WordBookSql().find_student_id(VALID_ACCOUNT.account())[0][0]

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @data(1, 2)
    @testcase
    def test_study_word(self, group_index):
        """新词练习"""
        print('===== 第{}组练习 =====' .format(group_index))
        word_info = {}
        recite_words_count = 0
        wrong_again_words = []
        if group_index == 1:
            if self.home.wait_check_home_page():
                UserCenterPage().get_user_info()  # 获取学生信息
                if self.home.wait_check_home_page():
                    self.home.click_hk_tab(1)  # 点击 背单词
                    if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                        self.word_rebuild.word_start_button()      # 点击 Go按钮
                    elif self.word_rebuild.wait_check_continue_page():
                        print('❌❌❌ 缓存未清除成功')
                    time.sleep(3)
            else:
                print('❌❌❌ 未进入主页面')
            today_already_study_word_data = [0, 0, 0]
        else:
            today_already_study_word_data = self.word_rebuild.data.get_student_today_word_data(self.stu_id)

        while self.word_rebuild.wait_check_game_title_page():
            title = self.word_rebuild.public.game_title().text
            if '新词' in title or '新释义' in title:
                flash_result = FlashCardProcess().flash_card_operate(word_info)
                if flash_result:
                    GameOperate().new_word_other_game_operate(flash_result, word_info, self.stu_id)
            elif '复习' in title:
                recite_words_count = ReciteWordPage().word_book_recite_operate(self.stu_id, wrong_again_words)
            else:
                break

        if self.word_rebuild.wait_check_start_wrong_again_page():
            self.word_rebuild.confirm_btn().click()
            SpellingWord().dictation_random_pattern_recite(self.stu_id, wrong_again_words)
            if self.word_rebuild.wait_check_game_title_page():
                if '单词拼写(复习)' in self.word_rebuild.public.game_title().text:
                    print('❌❌❌ 错题再练个数与记录个数不一致')
        else:
            print('没有错题再练')

        if ResultPage().wait_check_result_page():
            # 结果页单词统计核实
            WordResultPage().verify_result_page_data(self.stu_id, today_already_study_word_data,  word_info,
                                                     recite_words_count, group_index)


