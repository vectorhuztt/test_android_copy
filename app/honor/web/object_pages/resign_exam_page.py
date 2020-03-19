# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/2/16 13:52
# -------------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.honor.web.object_pages.base import BaseDriverPage
from app.honor.web.object_pages.home_page import WebHomePage
from app.honor.web.object_pages.login_page import LoginWebPage
from app.honor.web.test_data.teacher_account import TeacherAccount


class ResignExamPage(WebHomePage):
    def wait_check_home_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()=" 创建班级"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    def wait_check_mine_item_pool_page(self):
        """我的题库页面检查点"""
        time.sleep(3)
        locator = (By.XPATH, '//*[text()="我的"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_exam_tab_page(self):
        """试卷页面"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="卷子名称"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_mine_exam_page(self):
        """我的试卷页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="我的自创"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_exam_detail_page(self):
        """试卷详情页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="开始答卷"]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_delete_tip_page(self):
        """删除作业提示页面检查点"""
        locator = (By.CLASS_NAME, 'el-message-box__content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def wait_check_publish_tip_page(self):
        """删除作业提示页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"试卷为【提分版】功能")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
     
    def wait_check_assign_page(self):
        """布置试卷页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"考试信息")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False
     
    def logo(self):
        """logo"""
        ele = self.driver.find_element_by_id('logo')
        return ele

    def exam_label(self):
        """试卷"""
        ele = self.driver.find_element_by_xpath('//*[@id="page-head"]/div[1]/div/div[2]/div[1]/div[1]/a[3]')
        return ele
     
    def mine_label(self):
        """我的"""
        ele = self.driver.find_element_by_xpath('//*[@id="page-head"]/div[2]/div/a[2]')
        return ele
     
    def exam_list(self):
        """试卷列表"""
        ele = self.driver.find_elements_by_xpath('//*[@id="page-content"]/div/div[2]/table/tbody/tr')
        return ele

    def exam_name(self, ele):
        """试卷名称"""
        name = ele.find_element_by_xpath('./td[1]/div/span')
        print('\n布置试卷：', name.text)
        return name

    def delete_btn(self):
        """删除试卷"""
        ele = self.driver.find_element_by_xpath('//*[text()="删除试卷"]')
        return ele
    
    def publish_confirm_btn(self):
        """发布试卷确定按钮"""
        ele = self.driver.find_element_by_xpath('//*[text()="确 定"]')
        return ele

    def delete_confirm_btn(self):
        """删除提示信息确定按钮"""
        ele = self.driver.find_elements_by_css_selector('.el-message-box__btns span')
        return ele[1]
 
    def assign_exam_btn(self):
        """布置试卷"""
        ele = self.driver.find_element_by_xpath('//*[text()="布置试卷"]')
        return ele

    def student_card(self):
        """学生列表"""
        ele = self.driver.find_elements_by_class_name('student-card')
        return ele

    def vanclass_label(self):
        """班级标签"""
        ele = self.driver.find_elements_by_class_name('el-checkbox')
        return ele

    def vanclass_name_by_label(self, vanclass_ele):
        """根据标签获取班级名称"""
        ele = vanclass_ele.find_element_by_xpath('./following-sibling::span')
        return ele.text

    def publish_btn(self):
        """发布试卷按钮"""
        ele = self.driver.find_element_by_xpath('//*[@id="bodyer"]/div/div[1]/div/div/div/div[1]/button')
        return ele

    def reassign_exam_operate(self):
        LoginWebPage().login_operate(TeacherAccount.Account[-1][0],
                                     TeacherAccount.Account[-1][1])         # 登陆操作
        if self.wait_check_home_page():        # 进入我的试卷
            self.mine_bank_pool().click()
            if self.wait_check_mine_item_pool_page():
                self.mine_label().click()
                time.sleep(3)
                self.exam_label().click()
                time.sleep(3)
            while True:                       # 若试题>4, 则删除多余部分， 若等于4 ，则随机布置一个试卷
                if len(self.exam_list()) <= 5:
                    random_index = random.randint(0, 3)
                    self.exam_name(random_index).click()
                    if self.wait_check_exam_detail_page():
                        self.assign_exam_btn().click()               # 布置试卷
                        if self.wait_check_assign_page():
                            vanclass_label = self.vanclass_label()   # 选择MVP班级所有学生
                            for x in vanclass_label:
                                if self.vanclass_name_by_label(x) == 'MVP':
                                    x.click()
                                    break
                            time.sleep(2)
                            self.publish_btn().click()              # 发布试卷
                            if self.wait_check_publish_tip_page():
                                self.driver.execute_script(
                                    "document.getElementsByClassName('dialog-footer').item(0)"
                                    ".getElementsByTagName('button').item(1).click()")
                                time.sleep(3)
                    break

                else:
                    delete_name = self.exam_name(self.exam_list()[0])
                    print("删除试卷：", delete_name.text)
                    delete_name.click()
                    if self.wait_check_exam_detail_page():
                        self.delete_btn().click()                 # 删除试卷
                        time.sleep(2)
                        if self.wait_check_delete_tip_page():
                            self.driver.execute_script("document.getElementsByClassName('el-message-box__btns').item(0)"
                                                       ".getElementsByTagName('button').item(1).click()")
                            time.sleep(3)








