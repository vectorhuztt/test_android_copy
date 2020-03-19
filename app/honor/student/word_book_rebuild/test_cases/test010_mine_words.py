#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/12 8:57
# -----------------------------------------
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.my_word_page import MineWordsPage
from app.honor.student.word_book_rebuild.object_page.study_setting_page import StudySettingPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class MineWords(unittest.TestCase):
    """我的单词"""

    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.data = WordDataHandlePage()
        cls.mine = MineWordsPage()
        cls.login.app_status()  # 判断APP当前状态
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(MineWords, self).run(result)

    @testcase
    def test_mine_words(self):
        if self.home.wait_check_home_page():
            stu_info = StudySettingPage().get_user_info()  # 获取学生信息
            stu_id = stu_info[0]
            studied_words = self.data.get_total_words(stu_id)
            print('已学单词总数：', len(studied_words))
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.word_rebuild.wait_check_start_page():  # 开始页面检查点
                    start_page_total_count = self.word_rebuild.total_word()
                    self.mine.click_my_word_btn()                                         # 点击我的单词
                    if self.mine.wait_check_mine_word_page():
                        if start_page_total_count:
                            mine_words_count = self.mine.total_word()                     # 单词总数
                            print('我的单词总数：', mine_words_count)
                            if mine_words_count != start_page_total_count:                # 单词总数与开始页面数据比较
                                print('❌❌❌ 我的单词单词总数与开始页面总数不一致！')
                            if mine_words_count != len(studied_words):                    # 单词总数与数据库数据比较
                                print('❌❌❌ 我的单词总数与数据库数据不一致！')
                            self.mine.get_all_mine_words(studied_words)                   # 获取所有我的单词 去重
                            self.mine.get_words()[0].click()                              # 点击当前页面第一个单词
                            count = 3
                            if self.mine.flash.wait_check_flash_study_page():
                                self.mine.flash_study_operate(count, stu_id)              # 闪卡游戏处理
                                self.mine.click_back_up_button()

                            if self.mine.spell.wait_check_normal_spell_page():
                                self.mine.spelling_operate(count, stu_id)                 # 单词拼写处理

                            if self.mine.flash.wait_check_copy_page():
                                self.mine.flash_copy_operate(count)                       # 闪卡抄写处理

                            if self.mine.wait_check_mine_word_page():
                                self.mine.click_back_up_button()                          # 返回重新进入我的单词
                                if self.word_rebuild.wait_check_start_page():
                                    self.mine.click_my_word_btn()
                                    self.mine.get_words()[0].click()

                                if self.mine.flash.wait_check_flash_study_page():
                                    self.mine.flash_study_operate(count, stu_id)          # 只进行闪卡处理，校验标星标熟
                                    self.mine.click_back_up_button()
                                    if self.mine.flash.wait_check_copy_page() or \
                                       self.mine.spell.wait_check_normal_spell_page():
                                        self.mine.click_back_up_button()
                                        self.mine.flash.tips_operate()                   # 提示页面处理

                                    if self.mine.wait_check_mine_word_page():
                                        self.mine.click_back_up_button()
                                    if self.word_rebuild.wait_check_start_page():
                                        self.word_rebuild.click_back_up_button()         # 返回主页面
                        else:
                            if not self.mine.wait_check_no_word_page():
                                print('❌❌❌ 已背单词个数为0， 但是未显示未背单词提示页面')
                            else:
                                print(self.mine.no_word_tip_text())






