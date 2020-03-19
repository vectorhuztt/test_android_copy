# coding=utf-8
import unittest

from app.honor.student.homework.object_page.vocabulary_choice_page import VocabularyChoice
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from conf.base_config import GetVariable as gv
from conf.decorator import setup, teardown, testcase, teststeps
from utils.toast_find import Toast


class Games(unittest.TestCase):
    """词汇选择"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login_page = LoginPage()
        cls.home_page = HomePage()
        cls.homework = Homework()
        cls.vocab_select = VocabularyChoice()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_vocabulary_choice(self):
        self.login_page.app_status()  # 判断APP当前状态

        if self.home_page.wait_check_home_page():  # 页面检查点
            self.home_page.click_hk_tab(2)

            if self.homework.wait_check_hw_page():  # 页面检查点
                var = self.home_page.homework_count()
                if gv.VOC_CHO in var[0]:   # 该作业存在
                    for i in range(0, len(var[0])):
                        if var[0][i] == gv.VOC_CHO:
                            var[1][i].click()  # 点击进入该作业
                            count = self.homework.games_count(0, '词汇选择', gv.VOC_CHO)   # 统计小游戏个数
                            self.game_exist(count[0])  # 具体操作

                            if count[1] == 10:    # 判断小游戏list是否需翻页
                                game_count = self.homework.swipe_screen('词汇选择')
                                if len(game_count) != 0:
                                    self.game_exist(game_count)
                            break
                else:
                    print('当前页no have该作业')
                    game = self.home_page.swipe_operate(var[0], gv.VOC_CHO, '词汇选择')  # 作业list翻页
                    self.game_exist(game[0])
                #
                # self.verification_result()  # 答题结果验证
                print('Game Over')
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def game_exist(self, count):
        """词汇选择游戏具体操作 及 结果页操作"""
        if len(count) != 0:
            for index in count:
                if self.homework.wait_check_game_list_page(gv.VOC_CHO):
                    print('####################################################')
                    homework_type = self.homework.tv_testbank_name(index)  # 获取小游戏模式
                    self.homework.games_type()[index].click()  # 进入小游戏
                    result = self.vocab_select.diff_type(homework_type)  # 不同模式小游戏的 游戏过程

                    self.vocab_select.result_detail_page(result[0])  # 结果页 查看答案 按钮
                    self.vocab_select.study_again(homework_type)  # 结果页 错题再练 按钮

                    print('####################################################')
                    self.homework.back_operate()  # 返回小游戏界面
            self.homework.back_up_button()  # 返回作业列表
        else:
            print('no have词汇选择小游戏')
        self.homework.back_up_button()  # 返回主界面
