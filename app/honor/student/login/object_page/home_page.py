#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import time
from app.honor.student.homework.object_page.homework_page import Homework
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.wait_element import WaitElement


class HomePage(BasePage):
    """app主页面元素信息"""
    wait = WaitElement()

    @teststeps
    def wait_check_home_page(self, is_raise=False):
        """以“做试卷”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'做试卷')]")
        return self.wait.wait_check_element(locator, timeout=10)

    @teststeps
    def wait_check_expert_page(self):
        """以“做试卷”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'通知')]")
        return self.wait.wait_check_element(locator)


    @teststeps
    def wait_check_word_title(self):
        """将'单词本'作为 单词本首页 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词本')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def click_hk_tab(self, index):
        """以“口语练习、做单词、做习题、做试卷” 的id"""
        locator = (By.ID, self.id_type() + 'notice')
        self.wait.wait_find_elements(locator)[index-1].click()

    @teststep
    def homework(self):
        """以“口语、作业或者试卷列表内条目”的id为依据"""
        locator = (By.ID, self.id_type() + 'tv_homework_name')
        return self.wait.wait_find_elements(locator)

    @teststeps
    def end_judge(self):
        """元素：到底啦 下拉刷新试试"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'到底啦 下拉刷新试试')]")
        return self.wait.wait_check_element(locator)

    # 关于图书馆的定位
    @teststep
    def wait_check_recommend_more_btn_page(self):
        """推荐栏的发现更多按钮"""
        locator = (By.XPATH, "//*[@text='推荐']/following-sibling::android.widget.TextView")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_mine_more_btn_page(self):
        """推荐栏的发现更多按钮"""
        locator = (By.XPATH, "//*[@text='我的阅读']/following-sibling::android.widget.TextView")
        return self.wait.wait_check_element(locator)

    @teststep
    def check_more(self):
        """查看更多"""
        locator = (By.ID, self.id_type() + 'more')
        return self.wait.wait_find_elements(locator)

    @teststep
    def home_school_name(self):
        """主页学校名称"""
        ele = self.driver.find_element_by_id(self.id_type() + 'common_toolbar')
        ele_child = ele.find_elements_by_xpath('.//android.widget.TextView')
        return ele_child[0].text.split('•')[1]

    @teststep
    def tab_books(self, tab_name):
        """推荐书籍"""
        locator = (By.XPATH, '//*[@text="{}"]/../following-sibling::android.widget.FrameLayout/'
                             'android.widget.LinearLayout/android.widget.LinearLayout'.format(tab_name))
        ele = self.wait.wait_find_elements(locator)
        text = [x.find_element_by_xpath('.//android.widget.TextView').text for x in ele]
        return text

    # 公共元素- 底部四个tab元素：作业、试卷、个人中心、图书馆
    @teststep
    def click_tab_library(self):
        """下方图书馆Tab"""
        locator = (By.ID, self.id_type() + 'tab_lib_icon')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_tab_hw(self):
        """以“学习tab”的id为依据"""
        locator = (By.ID, self.id_type() + 'tab_hw_icon')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_test_vanclass(self):
        """以“班级tab”的id为依据"""
        locator = (By.ID, self.id_type() + 'tab_class_icon')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_tab_profile(self):
        """以“个人中心tab”的id为依据"""
        locator = (By.ID, self.id_type() + 'tab_profile')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_back_up_button(self):
        """以“返回按钮”的class name为依据"""
        locator = (By.ACCESSIBILITY_ID, "转到上一层级")
        self.wait.wait_find_element(locator).click()

    @teststeps
    def all_element(self):
        """页面内所有class name为android.widget.TextView的元素"""
        locator = (By.CLASS_NAME, "android.widget.TextView")
        return self.wait.wait_find_elements(locator)

    # 温馨提示 页面
    @teststeps
    def wait_check_tips_page(self, var=10):
        """以“icon”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@resource-id,"
                   "'{}md_title')]".format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def tips_title(self):
        """温馨提示title"""
        locator = (By.ID, self.id_type() + 'md_title')
        return self.wait.wait_find_element(locator).text

    @teststep
    def tips_content(self):
        """温馨提示 具体内容"""
        locator = (By.ID, self.id_type() + 'md_content')
        return self.wait.wait_find_element(locator).text

    @teststep
    def input(self):
        """输入框"""
        locator = (By.ID, "android:id/input")
        return self.wait.wait_find_element(locator)

    @teststep
    def cancel_button(self):
        """取消 按钮"""
        locator = (By.ID, self.id_type() + "md_buttonDefaultNegative")
        self.wait.wait_find_element(locator).click()

    @teststep
    def commit_button(self):
        """确定 按钮"""
        locator = (By.ID, self.id_type() + "md_buttonDefaultPositive")
        self.wait.wait_find_element(locator).click()

    @teststep
    def commit(self):
        """确定 按钮"""
        locator = (By.ID, self.id_type() + "md_buttonDefaultPositive")
        return self.wait.wait_find_element(locator)

    @teststeps
    def wait_activity(self):
        """获取当前页面activity"""
        self.driver.implicitly_wait(2)
        activity = self.driver.current_activity
        return activity

    @teststeps
    def homework_count(self):
        """获取作业title列表第一个页面的作业 """
        homework_list = self.homework()
        homework_title = [x.text for x in homework_list]  # 获取作业title列表
        return homework_title, homework_list

    @teststeps
    def homework_count_2(self):
        """获取作业title列表非第一页的作业 及 页面内最后一个作业的title 以及 元素 '到底啦 下拉刷新试试' """
        homework_title = []
        homework_list = self.homework()
        for i in range(0, len(homework_list)):
            homework_title.append(homework_list[i].text)  # 获取作业title列表
        # print(len(homework_title), len(homework_list))
        item = homework_list[len(homework_list) - 1].text  # 最后一个作业的title
        tips = self.end_judge()  # 判断元素 '到底啦 下拉刷新试试' 是否存在
        # print('tips:', tips)

        return tips, item, homework_title, homework_list

    @teststeps
    def swipe_operate(self, var, homework, game):
        """滑屏 操作"""
        print('----------------------')
        if len(var) == 10:
            last_one = var[len(var) - 2]  # 滑动前页面内最后一个作业title
        else:
            last_one = var[len(var) - 1]  # 滑动前页面内最后一个作业title
        self.screen_swipe_up(0.5, 0.75, 0.25, 1000)

        item = self.homework_count_2()
        if item[0] is True:  # 滑到底部
            print('滑动后到底部')
            index = []
            for i in range(0, len(item[2])):
                if item[2][i] == last_one:
                    index.append(i)
                    break

            count = self.homework_exist(index[0] + 1, item[2], item[3], homework, game)
            return count
        else:
            # print('滑动后未到底部')
            if last_one in item[2]:
                index_2 = []
                for j in range(0, len(item[2])):
                    if item[2][j] == last_one:
                        index_2.append(j)
                count = self.homework_exist(index_2[0] + 1, item[2], item[3], homework, game)
            else:
                count = self.homework_exist(0, item[2], item[3], homework, game)

            if len(count) == 0:
                return self.swipe_operate(item[2], homework, game)
            else:
                return count

    @teststeps
    def homework_exist(self, index, title, homework, item, game):
        """判断该作业是否存在 -- 若存在，统计小游戏的个数"""
        homework_count = []
        result = []
        for ind in range(index, len(title)):
            if title[ind] == item:
                homework_count.append(ind)
                break
        # print('homework_count:', homework_count)
        if len(homework_count) != 0:
            for i in homework_count:
                homework[i].click()
                result.append(Homework().games_count(0, game, item)[0])
        else:
            print('no have该作业')
        return result

    @teststeps
    def tips_operate_commit(self):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.commit_button()  # 确定按钮
            print('--------------------------')

    @teststeps
    def tips_operate_cancel(self):
        """温馨提示 页面信息  -- 取消"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            print('--------------------------')
            self.tips_title()
            self.tips_content()
            self.cancel_button()  # 取消按钮
            print('--------------------------')

