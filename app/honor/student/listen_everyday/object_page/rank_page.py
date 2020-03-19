# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/21 10:40
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from conf.base_page import BasePage
from conf.decorator import teststep


class RankPage(BasePage):

    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_rank_page(self):
        locator = (By.ID, self.id_type() + 'tv_order')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_name_page(self):
        locator = (By.ID, 'android:id/text1')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststep
    def select_class(self):
        self.driver.find_element_by_id('android:id/text1').click()

    @teststep
    def class_name(self):
        ele = self.driver.find_elements_by_id("android:id/text1")
        return ele

    @teststep
    def user_name(self):
        ele = self.driver.find_element_by_id(self.id_type() + "name")
        return ele

    @teststep
    def user_rank(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'rank')
        return ele

    @teststep
    def cover_title(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'cover_title_one')
        return ele

    @teststep
    def day_num(self):
        ele = self.driver.find_element_by_id(self.id_type() + "cover_title_two")
        return ele

    @teststep
    def show_button(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'share')
        return ele

    @teststep
    def week_rank(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'left_title')
        return ele

    @teststep
    def week_punch_days(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'right_title')
        return ele

    @teststep
    def game_name(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'game_name')
        return ele

    @teststep
    def student_names(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_name')
        return ele

    @teststep
    def days(self, stu_name):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/following-sibling::'
                                                'android.widget.TextView[contains(@resource-id, '
                                                '"{1}tv_score")]'.format(stu_name, self.id_type()))
        return ele.text


    @teststep
    def rank_ele_operate(self, name):
        self.select_class()
        time.sleep(2)
        van_class = self.class_name()
        self.home.click_blank()

        for i in range(len(van_class)):
            self.select_class()
            time.sleep(2)
            class_name = self.class_name()[i]
            print("班级:", class_name.text)
            class_name.click()
            if self.wait_check_rank_page():
                user_name = self.user_name().text
                print(user_name)
                if user_name != name:
                    self.base_assert.except_error('Error-- 名称与用户名不符')

                print(user_name, ' ', self.user_rank().text)
                print(self.cover_title().text + self.day_num().text, '\n')

                print(self.week_rank().text, '\t', self.week_punch_days().text)

                students = self.student_names()
                for j in range(len(students)):
                    print(students[j].text, '\t', self.days(students[j].text))

                print('-' * 30, '\n', '\n')

        self.show_button().click()
        GameCommonEle().share_page_operate()

