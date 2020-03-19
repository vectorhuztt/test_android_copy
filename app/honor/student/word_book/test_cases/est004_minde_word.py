import unittest

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book.object_page.data_action import WordBookDataHandle
from conf.decorator import setup, teardown, teststeps


class MineWord(unittest.TestCase):

    @classmethod
    @setup
    def setUp(cls):
        cls.home = HomePage()
        cls.word = WordBook()
        cls.mine = MyWordPage()
        cls.common = WordBookDataHandle()


    @teardown
    def tearDown(self):
        pass

    @teststeps
    def test_mine_word(self):
        """我的单词"""
        if self.home.wait_check_home_page():  # 页面检查点
            stu_info = UserCenterPage().get_user_info()
            stu_id = stu_info[0]
            if self.home.wait_check_home_page():  # 页面检查点
                print('进入主界面')
                self.home.click_hk_tab(1)  # 点击 背单词
                if self.home.wait_check_word_title():  # 页面检查点
                    total = self.word.total_word()
                    self.mine.click_my_word_btn()
                    if self.mine.wait_check_mine_word_page():
                        if self.mine.no_word_tips():
                            self.mine.no_word_tip_text()
                        else:
                            self.mine.play_mine_word(stu_id, total)

