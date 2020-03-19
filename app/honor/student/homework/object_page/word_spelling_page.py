#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from app.honor.student.homework.test_data.word_spelling_data import word_spelling_operate
from utils.get_attribute import GetAttribute
from utils.games_keyboard import Keyboard
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class WordSpelling(BasePage):
    """单词拼写"""
    def __init__(self):
        self.result = ResultPage()
        self.get = GetAttribute()
        self.key = Keyboard()

    # 以下为 共有元素
    @teststeps
    def wait_check_page(self):
        """以“title:单词拼写”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词拼写')]")
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
        """页面内喇叭量按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststeps
    def word(self):
        """展示的Word"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        word = ele[1::2]
        print('study_word：', word)
        return word

    @teststep
    def explain(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return word

    @teststep
    def finish_word(self):
        """完成答题 之后 展示的Word 前后含额外字符：aa"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        return word[1::2]

    # 默写模式 特有元素
    @teststeps
    def dictation_word(self):
        """展示的Word"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        value = ele[::2]
        return value

    @teststeps
    def dictation_word_judge(self):
        """判断是否展示Word"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "tv_word")
            return True
        except Exception:
            return False

    @teststep
    def under_line(self):
        """展示的横线"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "underline")
        return ele

    @teststep
    def hint_button(self):
        """提示按钮"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "hint")
        return ele

    # 下一步 按钮之后 答案页展示的答案
    @teststep
    def mine_answer(self):
        """展示的Word  前后含额外字符:aa"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        return word[1::2]

    @teststep
    def question(self):
        """展示的翻译"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return word

    @teststep
    def correct(self):
        """展示的答案"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_answer").text
        return word

    @teststeps
    def correct_judge(self):
        """判断 答案是否展示"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "tv_answer")
            return True
        except Exception:
            return False

    # 默写模式 答案页特有元素
    @teststep
    def dictation_finish_word(self):
        """完成答题 之后 展示的Word  前后不含额外字符:aa"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        return word[::2]

    @teststep
    def dictation_mine_answer(self):
        """展示的Word  前后不含额外字符:aa"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "tv_word").text
        return word[::2]

    # 以下为答案详情页面元素
    @teststeps
    def wait_check_detail_page(self):
        """以“answer”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             + self.id_type() + "tv_answer)]")
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
        value = self.get.get_selected(ele)
        return value

    @teststeps
    def diff_type(self, tpe):
        """选择 不同模式小游戏的 游戏方法"""
        print(tpe)
        time.sleep(2)
        if tpe == '默写模式':
            answer = self.dictation_pattern()
        elif tpe == '自定义':
            answer = self.custom_pattern()
        else:  # 随机模式
            answer = self.random_pattern()
        return answer

    @teststeps
    def random_pattern(self):
        """《单词拼写 随机模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                var = []  # 随机消除的字母
                count = []   # 做错的题目
                answer = []   # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间

                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    explain = self.explain()  # 解释
                    word = self.word()  # 未缺失的字母
                    value = word_spelling_operate(explain)  # 数据字典

                    item = word.replace('_', '')
                    if self.is_alphabet(item):  # 未缺失的内容为字母
                        if value != word:  # 随机消除的字母消除了
                            for j in range(len(value)):
                                if value[j] != word[j]:
                                    print('缺失的字母：', value[j])
                                    var.append(j)
                                    self.keyboard_operate(j, value[j])  # 点击键盘 具体操作

                    answer.append(self.finish_word())  # 我的答案
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断加 点击操作

                    self.result_operate(answer, count, i, timestr, self.mine_answer())  # 下一步按钮后的答案页面 测试
                    Homework().next_button_operate('true')  # 下一题 按钮 判断加 点击操作
                    print('======================================')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                return rate, answer, var

    @teststeps
    def custom_pattern(self):
        """《单词拼写 自定义模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                count = []  # 做错的题目
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    explain = self.explain()  # 解释
                    word = self.word()  # 未缺失的字母
                    value = word_spelling_operate(explain)  # 数据字典

                    item = word.replace('_', '')
                    if self.is_alphabet(item):  # 未缺失的内容为字母
                        if len(word) != 0:
                            if value != word:  # 自定义消除的字母消除了
                                for j in range(len(value)):
                                    if value[j] != word[j]:
                                        print('缺失的字母：', value[j])
                                        self.keyboard_operate(j, value[j])  # 点击键盘 具体操作
                            else:
                                print('❌❌❌ Error - 自定义消除的字母未消除', word)
                                for j in range(0, len(value)-1):
                                    if value[j] != word[j]:
                                        print('❌❌❌ Error - 未自定义消除的字母%s也消除了' % value[j])

                    answer.append(self.finish_word())  # 我的答案
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击

                    self.result_operate(answer, count, i, timestr, self.mine_answer())  # 下一步按钮后的答案页面 测试
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击

                    print('======================================')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                return rate, answer

    @teststeps
    def dictation_pattern(self):
        """《单词拼写 默写模式》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                count = []
                answer = []  # return值 与结果页内容比对
                timestr = []  # 获取每小题的时间
                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断 加点击

                    explain = self.explain()  # 解释
                    value = word_spelling_operate(explain)  # 数据字典

                    if self.dictation_word_judge():  # 默写模式 - 字母未全部消除
                        print('❌❌❌ Error - 单词拼写 默写模式 - 字母未全部消除')

                    if i in range(2, 5, 2):
                        hint = self.hint_button()  # 提示按钮
                        if self.get.get_enabled(hint) == 'true':
                            hint.click()  # 点击 提示按钮
                            if self.get.get_enabled(hint) != 'false':
                                print('❌❌❌ Error - 点击后提示按钮enabled属性为:', self.get.get_enabled(hint))

                            if self.dictation_word_judge():  # 出现首字母提示
                                word = self.dictation_word()
                                if len(word) == 1 and word == value[0]:
                                    print('点击提示出现首字母提示', word)
                                else:
                                    print('❌❌❌ Error - 点击提示未出现首字母提示')
                        else:
                            print('❌❌❌ Error - 提示按钮enabled属性为:', self.get.get_enabled(hint))

                    for j in range(len(value)):
                        self.keyboard_operate(j, value[j])  # 点击键盘 具体操作

                    answer.append(self.dictation_finish_word())  # 我的答案
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击

                    self.result_operate(answer, count, i, timestr, self.dictation_mine_answer())  # 下一步按钮后的答案页面 测试
                    Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                    print('======================================')

                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
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

    @teststeps
    def result_operate(self, answer, count, i, timestr, mine):
        """下一步按钮后的答案页面"""
        # mine 为 答案页面展示的 我的答题结果
        print('----------------------')
        result = answer[len(answer) - 1]
        print('我的答案:', result)
        print('我的答题结果:', mine)
        if self.correct_judge():  # 展示的答案元素存在说明回答错误
            correct = self.correct()  # 正确答案
            if len(mine) <= len(correct):  # 输入少于或等于单词字母数的字符
                if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('Error - 字符数少于或等于时:', mine.lower(), result.lower())
            else:  # 输入过多的字符
                if correct + mine[len(correct):].lower() != correct + result[
                                                                      len(correct):].lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('Error - 字符输入过多时:', correct + mine[len(correct):].lower(),
                          correct + result[len(correct):].lower())

            for k in range(len(correct)):  # 测试 答案判断是否正确
                if result[k] not in correct:
                    count.append(i)  # 做错的题目
                    break
        else:  # 回答正确
            if mine.lower() != result.lower():  # 展示的 我的答题结果 是否与我填入的一致
                print('Error - 展示的答题结果 与我填入的不一致:', mine.lower(), result.lower())

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
        """查看答案 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮
            if self.result.wait_check_detail_page():
                print('======================================')
                print('查看答案:')
                self.error_sum(rate)
                time.sleep(2)
            print('==============================================')

    @teststeps
    def error_sum(self, rate):
        """查看答案 - 点击答错的题 对应的 听力按钮"""
        print('题数:', int(rate))
        for i in range(0, int(rate)):
            print('解释:', self.result_explain(i))  # 解释
            print('单词:', self.result_answer(i))  # 正确word
            print('对错标识:', self.result_mine(i))  # 对错标识
            print('-----------------------------------')
            self.result_voice(i)  # 点击发音按钮
        self.result.back_up_button()  # 返回结果页

    @teststeps
    def study_again(self, tpe):
        """再练一遍 操作过程"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.again_button()  # 结果页 再练一遍 按钮
            print('再练一遍:')
            self.diff_type(tpe)  # 不同模式 对应不同的游戏过程
