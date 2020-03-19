import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.word_book_rebuild.object_page.ranking_page import RankingPage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.decorator import teardown, teststeps,setup


class Ranking (unittest.TestCase):
    """单词本"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.home = HomePage()
        cls.word = WordBookRebuildPage()
        cls.login = LoginPage()
        cls.rank = RankingPage()
        cls.login.app_status()  # 判断APP当前状态


    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @teststeps
    def test_rank_word(self):
        """排行榜"""
        if self.home.wait_check_home_page():  # 页面检查点
            print('进入主界面')
            self.home.click_hk_tab(1)            # 点击 背单词
            if self.home.wait_check_word_title():
                total_words = self.rank.total()
                self.rank.click_rank_icon()     # 点击排行榜图标
                if self.rank.wait_check_rank_page():
                    self.rank.play_rank_word(total_words)





