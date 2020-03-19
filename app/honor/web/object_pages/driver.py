# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/2/13 13:27
# -------------------------------------------
from selenium import webdriver

from app.honor.web.object_pages.base import BaseDriverPage
from conf.base_config import GetVariable as gv


class Driver:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        if gv.TEST_VERSION == 'dev':
            self.driver.get('http://dev.vanthink.cn/accounts#/login')
        elif gv.TEST_VERSION == 'test':
            self.driver.get('https://test.online.vanthink.cn/accounts#/login')

    def set_driver(self):
        base = BaseDriverPage()
        base.set_driver(self.driver)

    def quit_web(self):
        self.driver.quit()


