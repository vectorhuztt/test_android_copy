#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/30 17:09
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf.base_page import BasePage
from conf.decorator import teststep
from utils.wait_element import WaitElement


class MedalPage(BasePage):
    wait = WaitElement()

    @teststep
    def medal_icon(self):
        locator = (By.ID, self.id_type() + 'medal')
        return self.wait.wait_find_element(locator)

    @teststep
    def wait_check_medal_page(self):
        """勋章页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"我的勋章")]')
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_medal_img_page(self):
        locator = (By.ID, self.id_type() + 'img')
        return self.wait.wait_check_element(locator)

    @teststep
    def medals(self):
        """奖牌"""
        locator = (By.ID, self.id_type() + 'des')
        return self.wait.wait_find_elements(locator)

    @teststep
    def medal_content(self):
        """置灰奖牌的说明"""
        locator = (By.ID, self.id_type() + 'text')
        return self.wait.wait_find_element(locator).text




