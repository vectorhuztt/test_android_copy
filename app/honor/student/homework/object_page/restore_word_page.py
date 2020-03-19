#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.restore_word_data import restore_word_operate
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class RestoreWord(BasePage):
    """还原单词"""

    def __init__(self):
        self.result = ResultPage()

    @teststeps
    def wait_check_page(self):
        """以“还原单词”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'还原单词')]")
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
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "fab_sound") \
            .click()
        time.sleep(1)

    @teststep
    def prompt(self):
        """展示的提示词"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_prompt").text
        return ele

    @teststep
    def word(self):
        """展示的 待还原的单词"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "tv_word")

        return word

    # 查看答案页面
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def answer(self):
        """展示的提示词"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "tv_answer")
        return word

    @teststep
    def hint(self):
        """展示的 解释"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "tv_hint")
        return word

    @teststep
    def voice_button(self, index):
        """页面内音量按钮"""
        self.driver \
            .find_elements_by_id(self.id_type() + "iv_speak")[index] \
            .click()

    @teststep
    def result_mine(self, index):
        """我的"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "iv_mine")[index]
        value = GetAttribute().get_selected(ele)
        return value

    @teststep
    def button_swipe(self, from_x, from_y, to_x, to_y, steps=1000):
        """拖动单词button"""
        self.driver.swipe(from_x, from_y, to_x, to_y, steps)

    @teststeps
    def restore_word(self):
        """《还原单词》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                timestr = []  # 获取每小题的时间
                answer = []
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    self.voice_operate(i)  # 听力按钮

                    explain = self.prompt()  # 展示的提示词
                    value = restore_word_operate(explain)
                    word = self.word()  # 展示的单词
                    if value == 'aa':
                        self.drag_operate(word[1], word[0])  # 拖拽到第一个位置
                    else:
                        for z in range(len(value) - 1, -1, -1):  # 倒序
                            words = self.word()
                            for k in range(len(words)):
                                letter = words[k].text
                                if letter[0] == value[z] and k != 0:
                                    self.drag_operate(words[k], words[0])  # 拖拽到第一个位置
                                    break

                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                    var = self.word()  # 元素 tv_word
                    # if int(self.rate())+1 == int(rate) - i and len(var) == len(study_word)+1:  # todo 判断 是否进入答案页
                    text = []  # 元素 tv_word的text
                    for z in range(len(var)):
                        text.append(var[z].text)
                    print('我的答案:', text[1:])
                    print('正确答案：', text[0])

                    if i != int(rate)-1:
                        Homework().next_button_operate('true')  # 下一题 按钮 判断

                    answer.append(text[0])
                    print('----------------------------------------')
                    time.sleep(2)

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('===========================================')
                return rate, answer

    @teststeps
    def drag_operate(self, word2, word):
        """获取单词button坐标 及拖拽"""
        loc = self.get_element_location(word2)
        y2 = self.get_element_location(word)[1] - 40
        self.button_swipe(loc[0], loc[1], loc[0], y2, 1000)
        time.sleep(1)

    @teststeps
    def voice_operate(self, i):
        """听力按钮 操作"""
        if i == 2:  # 第3题
            j = 0
            print('多次点击发音按钮:')
            while j < 4:
                print(j)
                self.click_voice()  # 多次点击发音按钮
                j += 1
            time.sleep(1)
        else:
            self.click_voice()  # 点击 发音按钮

    @teststeps
    def check_detail_page(self, i, answer):
        """查看答案页面"""
        if self.result.wait_check_result_page():
            print('查看答案页面:')
            self.result.check_result_button()  # 点击查看答案按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('判断是否滑动：', i)
                    if int(i) <= 16:
                        self.result_operate()
                    else:
                        item = self.hint()
                        if int(i) % len(item) == 0:
                            page = int(int(i) / len(item))
                        else:
                            page = int(int(i) / len(item)) + 1
                        print('页数:', page)
                        for j in range(page):
                            last_one = self.result_operate()  # 滑动前页面内最后一个小游戏title
                            self.screen_swipe_up(0.5, 0.75, 0.35, 1000)
                            item_2 = self.hint()  # 滑动后页面内的解释 的数量
                            if item_2[len(item_2) - 1].text == last_one:
                                print('到底啦', last_one)
                                self.result.back_up_button()
                                break
                            elif item_2[len(item_2) - 1].text == answer[len(answer)-1]:
                                # 滑动后到底，因为普通情况下最多只有两页，滑动一次即可到底
                                print('滑动后到底', last_one)
                                k = []
                                for i in range(len(item_2) - 1, -1, -1):  # 倒序
                                    if item_2[i].text == last_one:
                                        k.append(i+1)
                                        break
                                self.result_operate(k[0])
                                break
                            else:
                                continue
                        self.screen_swipe_down(0.5, 0.75, 0.35, 1000)
                    self.result.back_up_button()  # 返回结果页
                    time.sleep(2)

    @teststeps
    def result_operate(self, index=0):
        """查看答案页面 -- 展示的解释内容验证"""
        explain = self.hint()  # 解释
        word = self.answer()  # 题目
        for i in range(index, len(explain)):
            key = explain[i].text
            value = restore_word_operate(key)
            if word[i].text == value:
                print('对错标识:', self.result_mine(i))  # 对错标识
                self.voice_button(i)  # 结果页 - 听力按钮
            else:
                print('❌❌❌ Error -解释内容与题中不一致:', key, word[i].text, value)
            print('----------------------------------')
        return explain[-1].text
