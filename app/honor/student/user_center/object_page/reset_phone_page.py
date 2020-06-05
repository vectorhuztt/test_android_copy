#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.decorator import teststep
from conf.base_page import BasePage
from utils.wait_element import WaitElement


class PhoneReset(BasePage):
    """修改手机号页面"""
    wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:手机号码”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'手机号')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def et_phone(self):
        """以“手机号”的id为依据"""
        locator = (By.ID, self.id_type() + 'et_phone')
        return self.wait.wait_find_element(locator)

    @teststep
    def verify(self):
        """以“验证码”的id为依据"""
        locator = (By.ID, self.id_type() + 'verify_input')
        return self.wait.wait_find_element(locator)

    @teststep
    def count_time(self):
        """以“获取验证码按钮”的id为依据"""
        locator = (By.ID, self.id_type() + 'count_time')
        self.wait.wait_find_element(locator).click()

    @teststep
    def btn_certain(self):
        """以“确定按钮”的id为依据"""
        locator = (By.ID, self.id_type() + 'btn_certain')
        self.wait.wait_find_element(locator).click()