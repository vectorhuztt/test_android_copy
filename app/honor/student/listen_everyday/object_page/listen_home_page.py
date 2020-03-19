# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/14 14:37
# -------------------------------------------
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep


class ListenHomePage(BasePage):

    @teststep
    def wait_check_listen_everyday_home_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "每日一听")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_degrade_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "是否感觉题太难了")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_certificate_page(self):
        locator = (By.XPATH, '//android.widget.Button[contains(@text, "炫耀一下")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_share_page(self):
        locator = (By.XPATH, '//android.widget.Button[contains(@text, "微信好友")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_today_limit_img_page(self):
        locator = (By.ID, self.id_type() + 'error_img')
        return self.get_wait_check_page_result(locator)

    @teststep
    def level_button(self):
        """等级"""
        ele = self.driver.find_element_by_id(self.id_type() + 'level')
        return ele

    @teststep
    def history_button(self):
        """历史记录"""
        ele = self.driver.find_element_by_id(self.id_type() + 'history')
        return ele

    @teststep
    def rank_button(self):
        """排行榜"""
        ele = self.driver.find_element_by_id(self.id_type() + "rank")
        return ele

    @teststep
    def start_button(self):
        """开始"""
        ele = self.driver.find_element_by_id(self.id_type() + 'start')
        return ele

    @teststep
    def excise_time(self):
        """练习时间"""
        ele = self.driver.find_element_by_id(self.id_type() + 'time')
        return ele


    @teststep
    def start_excise_button(self):
        """开始练习"""
        ele = self.driver.find_element_by_id(self.id_type() + 'action_two')
        return ele

    @teststep
    def commit_button(self):
        """确定"""
        ele = self.driver.find_element_by_id(self.id_type() + "confirm")
        return ele

