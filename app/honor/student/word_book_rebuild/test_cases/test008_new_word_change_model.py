#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/23 14:50
# -----------------------------------------
import unittest

from ddt import ddt, data

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.study_setting_page import StudySettingPage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class NewWordChangeModel(unittest.TestCase):
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
        super(NewWordChangeModel, self).run(result)

    @data(2)
    @testcase
    def test_new_word_change_study_model(self, study_model):
        """测试新词游戏设置"""
        if self.home.wait_check_home_page():
            stu_info = StudySettingPage().get_user_info()  # 获取学生信息
            stu_id = stu_info[0]
            self.data.clear_student_word_data(stu_id)  # 清除学生已学单词记录
            self.data.reset_student_wordbook_rule(stu_id)

            if self.home.wait_check_home_page():
                StudySettingPage().check_study_model_operate(study_model)
                if self.home.wait_check_home_page():
                    self.home.click_hk_tab(1)                         # 点击 背单词
                    if self.word_rebuild.wait_check_start_page():     # 开始页面检查点
                        self.word_rebuild.word_start_button()  # 点击 Go按钮

                group_num = 7 if study_model == 1 else 10
                all_explains, new_explain_words = [], []
                for x in range(group_num):
                    print("\n================ 练习组数：{}======================".format(x), '\n')
                    if self.word_rebuild.wait_check_game_title_page():
                        flash_result = FlashCard().scan_game_operate(familiar=True)
                        all_explains.extend(list(flash_result[0].keys()))
                        new_explain_words.extend(flash_result[-1])
                        if len(flash_result[0]) > 10:
                            self.base_assert.except_error('新词个数大于10')

                        if '单词拼写' in self.word_rebuild.public.game_title().text:
                            SpellingWord().new_word_spell_operate(flash_result[0], flash_result[-1])

                        if ResultPage().wait_check_result_page():
                            # 结果页单词统计核实
                            all_words = [self.data.get_word_by_explain_id(stu_id, x) for x in all_explains]  # 根据解释id获取单词
                            ResultPage().result_page_handle(len(list(set(all_words))), len(new_explain_words), 0, x)






