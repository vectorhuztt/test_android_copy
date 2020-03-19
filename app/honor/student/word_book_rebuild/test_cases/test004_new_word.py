#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 11:00
# -----------------------------------------
import unittest

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class NewWord(unittest.TestCase):
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
        # cls.word_info = cls.word_rebuild.read_words_info_from_file('word.json')  # 记录所有单词
        cls.word_info = {}
        cls.new_explain_words = []

    @teardown
    def tearDown(self):
        self.word_rebuild.write_words_to_file('new_explain_words.txt', self.new_explain_words)
        self.word_rebuild.write_words_to_file('word.json', self.word_info)
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(NewWord, self).run(result)


    @testcase
    def test_new_word(self, do_right=False):
        """测试新词"""
        if self.home.wait_check_home_page():

            # 取消所有班级布置的单词
            # for x in TEACHER_ACCOUNT:
            #     AssignWord().revoke_van_class_wordbook_operate(x, STU_PASSWORD)
            #     LoginWebPage().logout_operate()
            # QuitAddClass().quit_all_class_operate()

            stu_info = UserCenterPage().get_user_info()            # 获取学生信息
            stu_id = stu_info[0]
            WordDataHandlePage().clear_student_word_data(stu_id)   # 清除学生已学单词记录
            self.word_info = {}
            # WordDataHandlePage().clear_word_finish_date(stu_id)

            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)                         # 点击 背单词
                if self.word_rebuild.wait_check_start_page():     # 开始页面检查点
                    self.word_rebuild.word_start_button()          # 点击 Go按钮

                elif self.word_rebuild.wait_check_continue_page():  # 若为继续页面，则说明未清除缓存
                    self.base_assert.except_error('缓存未清除成功')
                    self.word_rebuild.word_continue_button()

                recite_words, all_words = [], []  # 复习单词, 新词
                for x in range(2):
                    if self.word_rebuild.wait_check_game_title_page():
                        #  闪卡学习过程 返回闪卡题数，标星标熟
                        flash_result = FlashCard().flash_study_model(stu_id, self.word_info, x, do_right)
                        if flash_result:
                            group_new_explain_words = flash_result[3]          # 每组新释义单词
                            all_words.append(len(flash_result[0]))             # 把每组新词个数加入新词数组
                            self.new_explain_words.extend(group_new_explain_words)    # 将新释义单词加入新释义数组中
                            # 其他新词游戏过程
                            self.word_rebuild.normal_study_new_word_operate(stu_id, flash_result, do_right)  # 游戏过程
                    if ResultPage().wait_check_result_page():
                        # 结果页单词统计核实
                        ResultPage().result_page_handle(len(self.word_info), len(self.new_explain_words),
                                                        len(recite_words), x)
                self.word_rebuild.click_back_up_button()
                self.home.tips_operate_commit()
