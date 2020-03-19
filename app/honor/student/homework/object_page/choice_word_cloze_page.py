#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.excel_read_write import ExcelUtil
from utils.click_bounds import ClickBounds
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class ChoiceWordCloze(BasePage):
    """选词填空"""
    def __init__(self):
        self.bounds = ClickBounds()
        self.result = ResultPage()
        self.get = GetAttribute()
        self.key = Keyboard()

    @teststeps
    def wait_check_page(self):
        """以“title:选词填空”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选词填空')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_play_page(self):
        """以“rate”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             + self.id_type() + "rate)]")
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
    def font_middle(self):
        """第一个Aa"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "font_middle")
        return ele

    @teststep
    def font_large(self):
        """第二个Aa"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "font_large")
        return ele

    @teststep
    def font_great(self):
        """第三个Aa"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "font_great")
        return ele

    @teststep
    def prompt(self):
        """提示词"""
        self.driver\
            .find_element_by_id(self.id_type() + "prompt").click()

    @teststep
    def bounds_prompt(self):
        """提示词按钮"""
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,0)]")[1]
        return ele

    @teststep
    def prompt_content(self):
        """提示词内容"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,0)]")[1].text
        return ele

    @teststep
    def click_blank(self):
        """点击页面 提示词弹框 以外空白处，弹框消失"""
        self.bounds.click_bounds(67.5, 1119.5)
        time.sleep(1)

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    # 查看答案 页面
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
    def content_value(self):
        """获取整个 外框元素"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "tb_content")
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
        print('正确答案：', answer)
        self.click_blank()
        return answer

    @teststeps
    def choice_word_filling(self):
        """《选词填空》 游戏过程"""
        if self.wait_check_page():  # 页面检查点
            if self.wait_check_play_page():
                timestr = []
                self.prompt()  # 右上角 提示词
                time.sleep(1)
                content = self.prompt_content()  # 取出提示内容
                self.click_blank()  # 点击空白处 弹框消失
                word_list = content.split('   ')  # 取出单词列表
                print('待输入的单词:', word_list)

                self.font_operate()  # Aa文字大小切换按钮 切换 及状态统计

                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 加点击

                    if i == 0:  # 获取第一个输入框的坐标，点击激活小键盘
                        item = self.content_desc()
                        loc = self.get_element_location(self.content_value())  # 文章元素左上角 顶点坐标
                        x = float(item[0][i]) + loc[0]+55.0  # 55.0为点击输入框中心点的偏移量
                        y = float(item[1][i]) + loc[1]
                        self.driver.tap([(x, y)])  # 点击激活输入框
                    else:
                        self.key.games_keyboard('enter')  # 点击回车键进入下一题

                    word = word_list[i]  # 单词
                    print('study_word:', word)
                    if len(word_list) >= int(rate):
                        for index in range(len(word)):
                            if index == 4:
                                self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
                                self.key.games_keyboard(word[index].upper())  # 点击键盘对应 大写字母
                                self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
                            else:
                                self.key.games_keyboard(word[index])  # 点击键盘对应字母
                    else:
                        self.key.games_keyboard('a')  # 点击键盘对应字母

                    timestr.append(self.time())  # 统计每小题的计时控件time信息

                Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时
                print('==================================================')
                return rate

    @teststeps
    def check_detail_page(self, rate, homework_title, game_title):
        """查看答案页面面"""
        if self.result.wait_check_result_page():  # 结果页检查点
            self.result.check_result_button()  # 结果页 查看答案 按钮

            if self.result.wait_check_detail_page():  # 页面检查点
                print('查看答案页面:')
                item = self.get_result()
                print('excel-opeate:')
                for i in range(len(item)):
                    print('----------------------')
                    ExcelUtil().data_write(rate, homework_title, game_title, item[i])
                self.result.back_up_button()

    @teststeps
    def font_operate(self):
        """Aa文字大小切换按钮 状态判断 及 切换操作"""
        x = []
        y = []
        middle = self.font_middle()  # first
        large = self.font_large()  # second
        great = self.font_great()  # third

        i = 0
        j = 0
        while i < 3:
            bounds = self.content_desc()  # 获取输入框坐标
            print(self.get.get_checked(middle), self.get.get_checked(large), self.get.get_checked(great))

            if self.get.get_checked(middle) == 'false':
                if self.get.get_checked(large) == 'false':
                    x.insert(2, bounds[0][0])
                    y.insert(2, bounds[1][0])
                    print('当前选中的Aa按钮为第3个：', bounds[0][0], bounds[1][0])
                    j = 3
                else:
                    if self.get.get_checked(large) == 'true':
                        x.insert(1, bounds[0][0])
                        y.insert(1, bounds[1][0])
                        print('当前选中的Aa按钮为第2个：', bounds[0][0], bounds[1][0])
                        j = 2
            else:
                x.insert(0, bounds[0][0])
                y.insert(0, bounds[1][0])
                print('当前选中的Aa按钮为第1个：', bounds[0][0], bounds[1][0])
                j = 1

            if j == 1:
                large.click()
            elif j == 2:
                great.click()
            else:
                middle.click()
            i += 1
            print('--------------------------------------------')
            time.sleep(2)

        if not float(y[2]) > float(y[1]) > float(y[0]):
            print('❌❌❌ Error - Aa文字大小切换按钮:', y)
        print('==============================================')
