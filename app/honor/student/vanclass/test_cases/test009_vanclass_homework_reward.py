#!/usr/bin/env python
# encoding:UTF-8
import unittest
import re

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.vanclass.test_data.vanclass_data import GetVariable as gv
from app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.toast_find import Toast


class HwReward(unittest.TestCase):
    """本班作业 - 打卡"""

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
        super(HwReward, self).run(result)

    @testcase
    def test_homework_reward(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_test_vanclass()  # 班级tab
            if self.van.wait_check_page():  # 页面检查点

                van = self.van.vanclass_name()  # 班级名称
                for i in range(len(van)):
                    if van[i].text == gv.CLASS_NAME:
                        van[i].click()  # 进入班级详情页
                        break
                if self.van.wait_check_vanclass_page(gv.CLASS_NAME):  # 页面检查点

                    self.van.vanclass_hw()  # 点击 本班作业 tab
                    if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                        print('%s 本班作业:' % gv.CLASS_NAME)
                        if self.van.empty_tips():
                            print('暂无数据')
                        else:
                            all_hw = self.detail.all_tab()  # 全部 tab
                            if self.detail.selected(all_hw) is False:
                                self.base_assert.except_error('Error- 未默认在 全部页面')
                            incomplete = self.detail.finished_tab()  # 未完成 tab
                            incomplete.click()  # 进入 未完成 tab页
                            if self.detail.selected(incomplete) is False:
                                self.base_assert.except_error('Error- 未进入 已完成 tab页')
                            else:
                                print('--------------已完成tab-------------------')
                                self.share_operate()
                                if self.detail.wait_check_page(gv.CLASS_NAME):  # 页面检查点
                                    self.home.click_back_up_button()  # 返回 班级详情 页
                                else:
                                    print('未返回 本班作业页面')
                    else:
                        print('未进入班级 -本班作业tab')
                        self.home.click_back_up_button()

                    if self.van.wait_check_quit_vanclass(gv.CLASS_NAME):  # 班级 页面检查点
                        self.home.click_back_up_button()  # 返回主界面
                        if self.van.wait_check_page():
                            self.home.click_tab_hw()
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def share_operate(self):
        """分享"""
        hw_names = self.detail.hw_name()
        select_hw = hw_names[0]
        select_name = select_hw.text
        select_hw.click()
        if self.detail.wait_check_page(select_name):  # 页面检查点
            self.detail.reward_button()  # 打卡按钮
            if self.detail.wait_check_reward_page():
                if self.detail.reward_desc() != '您暂时无法打卡':
                    self.detail.reward_tips()  # 打卡说明
                    self.detail.reward_desc()  # 获取礼包提示
                    self.detail.get_reward_button()  # 礼包 按钮

                    if self.detail.wait_check_reward_result_page():
                        print('---------------------------')
                        if self.detail.reward_img():  # 打卡后 获得的图片
                            self.detail.reward_tips()  # 打卡说明
                            self.detail.reward_desc()  # 获取礼包提示

                            self.detail.check_complete_button()  # 查看完整卡片 按钮
                            if self.detail.wait_check_complete_page():
                                num = self.detail.img_num()
                                for i in range(len(num)):
                                    if num[i].text != 0:
                                        break

                                self.home.click_back_up_button()  # 返回
                        else:
                            self.base_assert.except_error('Error- 无打卡图片')
                else:
                    self.detail.get_reward_button()  # 礼包 按钮
                    Toast().find_toast('暂时没有打卡机会了')
                    print(self.detail.reward_desc(), ',暂时没有打卡机会了')  # 打卡说明
                    self.detail.reward_tips()  # 获取礼包提示

                if self.detail.wait_check_reward_page():  # 页面检查点
                    self.home.click_back_up_button()  # 返回
                    if self.detail.wait_check_page(select_name):  # 页面检查点
                        self.home.click_back_up_button()  # 返回

        else:
            print('未进入作业 %s 页面' % select_name)
