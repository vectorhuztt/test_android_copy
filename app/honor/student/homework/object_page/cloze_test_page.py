#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from app.honor.student.homework.object_page.result_page import ResultPage
from conf.decorator import teststeps, teststep
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class Cloze(BasePage):
    """完形填空"""
    def __init__(self):
        self.get = GetAttribute()
    
    @teststeps
    def wait_check_page(self):
        """以“title:完形填空”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'完形填空')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_play_page(self):
        """以“rate”的ID为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,'{}rate')]".format(self.id_type()))
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
    def dragger_button(self):
        """拖动按钮"""
        num = self.driver \
            .find_element_by_id(self.id_type() + "dragger")
        return num

    @teststeps
    def question(self):
        """题目"""
        num = self.driver \
            .find_element_by_id(self.id_type() + "question").text
        return num

    @teststeps
    def option_button(self, var):
        """选项"""
        ele = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]"
                                    "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout"
                                    "/android.widget.LinearLayout/android.widget.TextView" % var)
        item = []
        content = []
        for i in range(0, len(ele), 2):
            item.append(ele[i])
            content.append(ele[i+1])
        print('选项个数:', len(item), len(content))
        return item, content

    @teststeps
    def option_content(self):
        """选项 内容"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_item")
        return ele

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(self.id_type() + "option")
        var = num.size
        return var['height']

    @teststep
    def input_text(self):
        """输入框"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "cl_content")
        return ele

    @teststeps
    def get_input_bounds(self):
        """获取 输入框坐标"""
        ele = self.input_text()  # 输入框
        content = self.get.get_description(ele)
        item_x = re.match(".*\[(.*)\].*\[", content)  # x值
        item_y = re.match(".*\[(.*)\].*", content)  # y值
        x = item_x.group(1).split(',')  # 所有输入框y值的列表
        y = item_y.group(1).split(',')  # 所有输入框x值的列表
        size = ele.size
        return x, y, size

    @teststeps
    def get_result(self):
        """获取 输入框 的结果"""
        ele = self.input_text()  # 输入框
        content = self.get.get_description(ele)
        value = re.match("\\[(.+?)\\]", content)  # answer
        answer = value.group(1).split(',')  # 所有输入框值的列表
        print(answer)
        return answer

    @teststeps
    def cloze_operate(self):
        """《完形填空》 游戏过程"""
        if self.wait_check_page():
            if self.wait_check_play_page():
                result = []
                timestr = []  # 获取每小题的时间
                rate = self.rate()

                self.font_operate()  # Aa文字大小切换按钮 切换 及状态统计

                drag = self.dragger_button()  # 拖拽 拖动按钮
                loc = self.get_element_bounds(drag)
                size = self.options_view_size()  # 获取整个选项页面大小

                y = loc[3] - size * 4 / 3
                if loc[3] - size * 4 / 3 < 0:
                    y = 0
                self.driver.swipe(loc[2], loc[3], loc[2], y, 1000)  # 向上拖拽

                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 判断加 点击操作

                    if i == 4:
                        self.screen_swipe_up(0.5, 0.5, 0.25, 1000)

                    num = self.question()  # 题目
                    if int(re.sub("\D", "", num)) == i:  # 如果一次没滑动，再滑一次
                        self.screen_swipe_left(0.9, 0.8, 0.1, 2000)
                        num = self.question()  # 题目
                    print(num)

                    options = self.option_button(num)  # 四个选项
                    options[0][random.randint(0, len(options[0])) - 1].click()  # 随机点击选项
                    time.sleep(1)
                    for j in range(len(options[0])):
                        if self.get.get_selected(options[0][j]) == 'true':
                            print('选择的答案:', options[1][j].text)
                            result.append(options[1][j].text)
                            break

                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    self.screen_swipe_left(0.9, 0.8, 0.1, 2000)

                    if i == int(rate)-1:  # 最后一小题：1、测试滑动页面是否可以进入结果页   2、拖拽 拖动按钮
                        if not ResultPage().wait_check_result_page(2):  # 结果页检查点
                            drag = self.dragger_button()  # 拖拽 拖动按钮
                            loc = self.get_element_bounds(drag)
                            self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size - 10, 1000)  # 拖拽按钮到底部
                        else:
                            print('❌❌❌ Error - 滑动页面进入了结果页')

                    time.sleep(1)
                    print('================')

                time.sleep(1)
                content = self.get_result()  # 测试 是否答案已填入文章中
                if len(content) != len(result):
                    print('❌❌❌ Error -获取到的答案不一致', result, content)
                else:
                    for k in range(len(result)):
                        if content[k][0] == ' ':  # 由于填入content-desc的数据会自动加一个空格，故去掉
                            content[k] = content[k][1:]
                        if content[k] != result[k]:
                            print('❌❌❌ Error - 填入的答案与选择的答案不一致', result[k], content[k])

                Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时

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
            bounds = self.get_input_bounds()  # 获取输入框坐标
            print(self.get.get_checked(middle), self.get.get_checked(large), self.get.get_checked(great))

            if self.get.get_checked(middle) == 'false':
                if self.get.get_checked(large) == 'false':
                    x.insert(2, bounds[0][0])
                    y.insert(2, bounds[1][0])
                    print('当前选中的Aa按钮为第3个:', bounds[0][0], bounds[1][0])
                    j = 3
                else:
                    if self.get.get_checked(large) == 'true':
                        x.insert(1, bounds[0][0])
                        y.insert(1, bounds[1][0])
                        print('当前选中的Aa按钮为第2个:', bounds[0][0], bounds[1][0])
                        j = 2
            else:
                x.insert(0, bounds[0][0])
                y.insert(0, bounds[1][0])
                print('当前选中的Aa按钮为第1个:', bounds[0][0], bounds[1][0])
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
