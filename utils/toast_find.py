#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conf.decorator import teststeps
from conf.base_page import BasePage


class Toast(BasePage):
    """获取toast 弹框"""
    @teststeps
    def find_toast(self, text, timeout=10, poll_frequency=0.1):
        """is toast exist, return True or False"""
        # noinspection PyBroadException
        try:
            toast = (By.XPATH, ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast))
            return True
        except Exception:
            return False
