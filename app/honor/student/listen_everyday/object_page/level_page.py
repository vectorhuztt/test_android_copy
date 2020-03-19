# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/14 13:40
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast


class LevelPage(BasePage):
    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_listening_level_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"听力等级")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_level_page(self, level_name):
        """最后一个等级页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"{}")]'.format(level_name))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_start_button(self, back_name):
        try:
            self.start_button(back_name)
            return True
        except:
            return False

    @teststep
    def back_name(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'back_name')
        return ele

    @teststep
    def play_voice_button(self, back_name):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/'
                                                'following-sibling::android.widget.LinearLayout/'
                                                'android.widget.ImageView'.format(back_name))
        return ele

    @teststep
    def level_name(self, back_name):
        ele = self.driver.find_elements_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling'
                                                 '::android.widget.LinearLayout/android.widget.TextView'
                                                 .format(back_name))
        return ele

    @teststep
    def start_button(self, back_name):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling'
                                                '::android.widget.TextView'.format(back_name))
        return ele


    @teststeps
    def level_page_ele_operate(self):
        tips = []
        while True:
            for i, x in enumerate(self.back_name()):
                content = self.back_name()[i].text
                print("等级说明：", content)
                if content in tips:
                    continue
                else:
                    tips.append(content)
                    print([y.text for y in self.level_name(content)])
                    if not self.wait_start_button(content):
                        self.home.screen_swipe_up(0.5, 0.9, 0.7, 1000)

                    if self.start_button(content).text == '练习中...':
                        print('该等级已开始学习')
                    else:
                        self.play_voice_button(content).click()
                        self.start_button(content).click()
                        if Toast().find_toast('听力等级设置成功'):
                            if self.start_button(content).text != '练习中...':
                                self.base_assert.except_error('Error-- 点击开始后文字未发生改变')
                        else:
                            self.base_assert.except_error('未发现等级设置成功提示')
                print('-' * 30, '\n')

            if self.wait_check_level_page('10级B'):
                break
            else:
                self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)

        while True:
            if self.wait_check_level_page('2级A'):
                print('选择测试等级： 2级A')
                self.start_button('2级A').click()
                break
            else:
                self.home.screen_swipe_up(0.5, 0.3, 0.9, 1000)
        self.home.click_back_up_button()




