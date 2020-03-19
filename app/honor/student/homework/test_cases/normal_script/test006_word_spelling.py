# coding=utf-8
import time
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.word_spelling_page import WordSpelling
from conf.base_config import GetVariable as gv
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """单词拼写"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.word_spelling = WordSpelling()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_word_spelling(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():
            self.home_page.click_hk_tab(2)

            if self.homework.wait_check_hw_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.WOR_SPE in var[0]:
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.WOR_SPE:
                            var[1][i].click()  # 点击进入该作业
                            count = self.homework.games_count(0, '单词拼写', gv.WOR_SPE)  # 小游戏个数统计
                            self.game_exist(count[0])  # 具体操作

                            if count[1] == 10:  # 判断小游戏list是否需滑屏
                                game_count = self.homework.swipe_screen('单词拼写')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                            break
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.WOR_SPE, '单词拼写')  # 作业list翻页
                    self.game_exist(game[0])
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """单词拼写游戏具体操作 及 结果页操作"""
        time.sleep(1)
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.WOR_SPE):
                    print('##########################################')
                    homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式

                    self.homework.games_type()[index].click()  # 进入小游戏
                    result = self.word_spelling.diff_type(homework_type)  # 不同模式小游戏的 游戏过程
                    self.word_spelling.result_detail_page(result[0])  # 结果页 查看答案 按钮
                    self.word_spelling.study_again(homework_type)  # 结果页 再练一遍 按钮

                    # if game_status == '未开始':
                    #     for i in range(len(answer[1])):
                    #         ExcelUtil(gev.EXCEL_PATH).data_write(answer[0], homework_title, game_title, answer[1][i])

                    print('##########################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have单词拼写小游戏')
        self.homework.back_up_button()  # 返回主界面
