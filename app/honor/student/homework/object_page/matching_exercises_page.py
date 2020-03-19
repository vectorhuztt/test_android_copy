#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.matching_exercise_data import match_operate
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class MatchingExercises(BasePage):
    """连连看"""
    def __init__(self):
        self.result = ResultPage()

    @teststeps
    def wait_check_page(self):
        """以“title:连连看”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'连连看')]")
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
        rate = self.driver\
            .find_element_by_id(self.id_type() + "time").text
        return rate

    @teststep
    def word(self):
        """展示的Word"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele

    # 以下为答案详情页面元素
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}tv_answer')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def result_voice(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(self.id_type() + "iv_speak")[index] \
            .click()

    @teststep
    def result_answer(self, index):
        """单词"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_answer")[index].text
        return ele

    @teststep
    def result_explain(self, index):
        """解释"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_hint")[index].text
        return ele

    @teststep
    def result_mine(self, index):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "iv_mine")[index]
        value = GetAttribute().get_selected(ele)
        return value

    @teststeps
    def match_exercise(self):
        """《连连看》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                if int(rate) % 5 == 0:
                    page = int(int(rate)/5)
                else:
                    page = int(int(rate) / 5) + 1
                print('页数:', page)
                for j in range(page):  # 然后在不同页面做对应的题目
                    print('第%s页：' % (j+1))
                    word = []  # 单词list
                    word_index = []  # 单词在所有button中的索引
                    explain = []  # 解释list
                    explain_index = []   # 解释在所有button中的索引
                    ele = self.word()  # 所有button
                    for i in range(3, len(ele)):
                        if self.is_alphabet(ele[i].text[0]):  # 如果是字母
                            word.append(ele[i].text)
                            word_index.append(i)
                        else:  # 如果是汉字
                            explain.append(ele[i].text)
                            explain_index.append(i)
                    # print(word_index, study_word, explain, explain_index)

                    for k in range(len(word)):  # 具体操作
                        Homework().rate_judge(rate, k+j*4)  # 测试当前rate值显示是否正确

                        value = match_operate(word[k])  # 数据字典
                        ele[word_index[k]].click()  # 点击解释
                        for z in range(len(explain)):
                            if explain[z] == value:
                                timestr.append(self.time())  # 统计每小题的计时控件time信息
                                ele[explain_index[z]].click()  # 点击对应word
                                #
                                # if k == 1:  # 测试 配对成功后，不可再次点击
                                #     ele[word_index[k]].click()
                                print('--------------------------')
                                break
                    time.sleep(1)
                    print('=================================')
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                return rate

    @teststeps
    def result_detail_page(self, rate):
        """《连连看》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('==============================================')
                    print('查看答案:')
                    self.error_sum(rate)
                    time.sleep(2)

    @teststeps
    def error_sum(self, rate):
        """查看答案 - 点击答错的题 对应的 听力按钮"""
        print('题数:', int(rate))
        for i in range(0, int(rate)):
            print('解释:', self.result_explain(i))  # 解释
            print('单词:', self.result_answer(i))  # 正确word
            mine = self.result_mine(i)  # 对错标识
            if mine != 'true':
                print('❌❌❌ Error - 对错标识')
            else:
                print('对错标识:', mine)
            print('-----------------------------------')

            self.result_voice(i)  # 点击发音按钮
        self.result.back_up_button()  # 返回结果页

    @teststeps
    def study_again(self):
        """再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()  # 结果页 再练一遍 按钮
            print('==============================================')
            print('再练一遍:')
            self.match_exercise()  # 游戏过程
