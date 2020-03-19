#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import time
import random

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from app.honor.student.homework.object_page.homework_page import Homework
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.get_attribute import GetAttribute


class Listening(BasePage):
    """听后选择"""
    def __init__(self):
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:听力练习”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'听后选择')]")
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
        rate = self.driver \
            .find_element_by_id(self.id_type() + "rate").text
        return rate

    @teststep
    def play_voice(self):
        """播放按钮"""
        horn = self.driver\
            .find_element_by_id(self.id_type() + "fab_audio")
        return horn

    @teststeps
    def red_tips(self):
        """上方红色提示"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_hint")
            return True
        except:
            return False

    @teststeps
    def option_button(self, var):
        """选项"""
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]"
                                    "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout"
                                    "/android.widget.LinearLayout/android.widget.TextView" % var)
        item = []
        content = []
        for i in range(0, len(ele), 2):
            item.append(ele[i])
            content.append(ele[i+1].text)
        return item, content

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststep
    def options(self):
        """选项"""
        answer = self.driver\
            .find_elements_by_id(self.id_type() + "tv_char")
        return answer

    @teststep
    def option_item(self):
        """选项 内容"""
        item = self.driver \
            .find_elements_by_id("com.vanthink.vanthinkteacher.debug:id/tv_item")
        return item

    @teststep
    def questions(self):
        """题目"""
        num = self.driver\
            .find_elements_by_id(self.id_type() + "question")
        return num

    @teststep
    def next_button(self):
        """‘下一题’按钮"""
        time.sleep(1)
        self.driver \
            .find_element_by_id(self.id_type() + "fab_submit") \
            .click()

    @teststep
    def judge_next_button(self):
        """‘下一题’按钮 状态判断"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "fab_submit")  # ‘下一题’按钮
            return True
        except:
            return False

    @teststep
    def next_button_judge(self, var):
        """‘下一题’按钮 状态判断"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "fab_submit")  # ‘下一题’按钮
        value = GetAttribute().get_enabled(item)

        if value != var:  # 测试 下一步 按钮 状态
            print('❌❌❌ 下一步按钮 状态Error', value)

    @teststeps
    def next_button_operate(self, var):
        """下一步按钮 判断 加 点击操作"""
        self.next_button_judge(var)  # 下一题 按钮 状态判断
        self.next_button()  # 点击 下一题 按钮

    @teststeps
    def get_last_element(self):
        """页面内最后一个class name为android.widget.TextView的元素"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        return ele[-1]

    @teststeps
    def get_first_num(self):
        """获取 当前页面第一个题号"""
        item = self.questions()[0].text.split(".")[0]
        return item
    
    @teststep
    def question_judge(self, var):
        """元素 resource-id属性值是否为题目"""
        value = GetAttribute().get_resource_id(var)
        if value == self.id_type() + "question":
            return True
        else:
            return False

    # 查看答案 页面
    @teststeps
    def wait_check_detail_page(self):
        """以“rate”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}rate')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def listen_choice_operate(self):
        """《听后选择》 游戏过程"""
        if self.wait_check_page():  # 页面检查
            if self.wait_check_play_page():
                hint = self.red_tips()  # 顶部红色提示信息
                if not hint:   # 检查是否有红色提示
                    print("----没有红色标识------")

                horn = self.play_voice()
                if not self.get.get_enabled(horn):  # 播放按钮检查
                    print("出现错误：喇叭不可点-------")
                else:
                    horn.click()  # 点击发音按钮
                    retip = self.red_tips()  # 顶部红色提示信息
                    if retip is False:  # 检查红色提示是否消失
                        timestr = []  # 获取每小题的时间
                        rate = int(self.rate())  # 获取待完成数
                        print("作业个数：", rate)
                        self.swipe_operate(int(rate), timestr)

                        while True:  # 由于下一步 按钮会在音频播放完成后可点击
                            if self.judge_next_button():
                                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                                self.next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                                break
                            else:
                                time.sleep(3)

    @teststeps
    def swipe_operate(self, swipe_num, timestr):
        """滑屏 获取所有题目内容"""
        ques_last_index = 0  # 每个页面最后操作过的题号
        index = 0  # 每做一题加一

        if self.wait_check_play_page():
            rate = self.rate()  # 小题数
            for i in range(swipe_num):
                if ques_last_index < swipe_num:
                    ques = self.questions()  # 题目
                    ques_first_index = int(ques[0].text.split(".")[0])  # 页面中第一道题 题号

                    if ques_first_index - ques_last_index > 1:  # 判断页面是否滑过，若当前题比上一页做的题不大于1，则下拉直至题目等于上一题的加1
                        for step in range(0, 10):
                            self.screen_swipe_down(0.5, 0.5, 0.62, 1000)
                            if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                                ques = self.questions()
                                break
                            elif int(self.get_first_num()) < ques_last_index + 1:  # 下拉拉过了
                                self.screen_swipe_up(0.5, 0.6, 0.27, 1000)  # 滑屏
                                if int(self.get_first_num()) == ques_last_index + 1:  # 正好
                                    ques = self.questions()
                                    break

                    last_one = self.get_last_element()  # 页面中最后一个元素

                    if self.question_judge(last_one):  # 判断最后一个元素为题目
                        for j in range(len(ques) - 1):
                            current_index = int(ques[j].text.split(".")[0])
                            if current_index > ques_last_index:
                                self.click_options(rate, index, ques[j].text, timestr)
                                index += 1
                        ques_last_index = int(ques[- 2].text.split(".")[0])
                    else:  # 最后一个元素为选项
                        for k in range(len(ques)):
                            if k < len(ques) - 1:  # 前面的题目照常点击
                                current_index = int(ques[k].text.split(".")[0])
                                if current_index > ques_last_index:
                                    self.click_options(rate, index, ques[k].text, timestr)
                                    index += 1
                                    if k == len(ques) - 2:
                                        ques_last_index = int(ques[-2].text.split(".")[0])
                            elif k == len(ques) - 1:  # 最后一个题目上滑一部分再进行选择
                                self.screen_swipe_up(0.5, 0.76, 0.60, 1000)
                                ques = self.questions()
                                for z in range(len(ques)):
                                    current_index = int(ques[z].text.split(".")[0])
                                    if current_index > ques_last_index:
                                        self.click_options(rate, index, ques[z].text, timestr)
                                        index += 1
                                        ques_last_index = int(ques[z].text.split(".")[0])
                                        break

                    if i != swipe_num - 1:
                        self.screen_swipe_up(0.5, 0.9, 0.27, 1000)  # 滑屏
                else:
                    break

    @teststeps
    def click_options(self, rate, i, questions, timestr):
        """点击选项/判断rate及计时功能"""
        time.sleep(1)
        Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

        options = self.option_button(questions)  # 选项
        print(questions, '\n',
              '选项:', options[1])
        options[0][random.randint(0, len(options[0])) - 1].click()

        timestr.append(self.time())  # 统计每小题的计时控件time信息
        print('-----------------------------------------')
