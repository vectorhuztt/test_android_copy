import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.user_center.object_page.buy_card_page import PurchasePage
from app.honor.student.user_center.object_page.user_Info_page import UserInfoPage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.web.object_pages.assign_word import AssignWord
from app.honor.web import Driver
from app.honor.student.word_book.object_page.wordbook_sql import WordBookSql
from conf.base_page import BasePage
from conf.decorator import teststep
from utils.toast_find import Toast
from conf.base_config import GetVariable as gv


class CleanDataPage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.common = WordBookSql()
        self.user_center = UserCenterPage()
        self.user_info = UserInfoPage()

    @teststep
    def wait_check_set_up_page(self):
        """以“设置” text 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_clear_cache_page(self):
        """以“设置” text 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'清除缓存')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def wait_check_grade_page(self):
        """以“请选择你所处的年级” text为依据"""
        locator =(By.XPATH, "//android.widget.TextView[contains(@text,'请选择你所处年级')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def select_setting_up(self):
        """点击设置"""
        self.driver.\
            find_element_by_xpath("//android.widget.TextView[contains(@text,'设置')]")\
            .click()

    @teststep
    def select_clear_cache(self):
        """清除缓存"""
        self.driver. \
            find_element_by_xpath("//android.widget.TextView[contains(@text,'清除缓存')]") \
            .click()

    @teststep
    def grade_btn(self):
        """点击年级"""
        self.driver. \
            find_element_by_xpath("//android.widget.TextView[contains(@text,'年级')]") \
            .click()

    @teststep
    def grade_options(self):
        """年级选项"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_grade')
        return ele

    @teststep
    def select_another_grade(self):
        """选择倒数第一个年级（只要此次年级和指定年级不一样都可以）"""
        grades = self.grade_options()
        grades[-1].click()

    @teststep
    def select_certain_grade(self):
        """选择指定年级 """
        xpath_ele = "//android.widget.TextView[contains(@text,'{}')]".format(gv.GRADE)
        self.driver. \
            find_element_by_xpath(xpath_ele).click()

    @teststep
    def reset_grade(self):
        """重新选择年级"""
        self.clean_cache()  # 清除缓存
        self.grade_btn()   # 年级按钮
        if self.wait_check_grade_page():
            self.select_another_grade()  # 选择最后一个年级
            if self.user_center.wait_check_user_center_page():
                self.grade_btn()
                if self.wait_check_grade_page():
                    self.select_certain_grade()  # 重新选择三年级
        if self.user_center.wait_check_user_center_page():
            self.home.click_tab_hw()

    @teststep
    def clean_cache(self):
        """清除缓存"""
        if self.wait_check_set_up_page():
            self.select_setting_up()    # 设置按钮
            if self.wait_check_clear_cache_page():
                self.select_clear_cache()  # 清空缓存
                Toast().find_toast("清除缓存成功")
            self.home.click_back_up_button()
            if self.user_center.wait_check_user_center_page():
                pass

    @teststep
    def clean_cache_back_to_home(self):
        """清除缓存"""
        self.home.click_tab_profile()
        self.home.screen_swipe_up(0.5, 0.9, 0.3, 1000)
        self.clean_cache()
        self.home.click_tab_hw()
        if self.home.wait_check_home_page():
            pass

    @teststep
    def clear_user_all_data(self):
        """清除数据库所有相关数据"""
        self.common.delete_all_word_data()
        self.common.delete_word_homework()
        with open('app/student/word_book_rebuild/test_data/spell_copy', 'w') as f:
            json.dump({"新词": {}, "标熟新词": {}, "标星新词": {}, "复习单词": {}}, f, ensure_ascii=False)

    @teststep
    def get_user_phone(self):
        """获取用户手机号"""
        self.home.click_tab_profile()
        if self.user_center.wait_check_user_center_page():
            self.user_center.click_buy()
            if PurchasePage().wait_check_buy_page():
                phone = self.user_info.phone()
                return phone

    @teststep
    def get_id_back(self, action=0):
        """返回主页面"""
        phone = self.get_user_phone()
        stu_id = self.mysql.find_student_id(phone)
        gv.STU_ID = stu_id[0][0]
        print("学生id:", gv.STU_ID)
        self.home.click_back_up_button()
        self.clean_cache()
        if action == 1:
            if self.user_center.wait_check_user_center_page():
                self.clear_user_all_data()  # 清空用户单词数据 重新练习
                web_driver = Driver()
                web_driver.set_driver()
                AssignWord().assign_wordbook_operate()
                web_driver.quit_web()
        self.home.click_tab_hw()


