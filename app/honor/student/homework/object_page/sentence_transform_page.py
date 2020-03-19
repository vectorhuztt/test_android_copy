#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.sentence_transform_data import sentence_transform_operate
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class SentenceTrans(BasePage):
    """句型转换"""
    # 以下为 共有元素
    def __init__(self):
        self.result = ResultPage()

    @teststeps
    def wait_check_page(self):
        """以“句型转换”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'句型转换')]")
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
        rate = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return rate

    @teststep
    def clear_button(self):
        """页面内清除按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "bt_clear").click()

    @teststeps
    def clear_button_judge(self):
        """页面内清除按钮"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "bt_clear")
            return True
        except:
            return False

    @teststep
    def question_content(self):
        """展示的题目 - 句子"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_question").text
        return ele

    @teststeps
    def mine_answer(self):
        """展示的 我的答案"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.RelativeLayout[contains(@index,1)]/descendant::android.widget.TextView")
        words = []
        for i in range(len(ele)):
            words.append(ele[i].text)
        print('我的答案:', words)
        return ele, words

    @teststep
    def word(self):
        """展示的 待还原的单词"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.RelativeLayout[contains(@index,2)]/descendant::android.widget.TextView")

        return ele

    # 每小题回答完，下一步按钮后展示答案的页面
    @teststeps
    def correct_title(self):
        """展示的答案 的ID为依据"""
        locator = (By.ID, self.id_type() + "tv_answer")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def mine_result(self):
        """展示的答题结果"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_text")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        print('我的答题结果:', word)
        return word

    @teststep
    def correct_answer(self):
        """点击 下一题 按钮之后展示的答案"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_answer").text
        word = ele[2:].split(' ')
        return ele, word

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

    @teststeps
    def result_question(self):
        """展示的题目"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_question")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        return word

    @teststeps
    def result_answer(self):
        """展示的 正确答案"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_answer")
        word = []
        for i in range(len(ele)):
            word.append(ele[i].text)
        return word

    @teststeps
    def result_mine(self):
        """我的答案"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_mine")
        words = []
        for i in range(len(ele)):
            words.append(ele[i].text)
        word = words[0].split(' ')
        return words, word

    @teststeps
    def result_mine_state(self, index):
        """我的答案对错标识 selected属性"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "iv_mine")[index]
        value = GetAttribute().get_selected(word)
        return value

    @teststeps
    def sentence_transform(self):
        """《句型转换》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                count = []  # 做题结果
                answer = []
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

                    if not self.clear_button_judge():  # 判断清除按钮存在
                        print('❌❌❌ Error - 清除按钮不存在！！')

                    question = self.question_content()  # 展示的题目内容
                    value = sentence_transform_operate(question).split(' ')
                    self.restore_word(value)  # 填入单词 具体过程
                    var = self.mine_answer()  # 到目前为止我填入的答案

                    if i == 0:
                        print('第%s题 - 点击框中单词，移出框中' % (i + 1))
                        self.remove_word(var)  # 点击框中单词，是否可以移出框中
                    elif i == 1:
                        print('第%s题 - 点击清除按钮' % (i+1))
                        self.clear_button()  # 点击清除按钮
                        self.restore_word(value)  # 填入单词 具体过程
                    print('-------------')
                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击

                    if self.correct_title():  # 页面检查点
                        result = self.mine_result()  # 做题结果
                        correct = self.correct_answer()[1]  # 正确答案-- 分解成单词
                        for k in range(len(result)):  # 做错 count+1
                            if correct[k] != result[k]:
                                count.append(k)
                                break
                        answer.append(result)   # 做题结果

                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                    print('--------------------------------')
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('========================================')
                return rate, answer

    @teststeps
    def restore_word(self, value):
        """填入单词 具体过程"""
        time.sleep(2)
        for j in range(len(value)):
            words = self.word()  # 待还原的单词
            for k in range(len(words)):
                if words[k].text == value[j]:
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 加点击
                    words[k].click()
                    break

    @teststeps
    def remove_word(self, var):
        """点击框中单词，是否可以移出框中"""
        word = []
        for i in range(len(var[0])):
            var[0][i].click()  # 移出框中
            word.append(var[1][i])

        self.restore_word(word)  # 将移出框中的单词重新填入

    @teststeps
    def check_detail_page(self, i, answer):
        """查看答案页面"""
        if self.result.wait_check_result_page():
            print('查看答案页面：')
            self.result.check_result_button()
            if self.result.wait_check_detail_page():
                if self.wait_check_detail_page():
                    if int(i) <= 16:
                        self.result_operate(answer)
                    else:
                        item = self.result_question()
                        if int(i) % len(item) == 0:
                            page = int(int(i) / len(item))
                        else:
                            page = int(int(i) / len(item)) + 1
                        print('页数:', page)
                        for j in range(page):
                            last_one = self.result_operate(answer)  # 滑动前页面内最后一个小题- 做题结果
                            self.screen_swipe_up(0.5, 0.75, 0.35, 1000)
                            item_2 = self.result_question()  # 滑动后页面内的题目 的数量
                            if item_2[len(item_2) - 1].text == last_one:
                                print('到底啦', last_one)
                                self.result.back_up_button()
                                break
                            elif item_2[len(item_2) - 1].text == answer[len(answer) - 1]:
                                # 滑动后到底，因为普通情况下最多只有两页，滑动一次即可到底
                                print('滑动后到底', last_one)
                                k = []
                                for i in range(len(item_2) - 1, -1, -1):  # 倒序
                                    if item_2[i].text == last_one:
                                        k.append(i + 1)
                                        break
                                self.result_operate(answer, k[0])
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
        word = self.result_mine()  # 我的答案
        answer = self.result_answer()  # 正确答案
        for i in range(index, len(explain)):
            count = []
            value = sentence_transform_operate(explain[i]).split(' ')
            if answer[i] == var[i]:  # 测试结果页 我的答案展示是否正确
                if answer[i] == value:  # 测试 正确答案
                    for j in range(len(word[1])):  # 我的答案 与 正确答案 比较
                        if word[1][j] != value[j]:  # 答案不正确 count+1
                            count.append(j)
                            break

                    if count == 0:
                        if self.result_mine_state() != 'true':
                            print('❌❌❌ Error - 我的答案:%s 与 正确答案:%s 对错标识:%s' % (word[0], value, 'false'))
                    else:
                        if self.result_mine_state() != 'false':
                            print('❌❌❌ Error - 我的答案:%s 与 正确答案:%s 对错标识:%s' % (word[0], value, 'true'))
                else:
                    print('❌❌❌ Error - 正确答案:', answer[i], value)
            print('--------------------------------')
        return word[1][len(word[1]) - 1]

    @teststeps
    def study_again(self):
        """《句型转换》 再练一遍 操作过程"""
        print('========================================')
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()  # 结果页 再练一遍 按钮
            print('再练一遍:')
            result = self.sentence_transform()  # 游戏过程
            return '再练一遍按钮', result[0], result[1]
