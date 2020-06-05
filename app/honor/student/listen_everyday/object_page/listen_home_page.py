# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/14 14:37
# -------------------------------------------
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep
from utils.wait_element import WaitElement


class ListenHomePage(BasePage):
    wait = WaitElement()

    @teststep
    def wait_check_listen_everyday_home_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "每日一听")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_degrade_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "是否感觉题太难了")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_certificate_page(self):
        locator = (By.XPATH, '//android.widget.Button[contains(@text, "炫耀一下")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_share_page(self):
        locator = (By.XPATH, '//android.widget.Button[contains(@text, "微信好友")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_today_limit_img_page(self):
        locator = (By.ID, self.id_type() + 'error_img')
        return self.wait.wait_check_element(locator)

    @teststep
    def level_button(self):
        """等级"""
        locator = (By.ID, self.id_type() + 'level')
        return self.wait.wait_find_element(locator)


    @teststep
    def history_button(self):
        """历史记录"""
        locator = (By.ID, self.id_type() + 'history')
        return self.wait.wait_find_element(locator)

    @teststep
    def rank_button(self):
        """排行榜"""
        locator = (By.ID, self.id_type() + 'rank')
        return self.wait.wait_find_element(locator)

    @teststep
    def start_button(self):
        """开始"""
        locator = (By.ID, self.id_type() + 'start')
        return self.wait.wait_find_element(locator)

    @teststep
    def excise_time(self):
        """练习时间"""
        locator = (By.ID, self.id_type() + 'time')
        return self.wait.wait_find_element(locator)

    @teststep
    def start_excise_button(self):
        """开始练习"""
        locator = (By.ID, self.id_type() + 'action_two')
        return self.wait.wait_find_element(locator)

    @teststep
    def commit_button(self):
        """确定"""
        locator = (By.ID, self.id_type() + 'confirm')
        return self.wait.wait_find_element(locator)

