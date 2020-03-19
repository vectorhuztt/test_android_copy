#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/25 17:08
# -----------------------------------------
import unittest

from ddt import ddt, data

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class ReciteFirstReturnWords(unittest.TestCase):
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
        cls.word_info = {}  # 记录所有单词
        cls.new_explain_words = []

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ReciteFirstReturnWords, self).run(result)

    @data(1,2)
    @testcase
    def test_normal_recite_operate(self, level):
        if self.home.wait_check_home_page():
            new_words, new_explain_words = [], []
            recite_count = 0
            stu_info = UserCenterPage().get_user_info()  # 获取学生信息
            stu_id = stu_info[0]
            self.word_rebuild.data.change_level_in_interval_date(stu_id, level)  # 更改指定F值的日期
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                    self.word_rebuild.word_start_button()  # 点击 Go按钮

            for x in range(2):
                wrong_again_words = []
                right_explains = self.word_rebuild.data.get_student_new_all_right_explains(stu_id)  # 获取学生新词全对单词
                print('新词非标熟且全对解释：', right_explains)
                if '复习' in self.word_rebuild.public.game_title().text:
                    recite_count += self.word_rebuild.recite_word_operate(stu_id, level, wrong_again_words, right_explains)  # 复习单词过程
                    if self.word_rebuild.wait_check_start_wrong_again_page():             # 错题再练过程
                        self.word_rebuild.confirm_btn().click()
                        SpellingWord().dictation_random_pattern_recite(stu_id, wrong_again_words)
                        if self.word_rebuild.wait_check_game_title_page():
                            if '单词拼写(复习)' in self.word_rebuild.public.game_title().text:
                                print('❌❌❌ 错题再练个数与记录个数不一致')
                else:
                    if FlashCard().wait_check_flash_study_page():                  # 遇到新词退出
                        flash_result = FlashCard().scan_game_operate()             # 闪卡游戏, 默认不标熟
                        new_words.extend(list(flash_result[0].keys()))
                        new_explain_words.extend(flash_result[-1])
                        if len(flash_result[0]) > 10:
                            print('❌❌❌ 新词个数大于10')
                        self.word_rebuild.normal_study_new_word_operate(stu_id, flash_result, do_right=True)  # 其他新词游戏过程

                if ResultPage().wait_check_result_page():
                    ResultPage().result_page_handle(len(list(set(new_words))), len(new_explain_words), recite_count, x)
            self.word_rebuild.from_wordbook_back_to_home()