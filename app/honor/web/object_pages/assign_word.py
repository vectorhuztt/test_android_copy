# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/12 14:50
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.honor.web.object_pages.base import BaseDriverPage
from app.honor.web.object_pages.home_page import WebHomePage
from app.honor.web.object_pages.login_page import LoginWebPage
from conf.decorator import teststep


class AssignWord(BaseDriverPage):
    def __init__(self):
        self.home = WebHomePage()

    @teststep
    def wait_check_wordbook_page(self):
        """单词本页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="单词量排行"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_label_select_page(self):
        """检查是否还有下一级标签"""
        time.sleep(1)
        locator = (By.CLASS_NAME, 'label-list')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_assign_tip_page(self):
        """布置单词提示页面检查点"""
        time.sleep(1)
        locator = (By.CLASS_NAME, 'el-dialog__body')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_alert_tip_page(self):
        """弹框提示页面检查点"""
        time.sleep(1)
        locator = (By.CLASS_NAME, 'el-message-box__content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_class_page(self):
        locator = (By.XPATH, "//*[text()=' 邀请学生']")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_word_page(self):
        time.sleep(2)
        locator = (By.XPATH, "//*[text()='选择单词 ']")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_apply_students_page(self):
        """申请入班学生列表页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, "//*[contains(text(),'同意')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_any_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_assigned_word_page(self):
        """申请入班学生列表页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, "//*[contains(text(),'撤销')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_any_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def class_list(self):
        """班级名称列表"""
        ele = self.driver.find_elements_by_css_selector('#class-list a')
        return ele

    @teststep
    def wordbook_tab(self):
        """单词本"""
        ele = self.driver.find_element_by_xpath('//*[text()="单词本"]')
        return ele

    @teststep
    def student_tab(self):
        """学生标签"""
        ele = self.driver.find_elements_by_css_selector('.head-bottom-nav a')
        return ele[-1]

    @teststep
    def student_name(self):
        """申请学生姓名"""
        ele = self.driver.find_elements_by_class_name('username')
        return ele

    @teststep
    def student_nickname(self):
        """申请学生昵称"""
        ele = self.driver.find_elements_by_class_name('nickname')
        return ele

    @teststep
    def student_phone(self):
        """申请学生手机号"""
        ele = self.driver.find_elements_by_class_name('phone')
        return ele

    @teststep
    def agree_btn(self):
        """同意按钮"""
        ele = self.driver.find_elements_by_xpath('//*[contains(text(),"同意")]')
        return ele

    @teststep
    def reject_btn(self):
        """拒绝按钮"""
        ele = self.driver.find_elements_by_xpath('//*[contains(text(), "拒绝")]')
        return ele

    @teststep
    def alert_tip_content(self):
        """弹框提示内容"""
        ele = self.driver.find_element_by_css_selector('.el-message-box__message')
        return ele.text

    @teststep
    def alert_confirm_btn(self):
        """弹框提示确定按钮"""
        ele = self.driver.find_elements_by_css_selector('.el-message-box__btns .el-button')
        return ele[1]

    @teststep
    def get_all_assigned_word_book(self):
        """获取所有已布置的单词记录"""
        ele = self.driver.find_elements_by_css_selector('.table-list tr')
        return ele

    @teststep
    def assigned_word_book_name(self):
        """已布置单词的名称"""
        ele = self.driver.find_elements_by_css_selector('.name-wrapper p')
        return ele

    @teststep
    def revoke_btn(self):
        """撤销"""
        ele = self.driver.find_elements_by_css_selector('.revoke')
        return ele

    @teststep
    def assign_word_btn(self):
        """布置单词按钮"""
        ele = self.driver.find_elements_by_css_selector('.controls-bar .el-button')
        return ele[0]

    @teststep
    def assign_label(self, index):
        """复习1 标签"""
        ele = self.driver.find_elements_by_css_selector('.label-list .label')
        return ele[index]

    @teststep
    def next_label(self):
        """下一级标签"""
        ele = self.driver.find_element_by_xpath('//*[@class="label-list"]/a[1]')
        return ele

    @teststep
    def select_vanclass_operate(self, class_name):
        """选择班级"""
        ele = self.driver.find_elements_by_css_selector('.vanclass-tree .name')
        label = self.driver.find_elements_by_class_name('el-checkbox__input')
        for i, van_class in enumerate(ele):
            if van_class.text == class_name:
                label[i].click()
                break

    @teststep
    def assign_now_btn(self):
        """立即布置按钮"""
        ele = self.driver.find_element_by_xpath('//*[@class="controls-bar"]/button')
        return ele

    @teststep
    def assign_tip_content(self):
        """布置单词提示内容"""
        ele = self.driver.find_element_by_class_name('el-dialog__body')
        return ele.text

    @teststep
    def assign_confirm_btn(self):
        """确定按钮"""
        ele = self.driver.find_element_by_xpath('//*[@id="page-content"]/div[5]/div/div[3]/div/button[2]')
        return ele

    @teststep
    def agree_student_into_class_operate(self):
        """同意学生申请操作"""
        time.sleep(2)
        self.student_tab().click()
        if self.wait_check_apply_students_page():
            for i, name in enumerate(self.student_name()):             # 遍历申请学生
                print(name.text,                                       # 输出申请学生信息
                      self.student_nickname()[i].text,
                      self.student_phone()[i].text
                      )
                self.agree_btn()[i].click()                            # 同意
                if self.wait_check_alert_tip_page():
                    print(self.alert_tip_content())                    # 提示内容
                    self.alert_confirm_btn().click()                   # 确定
                    time.sleep(2)

    @teststep
    def revoke_word_book_operate(self):
        """撤销所有单词"""
        self.wordbook_tab().click()
        time.sleep(2)
        all_wordbook = self.get_all_assigned_word_book()
        index = 0
        while index < len(all_wordbook):  # 有已布置单词
            print(self.assigned_word_book_name()[0].text)
            self.revoke_btn()[0].click()  # 点击撤销
            time.sleep(2)
            index += 1

    @teststep
    def assign_word_to_students_operate(self, class_name, index):
        """布置单词给学生"""
        self.revoke_word_book_operate()
        self.assign_word_btn().click()
        time.sleep(2)
        self.select_vanclass_operate(class_name)                     # 选择班级

        self.assign_label(index).click()  # 选择标签                  # 选择标签
        time.sleep(2)
        while self.wait_check_label_select_page():                   # 继续选择下一级标签
            self.next_label().click()
            time.sleep(0.5)

        self.assign_now_btn().click()                                # 立即布置
        if self.wait_check_assign_tip_page():
            print(self.assign_tip_content())
            self.assign_confirm_btn().click()
            time.sleep(2)
            print('\n布置单词成功')
            print('-'*30, '\n')

    @teststep
    def assign_wordbook_operate(self, class_num, teacher_account, teacher_pass):
        """布置单词操作"""
        LoginWebPage().login_operate(teacher_account, teacher_pass)
        if self.home.wait_check_home_page():
            index = 0
            for x in self.class_list():
                class_id = x.get_attribute('href').split('/')[-1]
                if class_id in class_num:
                    print('选择班级：', x.text)
                    x.click()
                    if self.wait_check_class_page():
                        self.agree_student_into_class_operate()
                    word_index = 19 if index == 0 else 21
                    self.assign_word_to_students_operate(x.text, word_index)
                    index += 1

    @teststep
    def revoke_van_class_wordbook_operate(self, teacher_account, teacher_pass):
        LoginWebPage().login_operate(teacher_account, teacher_pass)
        if self.home.wait_check_home_page():
            for x in self.class_list():
                x.click()
                self.driver.implicitly_wait(2)
                if self.wait_check_class_page():
                    self.revoke_word_book_operate()









