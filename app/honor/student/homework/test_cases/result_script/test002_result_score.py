#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
import unittest

from app.honor.student.homework.object_page.single_choice_page import SingleChoice
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from conf.base_config import GetVariable as gv
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from utils.excel_read_write import ExcelUtil
from utils.toast_find import Toast
from conf.decorator import setup, teardown, testcase, teststeps


class Games(unittest.TestCase):
    """积分"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.single_choe = SingleChoice()
        cls.result = ResultPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_result_score(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():
            self.home_page.click_hk_tab(2)

            if self.homework.wait_check_hw_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.SCORE in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.SCORE:
                            var[1][i].click()  # 点击进入该作业
                            # self.homework.games_count(0, gv.SCORE_TYPE)
                            self.game_exist(gv.SCORE_COUNT, gv.SCORE)

                            # if count[1] == 10:  # 小游戏list需翻页
                            #     game_count = self.homework.swipe_screen(gv.RATE_TYPE)
                            #     if len(game_count) != 0:
                            #         self.game_exist(game_count)
                            # self.homework.back_up_button()  # 返回主界面
                else:
                    print('当前页no have该作业')
                    self.home_page.swipe_operate(var[0], gv.SCORE, gv.SCORE_TYPE)  # 作业list翻页
                    self.game_exist(gv.SCORE_COUNT, gv.SCORE)
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count, homework_title):
        """单项选择游戏 - 积分"""
        time.sleep(1)
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.SCORE):
                    print('####################################################')
                    game_status = self.homework.status()[index].text
                    game_title = self.homework.games_title()[index].text
                    self.homework.games_type()[index].click()  # 进入小游戏

                    result = self.single_choe.single_choice_operate()  # 单项选择 - 游戏过程
                    excel = ExcelUtil().\
                        excel_operate(result[0], game_status, result[2], homework_title, game_title, '')
                    self.result.result_page_score(excel[1])  # 结果页 -- 积分

                    result2 = self.single_choe.study_again()  # 结果页 错题再练 按钮
                    excel2 = ExcelUtil().\
                        excel_operate(result2[1], game_status, result2[2], homework_title, game_title, result2[0])
                    self.result.result_page_score(excel2[1] + excel[1])  # 结果页 -- 积分

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have该类型小游戏')
        self.homework.back_up_button()  # 返回主界面
