#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework import guess_word_operate
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep


class GuessWord(BasePage):
    """猜词游戏"""

    @teststeps
    def wait_check_page(self):
        """以“title:猜词游戏”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'猜词游戏')]")
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
    def click_voice(self):
        """页面内音量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def chinese(self):
        """展示的解释"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "chinese").text
        return word

    @teststep
    def english(self):
        """要填写的内容"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "english").text
        word = ele[:-1:2]
        return word

    @teststep
    def keyboard(self):
        """小键盘"""
        ele = self.driver \
            .find_elements_by_class_name("android.widget.TextView")
        keys = ele[6:]
        return keys

    @teststeps
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        print(tpe)
        if tpe == '有发音':
            self.voice_pattern()
        elif tpe == '无发音':
            self.no_voice_pattern()

    @teststeps
    def voice_pattern(self):
        """《猜词游戏 有发音模式》
        -- 由于目前无法处理发音类问题，故以下为测试 每小题六次答题机会 游戏过程 ---"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                answer = []  # 我的答题结果
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    item = []
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                    content = self.chinese()  # 展示的题目内容
                    word = guess_word_operate(content)
                    letters = self.keyboard()  # 小键盘 字母
                    if i == 2:  # todo int(rate)-2需判断int(rate)的值
                        res = self.error_operate(word, letters, item)  # 第2题点击六次错误字母
                        self.judge_error(res[0])  # 本小题所用机会数 判断
                    elif i == int(rate)-2:  # todo int(rate)-2需判断int(rate)的值
                        print('第%s题' % i)
                        var = []
                        res = []
                        for j in range(len(word)):
                            if j == 0:  # 点错一次
                                print('-------------------')
                                print('第%s个字母，点错一次：' % (j+1))
                                var.append(self.error_operate(word, letters, item, j, j+1))
                                res.append(var[0][0])
                            elif j == 2:  # 点错三次
                                print('-------------------')
                                print('第%s个字母，点错三次：' % (j+1), var[0])
                                var_2 = self.error_operate(word, letters, var[0][1], j, j+3)
                                res.append(var_2[0])
                            self.normal_operate(j, word, letters)

                        print('本小题点错次数：', res)
                        res = int(res[0] + res[1])
                        self.judge_error(res)  # 本小题所用机会数 判断
                    else:
                        for k in range(len(word)):
                            self.normal_operate(k, word, letters)

                    # answer.append(self.english())  # 我的答题结果
                    time.sleep(3)
                    print('======================================')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                return answer

    @teststeps
    def no_voice_pattern(self):
        """《猜词游戏 无发音模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确

                    word = self.english()    # 要填写的单词
                    print(word[:-1])
                    content = self.chinese()  # 展示的题目内容
                    value = guess_word_operate(content)  # 对应的word

                    item = value.split(' ')
                    if len(item) != 1:  # 词组
                        var = value.replace(' ', '')   # 删除空格
                        if len(word[:-1]) != len(var):  # 测试空格数是否与单词长度一致
                            print('❌❌❌ Error - 空格数:%s,应为：%s ' % (len(word[:-1]), len(var)))
                        else:
                            print('空格数无误：', len(var))

                    letters = self.keyboard()  # 小键盘 字母
                    for j in range(len(value)):
                        self.normal_operate(j, value, letters)  # 输入单词 具体操作过程

                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    time.sleep(3)
                    print('=====================================')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时

    @teststeps
    def normal_operate(self, j, word, letters):
        """游戏 输入单词 操作过程"""
        if j == 0:  # 第一个字母
            print('第一个字母：', word[j])
            for k in range(len(letters)):
                if letters[k].text == word[j]:
                    letters[k].click()  # 点击键盘对应字母
                    break
        else:  # 第一个字母之外的字母
            if word[j] != '':
                if word[j] not in word[0:j - 1]:
                    for k in range(len(letters)):
                        if letters[k].text == word[j]:
                            print(letters[k].text)
                            letters[k].click()  # 点击键盘对应字母
                            break

    @teststeps
    def error_operate(self, word, letters, item, j=0, end=6):
        """点击错误字母 操作过程"""
        count = end - j  # 点击错误的次数

        while j < end:
            for z in range(j, len(letters)):
                if (letters[z].text not in word) and (letters[z].text not in item):
                    item.append(letters[z].text)
                    j += 1
                    letters[z].click()  # 点击键盘对应字母
                    break
        print('点击错误字母:', item)
        print('-------------------')
        return count, item

    @teststeps
    def judge_error(self, var):
        """机会数 判断"""
        if var <= 6:
            print('No Error - 错误次数为：%s 次' % var)
        else:
            print('❌❌❌ Error - 错误次数为：%s' % var)
            # MyError(self.driver).my_error(var > 6)
        print('==============')
