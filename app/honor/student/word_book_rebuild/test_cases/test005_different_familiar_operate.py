#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/18 17:00
# -----------------------------------------
import unittest

from ddt import ddt, data

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class ReciteFirstReturnWords(unittest.TestCase):
    """复习不同标熟情况下的单词"""
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
        cls.word_info = {}  # 记录所有单词
        cls.new_explain_words = []
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ReciteFirstReturnWords, self).run(result)

    @data(4)
    @testcase
    def est_recite_B_return_new_words(self, familiar_type):
        first_group_familiar = []  # 第一组标熟单词
        right_words = []  # 新词做对单词
        all_new_words = []
        if self.home.wait_check_home_page():
            stu_info = UserCenterPage().get_user_info()  # 获取学生信息
            stu_id = stu_info[0]
            self.word_rebuild.data.clear_student_word_data(stu_id)  # 清除学生已学单词记录

            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                    self.word_rebuild.word_start_button()  # 点击 Go按钮
                elif self.word_rebuild.wait_check_continue_page():
                    self.base_assert.except_error('缓存未清除成功')

                word_has_different_explain = self.word_rebuild.data.get_word_has_different_explains(stu_id)
                for x in range(2):
                    do_right = self.word_rebuild.set_do_right_by_familiar_type(familiar_type, x)
                    # 不同情况的标熟情况
                    flash_result = FlashCard().\
                        flash_different_familiar_operate(stu_id, self.word_info, familiar_type, x,
                                                         first_group_familiar, word_has_different_explain)
                    if flash_result:
                        first_group_familiar = list(flash_result[1].values())
                        print('标熟单词：', first_group_familiar)

                        group_new_explain_words = flash_result[3]           # 每组的新词新释义单词
                        all_new_words.append(len(flash_result[0]))               # 将所有单词数量 加入所有新词中
                        self.new_explain_words.extend(group_new_explain_words)   # 将每组新释义单词加入数组中
                        # 其他新词游戏过程
                        normal_game_words = self.word_rebuild.normal_study_new_word_operate(stu_id, flash_result, do_right)
                        if do_right:
                            right_words.extend(normal_game_words)
                        print('正确单词：', all_new_words)
                    if ResultPage().wait_check_result_page():
                        # 结果页单词统计核实
                        ResultPage().result_page_handle(len(self.word_info.keys()), len(self.new_explain_words),
                                                        already_recite_count=0, group_count=x)
                self.word_rebuild.from_wordbook_back_to_home()

    @testcase
    def test_recite_B_return_recite_words(self):
        if self.home.wait_check_home_page():
            stu_info = UserCenterPage().get_user_info()  # 获取学生信息
            stu_id = stu_info[0]
            self.word_rebuild.data.change_level_limit_word_date(stu_id, 1)  # 更改指定F值的日期
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                    self.word_rebuild.word_start_button()  # 点击 Go按钮
                    wrong_again_words, all_words = [], []
                    right_explains = self.word_rebuild.data.get_student_new_all_right_explains(stu_id)    # 获取学生新词全对单词
                    print('新词非标熟且全对解释：', right_explains)
                    self.word_rebuild.recite_word_operate(stu_id, 1, wrong_again_words, right_explains)
                    if FlashCard().wait_check_flash_study_page():
                        self.word_rebuild.from_wordbook_back_to_home()










