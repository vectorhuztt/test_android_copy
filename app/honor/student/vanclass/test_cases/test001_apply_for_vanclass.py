#!/usr/bin/env python
# encoding:UTF-8
import time
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.vanclass.object_page.vanclass_detail_page import VanclassDetailPage
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.vanclass.test_data.remark_name_data import name_data, class_data_dev, class_data_test, class_data
from conf.base_config import GetVariable
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase, teststeps
from utils.assert_func import ExpectingTest
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class ApplyVanclass(unittest.TestCase):
    """申请 入班"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.van = VanclassPage()
        cls.detail = VanclassDetailPage()
        cls.get = GetAttribute()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ApplyVanclass, self).run(result)

    @testcase
    def test_apply_for_vanclass(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_test_vanclass()  # 班级tab
            if self.van.wait_check_page():  # 页面检查点

                if self.van.empty_tips():  # 暂无数据
                    print('暂无班级')
                else:  # 已有班级
                    print('已有班级:')
                    self.list_swipe_operate()  # 已有班级数 统计

                    for i in range(len(class_data)):
                        if self.van.wait_check_page() and i != len(class_data) - 1:
                            self.apply_vanclass_operate(class_data[i])  # 申请入班 具体操作

                    self.input_remark_name(class_data[-1])  # 班级备注名

                    if self.van.wait_check_page():  # 页面检查点
                        self.home.click_tab_hw()  # 返回主界面
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")

    @teststeps
    def list_swipe_operate(self):
        """班级列表 滑屏 操作"""
        var = self.vanclass_statistic_operate()  # 获取 班级列表信息
        self.van.screen_swipe_up(0.5, 0.8, 0.3, 1000)

        title = [x.text for x in self.van.vanclass_name()]
        last = title[-1]  # 最后一个作业的title

        index = []
        if len(title) < 7:  # 到底部
            if var in title:  #
                if last != var:  # 滑动了
                    # print('滑动后到底部')
                    for i in range(len(title)):
                        if title[i] == var:
                            index.append(i + 1)
                            break
                else:
                    # print('到底了')
                    index.append(len(title))

                self.vanclass_statistic_operate(index[0])  # 获取 班级列表信息
        else:
            # print('滑动后未到底部')
            if var in title:  # 未滑够一页
                # print('未滑够一页')
                for i in range(len(title)):
                    if title[i] == var:
                        index.append(i + 1)
                        break
            else:
                index.append(0)

            return self.list_swipe_operate(index[0])

    @teststeps
    def vanclass_statistic_operate(self, index=0):
        """已有班级数 统计"""
        name = self.van.vanclass_name()  # 班级名称
        num = self.van.vanclass_no()  # 班号
        count = self.van.st_count()  # 学生人数

        last = name[len(num) - 1].text  # 最后一个作业的title
        if len(num) > 6:  # 多于一页
            if len(name) != len(num) != len(count):
                if len(count) != len(name) - 1:
                    if len(count) != len(name) + 1:
                        print('❌❌❌ Error- 班级数、班号数、学生人数有误')
            length = min(len(name), len(num), len(count))
        else:
            if len(name) != len(num) != len(count):
                self.base_assert.except_error('Error- 班级数、班号数、学生人数有误')
            length = len(num)

        print('----------------------')
        for i in range(index, length):
            print(name[i].text, '  ', num[i].text, '  学生人数:', count[i].text)
            if class_data[-1]['class'] in num[i].text:
                num[i].click()
                if self.home.wait_check_tips_page():  # tips弹框 检查点
                    self.home.tips_title()
                    self.home.commit_button()
        return last

    @teststeps
    def apply_vanclass_operate(self, class_datas):
        """申请班级 具体操作"""
        self.van.add_class_button()  # 添加班级 按钮
        if self.home.wait_check_tips_page():  # 页面检查点
            text = self.home.tips_title()  # 修改窗口title

            button = self.home.commit()  # 确定按钮 元素
            if self.get.get_enabled(button) == 'true':
                self.base_assert.except_error('Error- 确定按钮未置灰')

            var = self.home.input()
            var.send_keys(class_datas['class'])
            print(text + ':' + class_datas['class'])

            if class_datas['class'] != '':
                if self.get.get_enabled(button) == 'false':
                    self.base_assert.except_error('Error- 确定按钮未变亮')
                self.home.commit_button()  # 点击确定按钮

                if self.van.wait_check_page():
                    if Toast().find_toast(class_datas['assert']):
                        print(class_datas['assert'])
                        print('-' * 30, '\n')

                elif self.van.wait_check_no_class_page():
                    print('班级不存在 点击屏幕 重新加载')
                    self.home.click_back_up_button()  # 返回
                    print('-' * 30, '\n')
            else:
                self.home.click_blank()

    @teststeps
    def input_remark_name(self, class_datas):
        """输入备注名"""
        for i in range(len(name_data)):
            if self.van.wait_check_page():
                self.apply_vanclass_operate(class_datas)

            if self.van.wait_check_apply_page(5):  # 页面检查点
                if i == 0:
                    ele = self.van.all_element()
                    print(ele[1][1], self.van.class_name_modify())
                    print(ele[1][3], self.van.apply_vanclass_no())
                    print(ele[1][5], self.van.apply_teacher_name())

                remark = self.van.remark_name_modify()  # 备注名
                remark.send_keys(name_data[i]['name'])
                print('填入的备注名是:', name_data[i]['name'])
                print('-'*30, '\n')
                self.van.apply_class_button()          # 申请入班 按钮

                if self.van.wait_check_apply_page():
                    if Toast().find_toast(name_data[i]['assert']):
                        print(name_data[i]['assert'])
                        print('-' * 30, '\n')

                elif self.van.wait_check_page():  # 页面检查点
                    self.home.screen_swipe_up(0.5, 0.8, 0.1, 1000)
                    num = self.van.vanclass_no()[-1].text  # 班号
                    count = self.van.st_count()  # 学生人数

                    if count[-1].text == '申请中':
                        if num[3:] != class_datas['class']:
                            self.base_assert.except_error('Error- 申请班号 信息不符' + num[3:] + '\n')

                        count[-1].click()  # 删除申请信息
                        if self.home.wait_check_tips_page():  # tips弹框 检查点
                            self.home.tips_title()
                            self.home.commit_button()
                            time.sleep(3)
                    else:
                        self.base_assert.except_error('Error- 无申请信息')




