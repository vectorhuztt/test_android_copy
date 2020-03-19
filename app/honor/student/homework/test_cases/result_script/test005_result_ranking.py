#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import unittest

from app.honor.student.homework.object_page.single_choice_page import SingleChoice
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from conf.base_config import GetVariable as gv
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.user_center.object_page import UserInfoPage
from app.honor.student.user_center.object_page import UserCenterPage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """排行榜"""

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
    def test_result_ranking(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            self.login_page.enter_user_info_page()  # 由 主界面 进入个人信息页
            if UserInfoPage().wait_check_user_center_page():
                nickname = UserInfoPage().nickname()  # 获取昵称
                self.homework.back_up_button()  # 返回个人中心页面
                if UserCenterPage().wait_check_user_center_page():
                    self.home_page.click_tab_hw()  # 进入主界面

                    if self.home_page.wait_check_home_page():  # 页面检查点

                        self.home_page.click_hk_tab(2)  # 进入 做作业
                        if self.homework.wait_check_hw_page():  # 页面检查点

                            var = self.home_page.homework_count()
                            if gv.RANK in var[0]:  # 该作业存在
                                for i in range(0, len(var[0])):
                                    if var[0][i] == gv.RANK:
                                        var[1][i].click()  # 点击进入该游戏
                                        # self.homework.games_count(0, gv.RANK_TYPE)
                                        self.game_exist(gv.RANK_COUNT, nickname)  # 具体操作
                                        # if count[1] == 10:  # 小游戏list需翻页
                                        #     game_count = self.homework.swipe_screen(gv.RATE_TYPE)
                                        #     if len(game_count) != 0:
                                        #         self.game_exist(game_count)
                                        # self.homework.back_up_button()  # 返回主界面
                            else:
                                print('当前页no have该作业')
                                self.home_page.swipe_operate(var[0], gv.RANK, gv.RANK_TYPE)  # 作业list翻页
                                self.game_exist(gv.RANK_COUNT, nickname)  # 具体操作
                            print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count, nickname):
        """单项选择游戏 - 排行榜"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.RANK):
                    print('####################################################')
                    before = self.homework.ranking(index, nickname)  # 排行榜icon
                    if self.homework.wait_check_game_list_page(gv.RANK):
                        self.homework.games_type()[index].click()  # 进入小游戏

                        self.single_choe.single_choice_operate()  # 单项选择 - 游戏过程
                        self.result.result_page_ranking(nickname)  # 结果页 排行榜
                        self.homework.back_operate()  # 返回小游戏界面

                        if self.homework.wait_check_game_list_page(gv.RANK):
                            after = self.homework.ranking(index, nickname)  # 排行榜icon
                            # 以下为 做题前后排行榜icon内容比较 过程

                            if len(before) != 0 and len(after) != 0:  # 不是暂无数据 and 排行榜含有本人信息时
                                if before[0][0] < after[0][0]:  # 做题前后排行榜信息比较
                                    print('Congratulations 准确率提高了')
                                elif before[0][0] == after[0][0]:
                                    if before[0][1] > after[0][1]:
                                        print('Congratulations 所用时间短了')
                                    elif before[0][1] == after[0][1]:
                                        print('准确率&所用时间均相同')
                                    else:
                                        print('❌❌❌ 排名逻辑有问题 - 所用时间')
                                else:
                                    print('❌❌❌ 排名逻辑有问题 - 准确率')

                print('####################################################')
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have该类型小游戏')
        self.homework.back_up_button()  # 返回主界面
