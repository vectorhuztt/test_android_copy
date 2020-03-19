#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.form_sentence_data import form_sentence_operate
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class FormSentence(BasePage):
    """连词成句"""

    def __init__(self):
        self.result = ResultPage()

    @teststeps
    def wait_check_page(self):
        """以“连词成句”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'连词成句')]")
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
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststep
    def question(self):
        """展示的题目"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_prompt").text
        return ele

    @teststep
    def word(self):
        """展示的 待还原的单词"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_word")

        return ele

    # 每小题回答完，下一步按钮后展示答案的页面特有元素
    @teststeps
    def correct_title(self, var):
        """展示的答案 的ID为依据"""
        locator = (By.ID, self.id_type() + "tv_sentence")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def mine_result(self):
        """展示的答题结果"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_word")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        return word

    @teststeps
    def correct_answer(self):
        """点击 下一题 按钮之后展示的答案"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_sentence").text
        word = ele[3:].split(' ')
        return word

    # 查看答案页面
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
    def result_question(self):
        """展示的题目"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "tv_hint")
        return word

    @teststep
    def result_answer(self):
        """展示的 正确答案"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_answer")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        return word

    @teststep
    def result_mine_state(self, index):
        """我的答案对错标识 selected属性"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "iv_mine")[index]
        value = GetAttribute().get_selected(word)
        return value

    @teststep
    def button_swipe(self, from_x, from_y, to_x, to_y, steps=1000):
        """拖动单词button"""
        self.driver.swipe(from_x, from_y, to_x, to_y, steps)

    @teststeps
    def form_sentence_operate(self):
        """《连词成句》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                question = []  # 题目
                count = []  # 做题结果
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 加点击

                    content = self.question()  # 展示的题目
                    value = form_sentence_operate(content).split(' ')  # 数据字典
                    question.append(content)  # return 题目

                    for z in range(len(value) - 1, -1, -1):  # 倒序
                        print(value[z])
                        word = self.word()  # 待还原的单词
                        for k in range(len(word)):
                            if word[k].text == value[z] and k != 0:
                                self.drag_operate(word[k], word[0])  # 拖拽到第一个位置
                                if k == 0:
                                    Homework().next_button_judge('true')  # 下一题 按钮 判断
                                break

                    if not self.correct_title(2):  # 页面检查点
                        Homework().next_button()  # 点击 下一题 按钮

                    if self.correct_title(10):
                        result = self.mine_result()  # 做题结果
                        correct = self.correct_answer()  # 正确答案-- 分解成单词
                        for k in range(len(result)):  # 做错 count+1
                            if correct[k] != result[k]:
                                count.append(k)
                                break

                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                    print('-------------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('===================================================')
                return rate, question, count

    @teststeps
    def drag_operate(self, word2, word):
        """获取 单词button坐标 及拖拽"""
        loc = self.get_element_location(word2)
        y2 = self.get_element_location(word)[1] - 40
        self.button_swipe(loc[0], loc[1], loc[0], y2, 1000)
        time.sleep(1)

    @teststeps
    def check_detail_page(self, i, question, count):
        """查看答案页面"""
        if self.result.wait_check_result_page():
            self.result.check_result_button()  # 查看答案 按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('查看答案：')
                    if int(i) <= 16:
                        self.result_operate(count)
                    else:
                        item = self.result_question()
                        if int(i) % len(item) == 0:
                            page = int(int(i) / len(item))
                        else:
                            page = int(int(i) / len(item)) + 1
                        print('页数:', page)
                        for j in range(page):
                            last_one = self.result_operate(count)  # 滑动前页面内最后一个小题- 题目
                            self.screen_swipe_up(0.5, 0.75, 0.35, 1000)
                            item_2 = self.result_question()  # 滑动后页面内的题目 的数量
                            if item_2[len(item_2) - 1].text == last_one:
                                print('到底啦', last_one)
                                self.result.back_up_button()
                                break
                            elif item_2[len(item_2) - 1].text == question[len(question) - 1]:
                                # 滑动后到底，因为普通情况下最多只有两页，滑动一次即可到底
                                print('滑动后到底', last_one)
                                k = []
                                for i in range(len(item_2) - 1, -1, -1):  # 倒序
                                    if item_2[i].text == last_one:
                                        k.append(i + 1)
                                        break
                                self.result_operate(count, k[0])
                                break
                            else:
                                continue
                        self.screen_swipe_down(0.5, 0.75, 0.35, 1000)
                    time.sleep(2)
                self.result.back_up_button()  # 返回结果页

    @teststeps
    def result_operate(self, var, index=0):
        """查看答案页面 -- 展示的解释内容验证"""
        explain = self.result_question()  # 题目
        answer = self.result_answer()  # 正确答案

        for i in range(index, len(explain)):
            value = form_sentence_operate(explain[i].text)
            if answer[i] != value:  # 测试 正确答案
                print('❌❌❌ 正确答案展示Error:', answer[i], value)
            else:
                if len(var) != 0:  # 存在做错的题
                    if i in var:
                        if self.result_mine_state(i) != 'false':
                            print('❌❌❌ Error - 对错标识:%s' % self.result_mine_state(i))
                        else:
                            print('对错标识:', self.result_mine_state(i))
                    else:
                        if self.result_mine_state(i) != 'true':
                            print('❌❌❌ Error - 对错标识:%s' % self.result_mine_state(i))
                        else:
                            print('对错标识:', self.result_mine_state(i))
                else:
                    if self.result_mine_state(i) != 'true':
                        print('❌❌❌ Error - 对错标识:%s' % self.result_mine_state(i))
                    else:
                        print('对错标识:', self.result_mine_state(i))
            print('-----------------------------')

        return explain[len(explain) - 1].text

    @teststeps
    def study_again(self):
        """《句型转换》 再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()  # 结果页 再练一遍 按钮
            print('再练一遍:')
            result = self.form_sentence_operate()  # 游戏过程
            return '再练一遍按钮', result[0], result[1], result[2]
