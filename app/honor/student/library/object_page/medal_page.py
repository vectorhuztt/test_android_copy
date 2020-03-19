#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/30 17:09
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf.base_page import BasePage
from conf.decorator import teststep


class MedalPage(BasePage):

    @teststep
    def medal_icon(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'medal')
        return ele

    @teststep
    def wait_check_medal_page(self):
        """勋章页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"我的勋章")]')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_medal_img_page(self):
        locator = (By.ID, self.id_type() + 'img')
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def medals(self):
        """奖牌"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'des')
        return ele

    @teststep
    def medal_content(self):
        """置灰奖牌的说明"""
        ele = self.driver.find_element_by_id(self.id_type() + 'text')
        return ele.text





