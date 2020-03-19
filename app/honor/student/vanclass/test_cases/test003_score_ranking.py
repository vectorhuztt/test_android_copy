#!/usr/bin/env python
# encoding:UTF-8
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class ScoreRanking(unittest.TestCase):
    """积分排行榜"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.detail = VanclassDetailPage()
        cls.van = VanclassPage()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ScoreRanking, self).run(result)

    @testcase
    def test_score_ranking(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_test_vanclass()  # 班级tab
            if self.van.wait_check_page():  # 页面检查点

                van = self.van.vanclass_name()  # 班级名称
                for i in range(len(van)):
                    if van[i].text == gv.VAN_LIST:
                        van[i].click()  # 进入班级详情页
                        break
                if self.van.wait_check_vanclass_page(gv.VAN_LIST):  # 页面检查点

                    self.van.score_ranking()  # 进入 积分排行榜
                    if self.detail.wait_check_score_page():  # 页面检查点
                        print('积分排行榜:')
                        self.this_week_operate()  # 本周
                        self.last_week_operate()  # 上周
                        self.this_month_operate()  # 本月
                        self.all_score_operate()  # 全部

                        self.home.click_back_up_button()
                        if self.van.wait_check_vanclass_page(gv.VAN_LIST):  # 班级详情 页面检查点
                            self.home.click_back_up_button()
                            if self.van.wait_check_page():  # 班级 页面检查点
                                self.home.click_tab_hw()  # 返回主界面
                    else:
                        print('未进入 积分排行榜页面')
                        self.home.click_back_up_button()
                        if self.van.wait_check_page():  # 班级 页面检查点
                            self.home.click_tab_hw()  # 返回主界面
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def this_week_operate(self):
        """本周tab 具体操作"""
        this_week = self.detail.score_all_tab(1)
        if self.detail.selected(this_week) is False:
            self.base_assert.except_error('Error- 默认在 本周页面')
        else:
            print('-------------------本周tab-------------------')
            if self.van.empty_tips():
                print('暂无数据')
            else:
                self.score_operate()

    @teststeps
    def last_week_operate(self):
        """上周tab 具体操作"""
        last = self.detail.score_all_tab(2)  # 上周
        if self.detail.selected(last) is True:
            self.base_assert.except_error('Error- 默认在 上周页面')
        else:
            last.click()  # 进入 上周 页面
            if self.detail.selected(last) is False:
                self.base_assert.except_error('Error- 未进入 上周页面')
            else:
                print('-------------------上周tab-------------------')
                if self.van.empty_tips():
                    print('暂无数据')
                else:
                    self.score_operate()

    @teststeps
    def this_month_operate(self):
        """本月tab 具体操作"""
        this_month = self.detail.score_all_tab(3)  # 本月
        if self.detail.selected(this_month) is True:
            self.base_assert.except_error('Error- 默认在 本月页面')
        else:
            this_month.click()  # 进入 本月 页面
            if self.detail.selected(this_month) is False:
                self.base_assert.except_error('Error- 未进入 本月页面')
            else:
                print('-------------------本月tab-------------------')
                if self.van.empty_tips():
                    print('暂无数据')
                else:
                    self.score_operate()

    @teststeps
    def all_score_operate(self):
        """全部tab 具体操作"""
        all_score = self.detail.score_all_tab(4)  # 全部
        if self.detail.selected(all_score) is True:
            self.base_assert.except_error('Error- 默认在 全部页面')
        else:
            all_score.click()  # 进入 全部 页面
            if self.detail.selected(all_score) is False:
                self.base_assert.except_error('Error- 未进入 全部页面')
            else:
                print('-------------------全部tab-------------------')
                if self.van.empty_tips():
                    print('暂无数据')
                else:
                    self.score_operate()

    @teststeps
    def score_operate(self):
        """积分排行榜页面具体操作"""
        order = self.detail.st_order()  # 编号
        icon = self.detail.st_icon()  # 头像
        name = self.detail.st_name()  # 昵称
        num = self.detail.num()  # 积分数
        if len(order) < 11:  # 少于8个
            if len(order) != len(icon) != len(name) != len(num):
                self.base_assert.except_error('Error- 学生 编号、头像、昵称、积分的个数不等')
            else:
                for i in range(len(order)):
                    print('------------------')
                    print(order[i].text, name[i].text, num[i].text)
        else:  # 多于8个 todo
            for i in range(10):
                print('------------------')
                print(order[i].text, name[i].text, num[i].text)
