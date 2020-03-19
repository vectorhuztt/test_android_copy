#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/23 15:09
# -----------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from conf.decorator import teststep
from utils.toast_find import Toast


class StudySettingPage(UserCenterPage):

    @teststep
    def wait_check_study_setting_page(self):
        """学习设置页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "学习设置")]')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_wordbook_study_setting_page(self):
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "单词本学习设置")]')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def study_setting(self):
        """单词本"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'study_setting')
        return ele

    @teststep
    def get_study_setting_side(self):
        """获取学习设置外边框"""
        ele = self.driver.find_elements_by_xpath('//android.support.v7.widget.RecyclerView/android.view.View')
        return ele


    @teststep
    def check_study_model_operate(self, study_model=1):
        """查看单词本学习设置操作"""
        HomePage().click_tab_profile()
        if self.wait_check_user_center_page():
            self.screen_swipe_up(0.5, 0.8, 0.2, 1000)
            self.study_setting()[0].click()
            if self.wait_check_study_setting_page():
                self.study_setting()[0].click()
                if self.wait_check_wordbook_study_setting_page():
                    thirty_model = self.get_study_setting_side()[0]
                    if thirty_model.get_attribute('clickable') == 'false':
                        print('❌❌❌ 默认单词本学习设置不为每组30词')
                    if study_model == 2:
                        self.study_setting()[1].click()
                        self.study_setting()[0].click()
                        if Toast().find_toast('一天内规则不可重复设置'):
                            print('规则一天内不可重复设置')
                        else:
                            print('❌❌❌ 未发现不可重复设置提示')
                    self.click_back_up_button()
                    if self.wait_check_study_setting_page():
                        self.click_back_up_button()
                    if self.wait_check_user_center_page():
                        HomePage().click_tab_hw()






