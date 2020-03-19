#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.strength_sentence_data import strength_sentence_operate
from utils.click_bounds import ClickBounds
from utils.games_keyboard import Keyboard
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class StrengthenSentence(BasePage):
    """强化炼句"""
    def __init__(self):
        self.bounds = ClickBounds()
        self.result = ResultPage()
        self.key = Keyboard()
        self.get = GetAttribute()

    # 以下为 共有元素
    @teststeps
    def wait_check_page(self):
        """以“title:强化炼句”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'强化炼句')]")
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
    def content_value(self):
        """获取整个 外框元素"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "input2")
        return ele

    @teststeps
    def content_desc(self):
        """点击输入框，激活小键盘"""
        content = self.get.get_description(self.content_value())
        item_x = re.match(".*\[(.*)\].*\[", content)  # x值
        item_y = re.match(".*\[(.*)\].*", content)  # y值
        x = item_x.group(1).split(',')  # 所有输入框y值的列表
        y = item_y.group(1).split(',')  # 所有输入框x值的列表
        return x, y

    @teststeps
    def get_result(self):
        """点击输入框，激活小键盘"""
        content = self.get.get_description(self.content_value())
        value = re.match("\\[(.+?)\\]", content)  # answer
        answer = value.group(1).split(',')  # 所有输入框值的列表
        return answer

    @teststep
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststeps
    def sentence(self):
        """展示的句子"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "input2").text
        return word

    @teststep
    def explain(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "explain").text
        return word

    # 每小题回答完，下一步按钮后展示答案的页面
    @teststeps
    def correct_title(self):
        """展示的答案title:正确答案 的ID为依据"""
        locator = (By.ID, self.id_type() + "correct_title")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "correct").text
        ele = word[:-1]  # 去掉最后的标点符号
        return ele

    # 查看答案页面
    @teststeps
    def result_question(self):
        """展示的题目"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_hint")
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

    @teststep
    def result_mine_state(self, index):
        """我的答案对错标识 selected属性"""
        word = self.driver \
            .find_elements_by_id(self.id_type() + "iv_mine")[index].get_attribute('selected')
        return word

    @teststeps
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        print(tpe)
        if tpe == '默写模式':
            answer = self.dictation_pattern()
        elif tpe == '自定义模式':
            answer = self.custom_pattern()
        elif tpe == '简单模式':
            answer = self.easy_pattern()
        else:  # 复杂模式
            answer = self.random_pattern()
        return answer

    @teststeps
    def random_pattern(self):
        """《强化炼句 复杂模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断加 点击操作 ,进入答案页面

                    self.correct_judge(value, i)  # 判断答题是否正确
                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断加 点击操作
                    print('-------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('======================================================')
                return rate, answer

    @teststeps
    def custom_pattern(self):
        """《强化炼句 自定义模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 点击

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 点击
                    if self.correct_title():
                        result = self.correct_judge(value, i)  # 判断答题是否正确
                        answer.append(result[0])

                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 点击
                    print('-------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('======================================================')
                return rate, answer

    @teststeps
    def easy_pattern(self):
        """《强化炼句 简单模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 点击

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 点击，进入答案页面

                    result = self.correct_judge(value, i)  # 判断答题是否正确
                    answer.append(result[0])
                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 点击
                    print('-------------------------------')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('======================================================')
                return rate, answer

    @teststeps
    def dictation_pattern(self):
        """《强化炼句 默写模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                answer = []
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 点击

                    value = self.input_text()  # 激活输入框并进行输入
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 点击，进入答案页面

                    result = self.correct_judge(value, i)  # 判断答题是否正确
                    answer.append(result[0])
                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 点击
                    print('-----------------------------')
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==================================================')
                return rate, answer

    @teststeps
    def input_text(self):
        """激活输入框 并 输入内容"""
        explain = self.explain()  # 解释的内容
        sentence = self.sentence().split(' ')  # 句子
        print('题目:', self.sentence())
        value = strength_sentence_operate(explain)  # 数据字典

        words = value.split(' ')  # 将句子分割成单词
        word = []
        for i in range(len(words)):
            if (self.is_alphabet(words[i])) and (words[i] not in sentence):
                word.append(words[i])

        for j in range(len(word)):
            item = self.content_desc()  # 获取输入框坐标
            loc = self.get_element_location(self.content_value())  # 文章元素左上角 顶点坐标
            x = float(item[0][j]) + loc[0]+55.0  # 55.0为点击输入框中心点的偏移量
            y = float(item[1][j]) + loc[1]
            self.driver.tap([(x, y)])  # 点击激活输入框

            for z in range(len(word[j])):
                if j == len(word)-1:
                    if word[j][z] in ['.', '?', '!']:  # 去掉最后的标点符号
                        break
                if z == 4 and z != len(word[j])-1:
                    self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                    self.key.games_keyboard(word[j][z].upper())  # 点击键盘对应 大写字母
                    self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                else:
                    if j == 2 and word[j][z] == "'":
                        self.key.games_keyboard(',')  # 第二小题  点击键盘 逗号
                    else:
                        self.key.games_keyboard(word[j][z])  # 点击键盘对应字母

        return value

    @teststeps
    def correct_judge(self, value, i):
        """每小题回答完，下一步按钮后展示答案的页面"""
        if self.correct_title():  # 展示的答案title元素是否存在
            result = self.get_result()  # content-desc的值
            answer = self.sentence()  # 展示的本人的答案

            for j in range(len(result)):
                for k in range(len(answer)):
                    if answer[k] == '{':
                        if len(answer) != 2:
                            if k == 0:  # 展示的本人的答案 result[j]
                                answer = result[j].strip() + answer[k + 2:]
                            elif k + 1 == len(answer) - 1:
                                if ' ' not in result[j]:
                                    answer = answer[:k - 1] + ' ' + result[j]
                                else:
                                    answer = answer[:k - 1] + result[j]
                            else:
                                if ' ' not in result[j]:
                                    answer = answer[:k - 1] + ' ' + result[j] + answer[k + 2:]
                                else:
                                    answer = answer[:k - 1] + result[j] + answer[k + 2:]
                            break

            if answer[len(answer)-1] == ' ':
                answer = answer[:-1]
            correct = self.correct()  # 展示的正确答案
            print('我的答案：', answer)
            if correct == value:  # 测试展示的答案是否正确
                if answer == correct:
                    print('回答正确')
                else:
                    print('回答错误')
            return answer, i

    @teststeps
    def study_again(self, tpe):
        """《强化炼句》 再练一遍 操作过程"""
        print('再练一遍 操作过程:')
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()  # 结果页 再练一遍 按钮
            result = self.diff_type(tpe)  # 强化炼句 - 游戏过程

            return '再练一遍按钮', result[0], result[1]

    @teststeps
    def check_detail_page(self, i, answer):
        """查看答案页面"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('结果页 - 查看答案 按钮：')
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
            self.result.back_up_button()

    @teststeps
    def result_operate(self, var, index=0):
        """查看答案页面 -- 展示的解释内容验证"""
        explain = self.result_question()  # 题目
        answer = self.result_answer()  # 正确答案
        print(answer, var)
        for i in range(index, len(explain)):
            count = []
            value = strength_sentence_operate(explain[i]).split(' ')
            if answer[i] == var[i]:  # 测试结果页 我的答案展示是否正确
                if answer[i] == value:  # 测试 正确答案
                    for j in range(len(var)):  # 我的答案 与 正确答案 比较
                        if var[j] != value[j]:  # 答案不正确 count+1
                            count.append(j)
                            if self.result_mine_state() != 'false':
                                print('❌❌❌ Error - 我的答案:%s 与 正确答案:%s 对错标识:%s' % (var[j], value[j], 'true'))
                        else:
                            if self.result_mine_state() != 'true':
                                print('❌❌❌ Error - 我的答案:%s 与 正确答案:%s 对错标识:%s' % (var[j], value[j], 'false'))
                        break
                else:
                    print('❌❌❌ Error - 正确答案:', answer[i], value)
            print('------------------------------------')
        return var[1][len(var[1]) - 1]

