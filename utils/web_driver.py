from conf.base_web import BaseDriverPage
from selenium import webdriver
from conf.base_config import GetVariable as gv


class GetWebDriver:
    _b = {
         'dev': 'http://dev.vanthink.cn/accounts#/login',
         'test': 'http://test.online.vanthink.cn/accounts#/login',
         'online': 'https://www.wxzxzj.com'
    }

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        url = self._b[gv.TEST_VERSION]
        self.driver.get(url)

    def set_driver(self):
        base = BaseDriverPage()
        base.set_driver(self.driver)

    def quit_web(self):
        self.driver.quit()

