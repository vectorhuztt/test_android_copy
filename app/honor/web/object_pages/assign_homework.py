#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/20 11:48
# -----------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.honor.web.object_pages.home_page import WebHomePage
from app.honor.web.object_pages.login_page import LoginWebPage
from conf.decorator import teststep, teststeps


class AssignHomeworkPage(WebHomePage):

    @teststep
    def wait_check_bank_pool_page(self):
        """题库页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"推荐到学校")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_bank_list_page(self):
        """大题列表页面检查点"""
        time.sleep(2)
        locator = (By.CLASS_NAME, 'el-cascader__label')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def nav_bars(self):
        """头部按钮"""
        ele = self.driver.find_elements_by_css_selector('.nav a')
        return ele

    @teststep
    def type_tab(self):
        """题型选项"""
        ele = self.driver.find_elements_by_css_selector('.tab-group .tab')
        return ele

    @teststep
    def all_type_selector(self):
        """所有分类下拉按钮"""
        ele = self.driver.find_element_by_css_selector('.el-cascader__label')
        return ele

    @teststep
    def type_name_list(self):
        """类型列表"""
        ele = self.driver.find_elements_by_css_selector('.el-cascader-menu  .el-cascader-menu__item--extensible')
        return ele

    @teststep
    def game_name_list(self):
        """游戏名称列表"""
        ele = self.driver.find_elements_by_css_selector('.el-cascader-menus > ul:nth-child(2) li')
        return ele

    @teststep
    def bank_list(self):
        """大题列表"""
        ele = self.driver.find_elements_by_css_selector('.testbank-name .title')
        return ele

    @teststep
    def homework_name_input_warp(self):
        """作业名称输入栏"""
        ele = self.driver.find_element_by_css_selector('.el-input__inner[placeholder="请填写作业名称"]')
        return ele

    @teststep
    def publish_homework(self):
        """发布作业"""
        self.driver.find_element_by_css_selector('.controls .el-button').click()

    @teststep
    def get_bank_label(self, bank_name):
        """根据大题名称获取大题checkbox"""
        ele = self.driver.find_element_by_xpath('//*[contains(text(),"{}")]/../preceding-sibling::label/span/span'.format(bank_name))
        return ele


    @teststep
    def delete_homework_operate(self, hw_name):
        self.click_test_class()
        if self.wait_check_class_page():
            print('==== 删除已存在test作业 =====\n')
            while True:
                homework_list = self.homework_name()
                test_homework_ele = [x for x in homework_list if hw_name in x.text]
                if not test_homework_ele:
                    break
                else:
                    test_homework_ele[0].click()
                    print('删除作业：', test_homework_ele[0].text)
                    time.sleep(1)
                    self.delete_btn().click()
                    self.tip_box_operate()
                    time.sleep(2)


    @teststeps
    def assign_homework_operate(self):
        LoginWebPage().login_operate()
        if self.wait_check_home_page():
            self.click_logo()
            time.sleep(2)
            self.delete_homework_operate()
            self.nav_bars()[1].click()
            if self.wait_check_bank_pool_page():
                self.type_tab()[1].click()
                time.sleep(2)
                for x in [('单词练习', '连连看'), ('口语练习', '口语跟读')]:
                    print('选择习题：', x)
                    if self.wait_check_bank_list_page():
                        self.all_type_selector().click()
                        time.sleep(2)
                        type_list = self.type_name_list()
                        for type_ele in type_list:
                            if x[0] in type_ele.text:
                                type_ele.click()
                                time.sleep(2)
                                break

                        bank_list = self.game_name_list()
                        for bank_ele in bank_list:
                            if x[1] in bank_ele.text:
                                bank_ele.click()
                                time.sleep(2)
                                break
                        time.sleep(2)

                        random_ele = random.choice(self.bank_list())
                        self.get_bank_label(random_ele.get_attribute('title')).click()
                        self.join_blanket()
                        self.tips_operate()
                        time.sleep(3)


                self.nav_bars()[-1].click()
                if self.wait_check_blanket_page():
                    time.sleep(2)
                    self.select_all_checkbox().click()
                    self.bank_control_btn()[-1].click()
                    self.tip_box_operate()
                    if self.wait_check_assign_homework_page():
                        self.homework_name_input_warp().send_keys('test')
                        self.select_test_class()
                        self.publish_homework()
                        self.tips_operate()





















