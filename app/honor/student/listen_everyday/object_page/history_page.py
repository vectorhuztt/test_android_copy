# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 16:11
# -------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep


class HistoryPage(BasePage):

    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_history_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "历史推荐")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_button_page(self):
        locator = (By.ID, self.id_type() + 'clear')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_red_hint_page(self):
        locator = (By.ID, self.id_type() + 'tv_hint')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_img_page(self):
        locator = (By.ID, self.id_type() + 'img')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_tips_page(self):
        locator = (By.ID, self.id_type() + 'md_content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def game_name(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'game_name')
        return ele

    @teststep
    def right_rate(self, game_name):

        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/../'
                                                'following-sibling::android.widget.TextView[contains(@resource-id,'
                                                '"{1}right_rate")]'.format(game_name, self.id_type()))
        return ele

    @teststep
    def game_date(self, game_name):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/../'
                                                'following-sibling::android.widget.TextView'
                                                '[contains(@resource-id,"{1}time")]'.format(game_name, self.id_type()))
        return ele

    @teststep
    def tips_operate_commit(self):
        """温馨提示 页面信息  -- 确定"""
        if self.wait_check_tips_page():  # 温馨提示 页面
            self.home.tips_content()
            self.home.commit_button()  # 确定按钮

    @teststep
    def history_page_operate(self):
        game_names = self.game_name()
        game_num = len(game_names) if len(game_names) < 10 else len(game_names) -1
        for i in range(game_num):
            if self.wait_check_history_page():
                name = game_names[i].text
                right_rate = self.right_rate(name).text
                game_date = self.game_date(name).text
                print(name)
                print(right_rate)
                print(game_date)

                if i == 3 or i == 5 or i == 7:
                    if name == '听音连句':
                        game_names[i].click()
                        if not self.wait_check_clear_button_page():
                            self.base_assert.except_error('Error-- 未发现听音连句的清除按钮')
                        else:
                            print('进入听音连句游戏页面')
                        self.home.click_back_up_button()
                        self.tips_operate_commit()

                    if name == '听后选择':
                        game_names[i].click()
                        if not self.wait_check_red_hint_page():
                            self.base_assert.except_error('Error-- 未发现听后选择的红色提示')
                        else:
                            print('进入听后选择游戏页面')
                        self.home.click_back_up_button()
                        self.tips_operate_commit()

                    if name == '听音选图':
                        game_names[i].click()
                        if not self.wait_check_img_page():
                            self.base_assert.except_error('Error-- 未发现听音选图的图片')
                        else:
                            print('进入听音选图游戏页面')
                        self.home.click_back_up_button()
                        self.tips_operate_commit()

            print('-'*30, '\n')
        self.home.click_back_up_button()
