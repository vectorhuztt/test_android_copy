#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.decorator import teststep
from conf.base_page import BasePage


class PhoneReset(BasePage):
    """修改手机号页面"""

    @teststep
    def wait_check_page(self):
        """以“title:手机号码”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'手机号')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def et_phone(self):
        """以“手机号”的id为依据"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "et_phone")
        return ele

    @teststep
    def verify(self):
        """以“验证码”的id为依据"""

        ele = self.driver\
            .find_element_by_id(self.id_type() + "verify_input")
        return ele

    @teststep
    def count_time(self):
        """以“获取验证码按钮”的id为依据"""
        self.driver\
            .find_element_by_id(self.id_type() + "count_time")\
            .click()

    @teststep
    def btn_certain(self):
        """以“确定按钮”的id为依据"""
        self.driver\
            .find_element_by_id(self.id_type() + "btn_certain")\
            .click()
