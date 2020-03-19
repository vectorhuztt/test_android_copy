#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from utils.games_keyboard import Keyboard
from utils.click_bounds import ClickBounds
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class FlashCardPage(BasePage):
    """闪卡练习"""

    def __init__(self):
        self.get = GetAttribute()
        self.key = Keyboard()

    @teststeps
    def wait_check_page(self):
        """以“title:闪卡练习”的ID为依据"""
        locator = (By.XPATH, "//android.widget.ImageView[contains(@resource-id,"
                             "'{}iv_star')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_tip_num(self, num):
        """查看题目数量是否发生改变"""
        locator = (By.XPATH, "//android.widget.ImageView[contains(@text,'{}')]".format(num))
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_star(self):
        """闪卡练习页面内 标星按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "iv_star") \
            .click()

    @teststep
    def click_voice(self):
        """闪卡练习页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def rate(self):
        """获取作业数量"""
        rate = self.driver\
            .find_element_by_id(self.id_type() + "rate").text
        return rate

    # 以下为学习模式 特有元素
    @teststep
    def english_study(self):
        """Word"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_english").text
        return word

    @teststep
    def explain_study(self):
        """翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_chinese").text
        return word

    @teststep
    def pattern_switch(self):
        """闪卡练习页面内  全英/英汉模式切换 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "iv_rotate")\
            .click()
        time.sleep(1)

    # 英汉模式 的例句
    @teststeps
    def wait_check_sentence_page(self, var=20):
        """以“例句”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}sentence')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_explain_page(self, var=20):
        """以“例句解释”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}sentence_explain')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def sentence_study(self):
        """例句"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "sentence").text
        print('例句:', word)

    @teststep
    def sentence_explain_study(self):
        """例句翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "sentence_explain").text
        print('例句解释:', word)

    @teststep
    def sentence_author_study(self):
        """例句 提供老师"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "author").text
        print(word)

    @teststeps
    def click_blank(self):
        """点击空白处"""
        ClickBounds().click_bounds(430, 800)
        print('点击空白处，切换双页面:')
        time.sleep(1)

    # 以下为抄写模式 特有元素
    @teststep
    def word_copy(self):
        """闪卡练习- 抄写模式 内展示的Word"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "tv_word")
        return ele.text

    @teststep
    def english_copy(self):
        """单页面内 答题框填入的Word"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "english").text
        return word

    @teststep
    def explain_copy(self):
        """闪卡练习内展示的翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "chinese").text
        return word

    # 以下为闪卡练习 结果页
    @teststeps
    def wait_check_result_page(self, var=10):
        """以“title:答题报告”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'完成学习')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def finish_study(self):
        """完成学习"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text
        print(ele)
        return ele

    @teststeps
    def study_sum(self):
        """eg: study_sum:6个内容,0标记★;抄写模式"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "study_sum").text
        print(ele)
        return ele

    @teststep
    def study_again_button(self):
        """再练一遍"""
        self.driver \
            .find_element_by_id(self.id_type() + "textView") \
            .click()

    @teststep
    def star_again_button(self):
        """标星内容再练一遍"""
        self.driver \
            .find_element_by_id(self.id_type() + "tv_star_en") \
            .click()

    @teststep
    def star_button(self):
        """五星按钮"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "iv_select")
        return ele

    @teststep
    def voice_button(self, index):
        """语音按钮"""
        self.driver \
            .find_elements_by_id(self.id_type() + "iv_voice")[index] \
            .click()

    @teststep
    def result_word(self):
        """展示的Word"""
        ele = self.driver.find_elements_by_id(self.id_type() + "tv_word")
        return ele

    @teststep
    def result_explain(self):
        """展示的  解释"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "tv_explain")
        return word

    @teststeps
    def study_pattern(self):
        """《闪卡练习 学习模式》 游戏过程"""
        if self.wait_check_page():
            answer = []   # return值 与结果页内容比对
            rate = self.rate()
            for i in range(int(rate)):
                Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                Homework().next_button_judge('true')  # 下一题 按钮 状态判断

                # self.click_voice()  # 听力按钮
                if i in (2, 5):  # 第3、6题  进入全英模式
                    self.pattern_switch()  # 切换到 全英模式
                    print('切换到 全英模式:')
                    if self.wait_check_sentence_page(5):
                        self.sentence_study()  # 例句
                        self.sentence_author_study()  # 例句作者

                    word = self.english_study()  # 单词
                    print('单词:%s' % word)

                    self.pattern_switch()  # 切换到 英汉模式
                else:
                    if self.wait_check_explain_page(5):
                        self.sentence_study()  # 例句
                        self.sentence_explain_study()  # 例句解释
                        self.sentence_author_study()  # 例句作者

                    word = self.english_study()  # 单词
                    explain = self.explain_study()  # 解释
                    print('单词:%s, 解释:%s' % (word, explain))

                answer.append(self.english_study())

                if i in range(1, 9, 2):  # 点击star按钮
                    self.click_star()
                    # if i == 1:
                    #     self.tips_operate()

                if i == 3 and i != int(rate) - 1:  # 第四题 滑屏进入下一题
                    self.screen_swipe_left(0.9, 0.5, 0.1, 1000)
                    time.sleep(1)
                else:
                    if i == int(rate) - 1:  # 最后一题 尝试滑屏进入结果页
                        self.screen_swipe_left(0.9, 0.5, 0.1, 1000)
                        if self.wait_check_result_page(5):
                            print('❌❌❌ Error - 滑动页面进入了结果页')

                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                    time.sleep(1)
                print('-------------------------')
            print('=================================')
            return rate, answer

    @teststeps
    def copy_pattern(self):
        """《闪卡练习 抄写模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            answer = []  # return值 与结果页内容比对
            rate = self.rate()
            for i in range(int(rate)):
                if self.wait_check_page():
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    right_word = self.word_copy()
                    word = list(right_word)  # 展示的Word -- 转化为list形式
                    answer.append(right_word)
                    print("第%s题,单词是:%s" % (i+1, right_word))
                    self.voice_operate(i)  # 听力按钮

                    for j in range(len(word)):
                        print(word[j])
                        if j == 5:
                            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                            self.key.games_keyboard(word[j].upper())  # 点击键盘对应 大写字母
                        else:
                            if j == 6:
                                self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                            self.key.games_keyboard(word[j].lower())  # 点击键盘对应字母
                    print('--------------------------------')
                time.sleep(4)
            print('=================================')
            return rate, answer

    @teststeps
    def voice_operate(self, i):
        """听力按钮 操作"""
        if i == 2:  # 第3题
            j = 0
            print('多次点击发音按钮:')
            while j < 4:
                self.click_voice()  # 多次点击发音按钮
                j += 1
            time.sleep(1)
        else:
            self.click_voice()  # 点击 发音按钮

    @teststeps
    def result_page(self, i, answer):
        """结果页操作"""
        self.finish_study()  # 完成学习
        self.study_sum()  # 学习结果

        word = self.result_word()
        print('判断是否滑动：', i)
        if len(word) <= int(i):
            # self.result_operate(int(i)-1, answer)
            # self.screen_swipe_up(0.5, 0.75, 0.35, 1000)
            self.result_operate(i, answer, int(i))
        else:
            name = word[len(word) - 1].text
            self.result_operate(len(word) - 1, answer)
            self.screen_swipe_up(0.5, 0.75, 0.35, 1000)

            index = self.result_operate_swipe(name)
            for j in range(5):
                if len(index) == 0:
                    self.screen_swipe_down(0.5, 0.75, 0.65, 1000)
                    index = self.result_operate_swipe(name)
                else:
                    break
            word = self.result_word()
            self.result_operate(len(word), answer, index[0])
        print('=================================')

    @teststeps
    def result_operate_swipe(self, name):
        """滑屏操作"""
        index = []
        word = self.result_word()
        for j in range(len(word)):
            if word[j].text == name:
                index.append(j)
                break
        return index

    @teststeps
    def result_operate(self, index, answer, k=0):
        """结果页 具体操作"""
        word = self.result_word()
        for i in range(len(word)):
            print(word[i].text, answer[i])
            if word[i].text != answer[i]:  # 结果页 展示的word与题目中是否一致
                print('❌❌❌ Error 查看答案页 展示的word与题中不一致')

        for index in range(k, int(index), 3):  # 点击 结果页 听力按钮
            self.voice_button(index)  # 结果页 - 听力按钮
            self.star_button()[index].click()  # 结果页 star 按钮

    @teststeps
    def selected_sum(self):
        """标星的数目统计"""
        var = self.star_button()  # 结果页star按钮
        ele = []  # 结果页标星的作业数
        for i in range(len(var)):
            if self.get.get_selected(var[i]) == 'true':
                ele.append(i)

        if len(ele) == 0:  # 结果页标星的作业数为0，则执行以下操作
            print('结果页标星的作业数为0, 点击star按钮:')
            for index in range(0, len(var), 2):
                self.star_button()[index].click()  # 结果页 star 按钮

            ele = []  # 结果页标星的作业数
            for i in range(len(var)):
                if self.get.get_selected(var[i]) == 'true':
                    ele.append(i)

            self.study_sum()  # 学习情况
            print('----------------')

        print('star按钮数目：', len(var))
        print('标星数：', len(ele))
        print('========================')
        return len(ele)
