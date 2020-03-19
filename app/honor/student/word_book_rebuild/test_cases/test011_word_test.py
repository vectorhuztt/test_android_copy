#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/29 15:41
# -----------------------------------------
import unittest
from ddt import ddt, data, unpack

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.word_test_page import WordTestPage
from app.honor.student.word_book_rebuild.object_page.word_test_result_page import WordTestResultPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest

@ddt
class WordTest(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.word_test = WordTestPage()
        cls.word_result = WordTestResultPage()
        cls.word_rebuild = WordBookRebuildPage()
        cls.login.app_status()  # 判断APP当前状态
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(WordTest, self).run(result)

    @data(
          # [1, False],
          [2, False],
          # [2, True],
          )
    @unpack
    @testcase
    def test_word_test(self, test_type, do_pass):
        """
        :param test_type: 1 只校验测试单词是否正确 2: 做题，结果页数据核对，错题再练
        :param do_pass: true 全做对 false 不做全对
        :return:
        """
        if self.home.wait_check_home_page():
            stu_info = UserCenterPage().get_user_info()
            stu_id = stu_info[0]
            nickname = stu_info[-1]
            self.word_test.sql_handler.delete_student_test_data(stu_id)
            fvalue_glt_3_count = self.word_test.sql_handler.get_f_glt_3_count(stu_id)

            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词

                for x in range(1):
                    fvalue_glt_3_words = self.word_test.sql_handler.get_test_words(stu_id, 1)
                    test_fail_words = self.word_test.sql_handler.get_test_words(stu_id, 2)
                    test_pass_words = self.word_test.sql_handler.get_test_words(stu_id, 3)
                    print('未测过且F>=3的单词个数：', len(fvalue_glt_3_words),
                          '\n测试未通过单词个数：', len(test_pass_words),
                          '\n测试通过单词个数：', len(test_fail_words),
                          '\n')

                    if self.word_rebuild.wait_check_start_page():
                        self.word_test.click_word_test_tab()

                        if self.word_test.wait_check_no_test_word_page():
                            if fvalue_glt_3_count >= 20:
                                self.base_assert.except_error('F值大于等于3的个数大于等于20，未进入复习页面')
                            self.word_test.click_confirm_btn()
                            if not self.word_rebuild.wait_check_start_page():
                                self.base_assert.except_error("无词复习点击确定后未返回单词本开始页面")

                        if self.word_test.wait_check_select_word_count_page():
                            if fvalue_glt_3_count < 20:
                                self.base_assert.except_error("F值大于等于3的个数小于20， 但是出现开始复习页面")

                    # 根据单词筛选顺序从数据库获得需要测试的单词
                    test_words_dict = self.word_test.get_test_word_list(fvalue_glt_3_words, test_fail_words, test_pass_words, x)
                    print('从数据库获取需要复习的单词：', list(test_words_dict.keys()))
                    if test_type == 1:
                        self.word_test.check_preview_word_operate(test_words_dict)
                        self.word_test.sql_handler.delete_student_test_data(stu_id)
                        self.word_test.click_back_up_button()
                    else:
                        for i in range(2):
                            test_answer, word_id_list = self.word_test.check_preview_word_operate(test_words_dict)
                            self.word_test.click_start_test_btn()
                            if i == 1:
                                do_pass = True
                            game_info = self.word_test.play_test_word_spell_operate(len(test_words_dict), test_answer, do_pass)
                            # 验证预览与做题是否打乱顺序
                            # if game_info[1] == word_id_list:
                            #     self.base_assert.except_error("预览单词顺序与实际做题顺序一致，顺序未打乱")
                            reform_words_dict = {x: test_words_dict[x] for x in game_info[1]}
                            wrong_word_dict = self.word_result.check_result_page_data_operate(stu_id, nickname, reform_words_dict, game_info[0], i)
                            if self.word_result.wait_check_test_result_page():
                                if i != 1:
                                    self.word_result.wrong_again_btn().click()
                                    test_words_dict = wrong_word_dict
                                else:
                                    self.word_result.result_back_btn().click()




























