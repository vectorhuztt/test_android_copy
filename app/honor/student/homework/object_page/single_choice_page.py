#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class SingleChoice(BasePage):
    """单项选择"""
    def __init__(self):
        self.result = ResultPage()

    @teststeps
    def wait_check_page(self):
        """以“title:单项选择”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单项选择')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_play_page(self):
        """以“rate”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}rate')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def rate(self):
        """获取作业数量"""
        rate = self.driver\
            .find_element_by_id(self.id_type() + "rate").text
        return rate

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststep
    def question_content(self):
        """获取题目内容"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "question").text
        return ele

    @teststep
    def option_button(self):
        """获取所有选项 - 四个选项"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_char")
        return ele

    @teststeps
    def option_selected(self, index):
        """获取所有选项 - 四个选项selected属性"""
        time.sleep(1)
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_char")[index]
        value = GetAttribute().get_selected(ele)
        return value

    @teststep
    def option_content(self, index):
        """获取所有选项 - 四个选项内容"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_char")[index].text
        return ele

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             + self.id_type() + "tv_answer)]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def single_choice_operate(self):
        """《单项选择》 游戏过程   返回当前大题的题数，正确数，正确题目内容， 最终完成时间"""
        if self.wait_check_page():
            if self.wait_check_play_page():
                count = 0
                timestr = []  # 获取每小题的时间
                questions = []  # 答对的题
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    item = self.question_content()  # 题目
                    print('题目:', item)
                    options = self.option_button()  # 四个选项
                    options[random.randint(0, len(options)-1)].click()  # 随机点击选项

                    ele = []  # 四个选项selected属性值为true的个数
                    for j in range(len(options)):  # 统计答案正确与否
                        if self.option_selected(j) == 'true':
                            ele.append(j)

                    if len(ele) == 1:  # 如果选项的selected属性为true的作业数为1,说明答对了，则+1
                        index = ele[0]
                        print('回答正确:', self.option_content(index))
                        questions.append(self.question_content())
                        count += 1
                    else:
                        print('回答错误:', ele)

                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                    print('--------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                final_time = ResultPage().get_time(timestr[len(timestr)-1])  # 最后一个小题的时间
                print('=======================================')
                return rate, count, questions, final_time

    @teststeps
    def check_detail_page(self):
        """《单项选择》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('查看答案页面:')
                for i in range(2):
                    self.screen_swipe_up(0.5, 0.75, 0.25, 1000)
                    self.screen_swipe_down(0.5, 0.25, 0.75, 1000)
                self.result.back_up_button()  # 返回结果页

    @teststeps
    def study_again(self):
        """《单项选择》 错题再练 操作过程"""
        print('==================================================')
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.error_again_button()  # 结果页 错题再练 按钮
            print('错题再练:')
            result = self.single_choice_operate()  # 单项选择 - 游戏过程
            return '错题再练按钮', result[0], result[2], result[3]
