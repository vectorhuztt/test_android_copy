#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/23 16:00
# -----------------------------------------
import unittest

from ddt import ddt, data

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.study_setting_page import StudySettingPage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class ReciteWord(unittest.TestCase):
    """复习单词"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.data = WordDataHandlePage()
        cls.login.app_status()  # 判断APP当前状态
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ReciteWord, self).run(result)

    @data(1)
    @testcase
    def test_recite_word_change_study_model(self, study_model):
        """测试复习新词设置"""
        if self.home.wait_check_home_page():
            stu_info = StudySettingPage().get_user_info()  # 获取学生信息
            stu_id = stu_info[0]
            self.data.clear_student_word_data(stu_id)        # 清除学生已学单词记录
            self.data.reset_student_wordbook_rule(stu_id)    # 恢复默认单词本设置
            self.data.change_all_word_fl_equal_one(stu_id)   # 将所有单词的F值更改为1
            self.data.change_10_word_fl_equal_three(stu_id)  # F值小于3的前十个单词的F值更改为3

            if self.home.wait_check_home_page():
                StudySettingPage().check_study_model_operate(study_model)
                if self.home.wait_check_home_page():
                    self.home.click_hk_tab(1)  # 点击 背单词
                    if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                        self.word_rebuild.word_start_button()  # 点击 Go按钮

                        group_num = 7 if study_model == 1 else 10
                        wrong_again_words, all_new_explain_words = [], []
                        all_recite_count = []
                        all_new_word = {}
                        for x in range(group_num):
                            if self.word_rebuild.wait_check_game_title_page():
                                # 游戏复习过程
                                recite_count = self.word_rebuild.recite_word_operate(stu_id, 3, wrong_again_words, right_words=[])
                                all_recite_count.append(recite_count)

                                # 闪卡新词游戏过程
                                flash_result = FlashCard().flash_study_model(stu_id, all_new_word, x, do_right=True)
                                if flash_result:

                                    # 校验每组新词个数是否正确
                                    self.word_rebuild.check_new_word_after_recite_process(flash_result, recite_count, x, study_model)
                                    group_new_explain_words = flash_result[3]  # 每组新释义单词
                                    all_new_explain_words.extend(group_new_explain_words)  # 将新释义单词加入新释义数组中
                                    # 其他新词游戏过程
                                    self.word_rebuild.normal_study_new_word_operate(stu_id, flash_result, do_right=True)

                                if ResultPage().wait_check_result_page():
                                    # 结果页单词统计核实
                                    self.data.change_10_word_fl_equal_three(stu_id)  # F值小于3的前十个单词的F值更改为3
                                    ResultPage().result_page_handle(len(self.word_info), len(all_new_explain_words),
                                                                    sum(all_recite_count), x)



