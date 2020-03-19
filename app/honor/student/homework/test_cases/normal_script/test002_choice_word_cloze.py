#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import unittest

from app.honor.student.homework.object_page.choice_word_cloze_page import ChoiceWordCloze
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from conf.base_config import GetVariable as gv
from conf.decorator import setup, teardown
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """选词填空"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.choice = ChoiceWordCloze()
        cls.result = ResultPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    def test_choice_word_cloze(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            self.home_page.click_hk_tab(2)

            if self.homework.wait_check_hw_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.CHO_WOR_CL in var[0]:  # 该作业存在
                    for i in range(len(var[0])):
                        if var[0][i] == gv.CHO_WOR_CL:
                            var[1][i].click()  # 点击进入该作业
                            count = self.homework.games_count(0, '选词填空', gv.CHO_WOR_CL)
                            self.game_exist(count[0], gv.CHO_WOR_CL)

                            if count[1] == 10:  # 小游戏list需翻页
                                game_count = self.homework.swipe_screen('选词填空')
                                if len(game_count) != 0:
                                    self.game_exist(game_count, gv.CHO_WOR_CL)
                            break
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.CHO_WOR_CL, '选词填空')  # 作业list翻页
                    self.game_exist(game[0], gv.CHO_WOR_CL)
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    def game_exist(self, count, homework_title):
        """选词填空游戏具体操作 及 结果页操作"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.CHO_WOR_CL):
                    print('####################################################')
                    game_title = self.homework.games_title()[index].text  # 小游戏name
                    self.homework.games_type()[index].click()  # 进入小游戏

                    rate = self.choice.choice_word_filling()  # 选词填空 游戏过程
                    self.choice.check_detail_page(rate, homework_title, game_title)  # 查看答案 操作

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have选词填空小游戏')
        self.homework.back_up_button()  # 返回主界面
