# coding=utf-8
import unittest

from app.honor.student.homework.object_page.flash_card_page import FlashCardPage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from conf.base_config import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """闪卡练习"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.flash_card = FlashCardPage()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_flash_card(self):
        """对不同小游戏类型，选择不同函数进行相应的操作"""
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            self.home_page.click_hk_tab(2)  # 进入习题

            if self.homework.wait_check_hw_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.FLA_CARD in var[0]:  # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.FLA_CARD:
                            var[1][i].click()  # 点击进入该作业
                            count = self.homework.games_count(0, '闪卡练习', gv.FLA_CARD)  # 小游戏个数统计
                            self.game_exist(count[0])

                            if count[1] == 10:  # 小游戏list需翻页
                                game_count = self.homework.swipe_screen('闪卡练习')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                            break
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.FLA_CARD, '闪卡练习')  # 作业list翻页
                    self.game_exist(game[0])

                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """闪卡练习游戏具体操作 """
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.FLA_CARD):
                    print('####################################################')
                    if index == count[1]:
                        homework_type = self.homework.tv_game_type(index)  # 获取小游戏模式
                    else:
                        homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式
                    print(homework_type)
                    if homework_type == "学习模式":
                        self.flash_card_study(index)
                    elif homework_type == "抄写模式":
                        self.flash_card_copy(index)
                    print('####################################################')
                    if self.flash_card.wait_check_result_page():  # 结果页检查点
                        self.homework.back_up_button()
            self.homework.back_up_button()  # 返回 作业列表
        else:
            print('no have闪卡练习小游戏')

        self.homework.back_up_button()  # 返回主界面

    @teststeps
    def flash_card_study(self, index):
        """闪卡练习--学习模式"""
        self.homework.games_type()[index].click()  # 进入小游戏
        result = self.flash_card.study_pattern()  # 闪卡练习 学习游戏过程

        # 结果页 标星内容再练一遍
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            print('标星内容再练一遍:')
            self.flash_card.selected_sum()  # 标星内容统计
            self.flash_card.star_again_button()  # 点击 标星内容再练一遍 按钮
            self.flash_card.study_pattern()  # 闪卡练习 学习模式游戏过程

        # 结果页 再练一遍
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            print('再练一遍:')
            self.flash_card.study_again_button()  # 点击 再练一遍 按钮
            self.flash_card.study_pattern()  # 闪卡练习 学习模式游戏过程

        if self.flash_card.wait_check_result_page():  # 结果页检查点
            self.flash_card.result_page(result[0], result[1])  # 点击结果页听力按钮 和 star按钮

    @teststeps
    def flash_card_copy(self, index):
        """闪卡练习--抄写模式"""
        self.homework.games_type()[index].click()  # 进入小游戏
        result = self.flash_card.copy_pattern()  # 闪卡练习 抄写模式 游戏过程

        # 结果页 标星内容再练一遍
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            print('标星内容再练一遍:')
            self.flash_card.selected_sum()  # 标星内容统计
            self.flash_card.star_again_button()  # 点击 标星内容再练一遍 按钮
            self.flash_card.copy_pattern()  # 闪卡练习 抄写模式游戏过程

        # 结果页 再练一遍
        if self.flash_card.wait_check_result_page():  # 结果页检查点
            print('再练一遍:')
            self.flash_card.study_again_button()  # 点击 再练一遍 按钮
            self.flash_card.copy_pattern()  # 闪卡练习 游戏过程

        if self.flash_card.wait_check_result_page():  # 结果页检查点
            self.flash_card.result_page(result[0], result[1])  # 点击结果页听力按钮 和 star按钮
