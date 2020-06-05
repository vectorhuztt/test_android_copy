# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/2/13 13:27
# -------------------------------------------
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf.decorator import teststep


class BaseDriverPage:

    @classmethod
    def set_driver(cls, driver):
        cls.driver = driver

    def get_diver(self):
        return self.driver

    @teststep
    def get_wait_check_res(self, locator, timout=10):
        try:
            ele = WebDriverWait(self.driver, timout, 0.5).until(EC.visibility_of_element_located(locator))
            return ele
        except:
            return False

    def page_source_web(self):
        print('页面内容', self.driver.page_source)

