#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import random
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.homework_page import Homework
from conf.decorator import teststeps, teststep
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute


class ReadCompre(BasePage):
    """阅读理解"""
    def __init__(self):
        self.get = GetAttribute()

    @teststeps
    def wait_check_page(self):
        """以“title:阅读理解”的xpath-index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'阅读理解')]")
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
    def dragger(self):
        """拖动按钮"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "dragger")
        return ele

    @teststep
    def question_num(self):
        """题目内容"""
        num = self.driver \
            .find_element_by_id(self.id_type() + "question")
        return num

    @teststeps
    def get_first_num(self):
        """获取 当前页面第一个题号"""
        item = self.question_num().text.split(".")[0]
        return item

    def article_view_size(self):
        """获取整个文章页面大小"""
        num = self.driver.find_element_by_id(self.id_type() + "ss_view")
        var = num.size
        return var['height']

    def options_view_size(self):
        """获取整个选项页面大小"""
        num = self.driver.find_element_by_id(self.id_type() + "optionlist")
        var = num.size
        return var['height']

    @teststeps
    def option_button(self, var):
        """选项"""
        print(var)
        ele = self.driver\
            .find_elements_by_xpath("//android.widget.TextView[contains(@text, '%s')]"
                                    "/following-sibling::android.widget.LinearLayout/android.widget.LinearLayout"
                                    "/android.widget.LinearLayout/android.widget.TextView" % var)

        item = []  # 选项
        content = []  # 选项内容
        for i in range(0, len(ele), 2):
            item.append(ele[i])
            content.append(ele[i+1])
        print('选项个数:', len(item))

        return item, content

    @teststep
    def option_item(self, index):
        """选项 内容"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_item")[index].text
        return ele

    @teststep
    def time(self):
        """获取作业时间"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "time").text
        return ele

    @teststeps
    def reading_operate(self):
        """《阅读理解》 游戏过程"""
        if self.wait_check_page():
            if self.wait_check_play_page():
                timestr = []  # 获取每小题的时间

                drag = self.dragger()  # 拖动按钮
                loc = self.get_element_bounds(drag)  # 获取按钮坐标
                size = self.options_view_size()  # 获取整个选项页面大小
                self.driver.swipe(loc[2], loc[3], loc[2], loc[3] + size-10, 1000)  # 拖拽按钮到最底部，以便测试Aa

                self.font_operate()  # Aa文字大小切换按钮 状态判断 及 切换操作

                loc = self.get_element_bounds(drag)  # 获取按钮坐标
                y = loc[3] - size * 4 / 3
                if loc[3] - size * 4 / 3 < 0:
                    y = 0
                self.driver.swipe(loc[2], loc[3], loc[2], y, 1000)  # 向上拖拽

                rate = self.rate()
                for i in range(int(rate)):
                    Homework().rate_judge(rate, i)  # 测试当前rate值显示是否正确
                    Homework().next_button_operate('false')  # 下一题 按钮 状态判断 加点击

                    question = self.question_num().text  # 题目
                    if i != 0:
                        for step in range(0, 5):
                            if int(self.get_first_num()) == i+1:  # 正好
                                question = self.question_num().text
                                break
                            elif int(self.get_first_num()) > i+1:  # 上拉拉过了
                                self.screen_swipe_down(0.5, 0.7, 0.9, 1000)
                                if int(self.get_first_num()) == i+1:  # 正好
                                    question = self.question_num().text
                                    break
                                elif int(self.get_first_num()) < i+1:  # 下拉拉过了
                                    self.screen_swipe_up(0.5, 0.9, 0.8, 1000)  # 滑屏

                    options = self.option_button(question)
                    options[0][random.randint(0, len(options[0])) - 1].click()  # 随机点击选项
                    time.sleep(1)
                    for j in range(len(options[0])):
                        if GetAttribute().get_selected(options[1][j]) == 'true':
                            print('我的答案：', options[1][j].text)
                            break

                    if i != int(rate) - 1:
                        self.screen_swipe_up(0.5, 0.9, 0.5, 1000)

                    timestr.append(self.time())  # 统计每小题的计时控件time信息
                    print('---------------------------')

                Homework().next_button_operate('true')  # 下一题 按钮 状态判断 加点击
                Homework().now_time(timestr)  # 判断游戏界面 计时功能控件 是否在计时

    @teststeps
    def font_operate(self):
        """Aa文字大小切换按钮 状态判断 及 切换操作"""
        loc = []
        middle = self.font_middle()  # first
        large = self.font_large()  # second
        great = self.font_great()  # third

        i = 0
        j = 0
        while i < 3:
            self.screen_swipe_up(0.5, 0.85, 0.2, 1000)
            y = self.article_view_size()  # 获取整个文章页面大小
            self.screen_swipe_down(0.5, 0.2, 0.8, 1000)
            print(self.get.get_checked(middle), self.get.get_checked(large), self.get.get_checked(great))

            if self.get.get_checked(middle) == 'false':
                if self.get.get_checked(large) == 'false':
                    print('当前选中的Aa按钮为第3个,页面高度:', y)
                    loc.insert(2, y)
                    j = 3
                else:
                    if self.get.get_checked(large) == 'true':
                        print('当前选中的Aa按钮为第2个,页面高度:', y)
                        loc.insert(1, y)
                        j = 2
            else:
                print('当前选中的Aa按钮为第1个,页面高度:', y)
                loc.insert(0, y)
                j = 1

            if j == 1:
                large.click()
            elif j == 2:
                great.click()
            elif j == 3:
                middle.click()
            i += 1
            time.sleep(2)
            print('-----------------------------------------')

        if not float(loc[2]) > float(loc[1]) > float(loc[0]):
            print('❌❌❌ Error - Aa文字大小切换按钮:', loc)
        print('=============================================')
