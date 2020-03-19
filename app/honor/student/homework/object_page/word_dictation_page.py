#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.word_dictation_data import dictation_operate
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard


class WordDictation(BasePage):
    """单词听写"""
    def __init__(self):
        self.result = ResultPage()
        self.key = Keyboard()

    @teststeps
    def wait_check_page(self):
        """以“title:单词听写”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词听写')]")
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
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststeps
    def word(self):
        """展示的Word  点击喇叭听写单词"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        word = ele.replace(' ', '')  # 删除空格
        return word

    # 下一步 按钮之后 答案页展示的答案
    @teststeps
    def mine_answer(self):
        """展示的Word """
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        word = ele.replace(' ', '')  # 删除空格
        return word

    @teststep
    def question(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return word

    @teststeps
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_answer").text
        print('正确答案：', word)
        return word

    @teststep
    def correct_judge(self):
        """判断 答案是否展示"""
        ele = self.find_element(self.id_type() + "tv_answer")
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
            .find_elements_by_id(self.id_type() + "iv_mine")[index].get_attribute("selected")
        return ele

    @teststeps
    def word_dictation(self):
        """《单词听写》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                count = []
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断 加点击

                    self.word()  # 灰字文案：点击喇叭听写单词
                    self.click_voice()  # 点击喇叭

                    word = dictation_operate(i)  # 数据字典
                    if self.is_alphabet(word):  # 解释内容为word
                        for j in range(0, len(word)):
                            self.keyboard_operate(j, word[j])  # 点击键盘 具体操作

                    answer.append(self.word())  # 我的答案
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击

                    self.result_operate(answer, count, i, timestr, self.mine_answer())  # 下一步按钮后的答案页面 测试
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                    print('--------------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==============================================')
                return rate, answer

    @teststeps
    def keyboard_operate(self, j, value):
        """点击键盘 具体操作"""
        if j == 4:
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.key.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.key.games_keyboard(value)  # 点击键盘对应字母
        Homework().next_button_judge('true')  # 测试 下一步 按钮的状态

    @teststeps
    def result_operate(self, answer, count, i, timestr, mine):
        """下一步按钮后的答案页面"""
        # mine 为 答案页面展示的 我的答题结果
        result = answer[len(answer) - 1]
        print('我的答案:', result)
        print('我的答题结果：', mine)
        if self.correct_judge():  # 展示的答案元素存在说明回答错误
            correct = self.correct()  # 正确答案
            if mine.lower() != result.lower():  # 展示的答题结果与我填入的答案不一致
                print('❌❌❌ Error - 展示的答题结果:%s 与我填入的答案:%s 不一致' % (mine, result))

            for k in range(len(correct)):  # 测试 答案判断是否正确
                if result[k] not in correct:
                    count.append(i)  # 做错的题目
                    break
        else:  # 回答正确
            if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                print('❌❌❌ Error - 展示的答题结果 与我填入的不一致:', mine, result)

        if i == 1:  # 第2题
            j = 0
            print('多次点击发音按钮:')
            while j < 4:
                print(j)
                self.click_voice()  # 多次点击发音按钮
                j += 1
            time.sleep(1)
        else:
            self.click_voice()  # 点击 发音按钮
        timestr.append(self.time())  # 统计每小题的计时控件time信息

    @teststeps
    def result_detail_page(self, rate):
        """《单词听写》 查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    print('查看答案:')
                    print('题数:', int(rate))
                    for i in range(int(rate)):
                        print('-----------------------------------')
                        print('解释:', self.result_explain(i))  # 解释
                        print('单词:', self.result_answer(i))  # 正确word
                        print('对错标识:', self.result_mine(i))  # 对错标识
                        self.result_voice(i)  # 点击发音按钮
                    self.result.back_up_button()  # 返回结果页
                    time.sleep(2)
            print('==============================================')

    @teststeps
    def study_again(self):
        """再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()  # 结果页 再练一遍 按钮
            print('再练一遍:')
            self.word_dictation()  # 游戏过程
