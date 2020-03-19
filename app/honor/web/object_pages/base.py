# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/2/13 13:27
# -------------------------------------------


class BaseDriverPage:

    @classmethod
    def set_driver(cls, driver):
        cls.driver = driver

    def get_diver(self):
        return self.driver

    def page_source_web(self):
        print('页面内容', self.driver.page_source)