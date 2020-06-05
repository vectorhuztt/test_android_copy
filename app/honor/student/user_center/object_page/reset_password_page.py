#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.decorator import teststep
from conf.base_page import BasePage
from utils.wait_element import WaitElement


class PwdReset(BasePage):
    """修改密码页面所有控件信息"""
    wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:重置密码”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'重置密码')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def pwd_origin(self):
        """以“原始密码”的id为依据"""
        locator = (By.ID, self.id_type() + 'pwd_origin')
        return self.wait.wait_find_element(locator)

    @teststep
    def pwd_new(self):
        """以“新密码”的id为依据"""
        locator = (By.ID, self.id_type() + 'pwd_new')
        return self.wait.wait_find_element(locator)

    @teststep
    def pwd_confirm(self):
        """以“新密码二次确认”的id为依据"""
        locator = (By.ID, self.id_type() + 'pwd_confirm')
        return self.wait.wait_find_element(locator)

    @teststep
    def pwd_checkbox(self):
        """以“显示密码”的id为依据"""
        locator = (By.ID, self.id_type() + 'pwd_visible')
        self.wait.wait_find_element(locator).click()

    @teststep
    def confirm_button(self):
        """以“完成按钮”的id为依据"""
        locator = (By.ID, self.id_type() + 'pwd_complete')
        self.wait.wait_find_element(locator).click()

