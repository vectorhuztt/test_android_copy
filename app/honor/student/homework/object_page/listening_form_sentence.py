#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import time
from math import ceil, floor

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from app.honor.student.homework.object_page.homework_page import Homework
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep

import random


class ListenFormCent(BasePage):

    @teststeps
    def wait_check_page(self):
        """以“title:听力练习”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'听音连句')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def answer_page_check(self):
        """以“查看答案的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'查看答案)]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def rate(self):
        """获取作业数量"""
        rate = self.driver \
            .find_element_by_id(self.id_type() + "rate").text
        return rate

    @teststeps
    def play_voice(self):
        self.driver.find_element_by_id(self.id_type() + "fab_audio").click()

    @teststeps
    def question_num(self):
        """题目内容"""
        num = self.driver \
            .find_elements_by_id(self.id_type() + "question")
        return num

    @teststep
    def option_button(self, var):
        """选项"""
        print(var)
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[@text=  "
                                    "'%s']/following-sibling::android.widget.LinearLayout/"
                                    "android.widget.LinearLayout/android.widget"
                                    ".LinearLayout/android.widget.TextView" % var)
        item = []
        for i in range(0, len(ele), 2):
            item.append(ele[i])
        print('选项个数:', len(item))
        return item

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststeps
    def next_button_operate(self, var):
        """下一步按钮 判断 加 点击操作"""
        self.next_button_judge(var)  # 下一题 按钮 状态判断
        self.next_button()  # 点击 下一题 按钮

    @teststep
    def next_button_judge(self,var):
        item = self.driver.find_element_by_id(self.id_type() + "fab_submit").get_attribute("enabled")  # ‘下一题’按钮
        if item != var:  # 测试 下一步 按钮 状态
            print('❌❌❌ 下一步按钮 状态Error', item)

    @teststep
    def next_button(self):
        """‘下一题’按钮"""
        time.sleep(1)
        self.driver \
            .find_element_by_id(self.id_type() + "fab_submit") \
            .click()

    @teststep
    def answer_check_button(self):
        self.driver.find_element_by_id(self.id_type() + "detail").click()

    @teststep
    def answer_voice_play(self):
        self.driver.find_element_by_id(self.id_type() + "iv_play").click()

    @teststep
    def get_question_num(self):
        num = self.driver.find_elements_by_id(self.id_type() + "question")
        return num

    @teststep
    def play_again_button(self):
        self.driver.find_element_by_id(self.id_type() + "again").click()
        self.listen_formcentence()

    @teststep
    def listen_formcentence(self):
        if self.wait_check_page():
            timestr = []  # 获取每小题的时间
            tipsum = self.rate()  #获取待完成数
            print("作业个数：",tipsum)
            self.play_voice()

            itr = ceil(int(tipsum)/3)
            for j in range(0,int(itr)):
                    num = self.question_num()
                    rate = self.rate()
                    for i in range(0,len(num)):
                        if i < 3:
                            Homework().rate_judge(rate, i, self.rate())  # 测试当前rate值显示是否正确
                            content = num[i].text
                            options = self.option_button(content)
                            options[random.randint(0, len(options)) - 1].click()
                            time.sleep(1)
                            timestr.append(self.time())  # 统计每小题的计时控件time信息
                            print('---------------------------')
                        else:
                            continue
                    if  int(self.rate()) > 1:
                        self.screen_swipe_up(0.5, 0.97, 0.02, 1000)
                        time.sleep(2)
            self.next_button_operate('true')  # 下一题 按钮 状态判断 加点击
            Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时

            self.answer_check_button()    #点击查看答案按钮
            print("点击查看答案-------")
            if self.answer_page_check:
                print("进入查看答案界面-----")
                time.sleep(1)
                print("点击播放按钮---------")
                self.answer_voice_play()
                questions_num = len(self.get_question_num())
                items = floor(questions_num/3)
                for i in range(0,int(items)):
                    if items > 0:
                        time.sleep(2)
                        self.screen_swipe_up(0.5, 0.97, 0.02, 1000)
                    else:
                        continue



