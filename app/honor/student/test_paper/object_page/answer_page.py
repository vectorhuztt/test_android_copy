# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/25 10:14
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class AnswerPage(BasePage):
    """小题页面"""

    @teststep
    def wait_check_answers_page(self):
        """以 答题卷 的标题 作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'提交并查看结果')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_confirm_tip_page(self):
        """以 确认交卷 的text作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'确认交卷')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_tip_name(self, t_name):
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % t_name)
        return self.get_wait_check_page_result(locator)

    @teststep
    def answer_check_button(self):
        """查看结果按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'answercard')
        return ele

    def question_titles(self):
        """获取题型名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + "tv_sheet_title")
        return ele

    @teststep
    def question_index(self):
        """题目的序号"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'rtv_num')
        return ele

    @teststep
    def tip_index(self, var):
        """获取序号为1 的题"""
        ele = self.driver.find_elements_by_xpath('//android.widget.TextView[contains(@text,"%s")]/../'
                                                 'following-sibling::android.support.v7.widget.RecyclerView/'
                                                 'android.widget.FrameLayout/android.widget.TextView' % var)
        return ele

    @teststep
    def ques_num(self, var):
        """获取题目 的题数描述"""
        locator = '//android.widget.TextView[contains(@text,"{0}")]/following-sibling::' \
                  'android.widget.TextView[contains(@resource-id,"{1}tv_sheet_num")]'.format(var, self.id_type())

        ele = self.driver.find_element_by_xpath(locator)
        return ele.text

    @teststep
    def exam_submit(self):
        """试卷提交"""
        self.driver.find_element_by_id(self.id_type() + 'tv_submit').click()

    @teststep
    def submit_confirm(self):
        """试卷 提交确认"""
        self.driver.find_element_by_id(self.id_type() + 'md_buttonDefaultPositive') \
            .click()

    @teststep
    def wait_result_btn_enabled(self):
        """等待结果页变为可点击状态"""
        while True:
            attr = self.answer_check_button()
            if attr.get_attribute('enabled') == 'true':
                break
            else:
                self.driver.implicitly_wait(1)

    @teststep
    def submit_tip_operate(self):
        """试卷提交 步骤"""
        self.exam_submit()
        if self.wait_check_confirm_tip_page():
            self.submit_confirm()

    @teststeps
    def check_skip_to_tip_status(self, t_name, index):
        """查看题目跳转状态"""
        self.answer_check_button().click()     # 查看答案
        if self.wait_check_answers_page():
            while t_name not in [x.text for x in self.question_titles()]:
                self.screen_swipe_up(0.5, 0.8, 0.5, 1000)

            while int(self.tip_index(t_name)[-1].text) < index:
                self.screen_swipe_up(0.5, 0.8, 0.6, 1000)

            if t_name == '连连看':
                undo_tip = [x for x in self.tip_index(t_name) if x.get_attribute('selected') == 'false']
                undo_tip[0].click()
            else:
                self.tip_index(t_name)[index].click()


    @teststep
    def skip_operator(self, i, num, game_type, page_func, status_func, *args):
        """
        :param status_func: 跳转判断方法
        :param page_func: 页面等待方法
        :param game_type: 题目类型
        :param num: 总题数
        :param i:  题目索引
        """
        if i != num - 1 and i % 2 == 0:
            time.sleep(1.5)
            self.check_skip_to_tip_status(game_type, i + 1)
            if not page_func():
                self.base_assert.except_error('从下一题题号进入游戏， 未进入游戏页面')

            self.check_skip_to_tip_status(game_type, i)
            if page_func():
                print('查看答案跳转题目')
                status_func(*args)
        else:
            self.screen_swipe_left(0.9, 0.6, 0.2, 1000)
            flag = 1 if page_func() else 2
            if flag:
                self.screen_swipe_right(0.2, 0.6, 0.9, 1000)
            if page_func():
                print('左右滑动跳转题目')
                status_func(*args)
            else:
                self.base_assert.except_error('未返回做题页面')
        if i != num - 1:
            self.check_skip_to_tip_status(game_type, i + 1)
        print('-' * 20, '\n')