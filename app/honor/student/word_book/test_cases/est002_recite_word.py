import unittest

from ddt import ddt, data

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.word_recite import ReciteProgress
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.decorator import teardown, teststeps, setup

@ddt
class Word(unittest.TestCase):
    """单词本"""

    @classmethod
    @setup
    def setUp(cls):
        cls.word = WordBookRebuildPage()
        cls.home = HomePage()
        cls.result = ResultPage()
        cls.login = LoginPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.recite = ReciteProgress()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @data(2)
    @teststeps
    def test_main_recite_word(self, level):
        """复习单词"""
        if self.home.wait_check_home_page():
            user_info = UserCenterPage().get_user_info()
            stu_id = user_info[0]
            self.recite.set_recite_date(stu_id, level)  # 更改复习单词的时间
            self.home.click_tab_hw()  # 返回主页面
            if self.home.wait_check_home_page():
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.home.wait_check_word_title():
                    if self.word.wait_check_start_page():
                        self.word.word_start_button()  # 点击 Go按钮

                        if self.word.wait_check_count_limit_page():
                            self.recite.limit_page_handle()  # 次数限制处理
                        else:
                            print('开始单词本练习')

                    elif self.word.wait_check_continue_page():  # 继续按钮
                        self.word.word_continue_button()     # 继续练习

                    # 复习过程
                    for j in range(1):
                        if self.word.wait_check_game_page():
                            self.recite.recite_progress(stu_id, j, level)

                            if self.result.wait_check_result_page():
                                self.result.more_again_button()  # 再练一次

                                if self.word.wait_check_game_page():  # 出现游戏页面
                                    self.recite.recite_progress(stu_id, j, level)

                                elif self.word.wait_check_count_limit_page():  # 出现次数限制页面
                                    self.recite.limit_page_handle()
                                    self.word.back_to_home()

                                elif self.result.wait_check_next_grade():
                                    self.word.back_to_home()
                                    break
                        else:
                            self.word.back_to_home()
                            break
            else:
                print("未进入主界面")
