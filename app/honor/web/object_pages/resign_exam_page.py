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

from app.honor.web.object_pages.home_page import WebHomePage
from app.honor.web.object_pages.login_page import LoginWebPage
from app.honor.web.test_data.teacher_account import TeacherAccount
from conf.decorator import teststep
from utils.wait_element import WaitElement


class ResignExamPage(WebHomePage):
    wait = WaitElement()

    @teststep
    def wait_check_home_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()=" 创建班级"]')
        self.wait.wait_check_element(locator)

    def wait_check_mine_item_pool_page(self):
        """我的题库页面检查点"""
        time.sleep(3)
        locator = (By.XPATH, '//*[text()="我的"]')
        self.wait.wait_check_element(locator)

    def wait_check_exam_tab_page(self):
        """试卷页面"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="卷子名称"]')
        self.wait.wait_check_element(locator)

    def wait_check_mine_exam_page(self):
        """我的试卷页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="我的自创"]')
        self.wait.wait_check_element(locator)

    def wait_check_exam_detail_page(self):
        """试卷详情页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[text()="开始答卷"]')
        self.wait.wait_check_element(locator)

    def wait_check_delete_tip_page(self):
        """删除作业提示页面检查点"""
        locator = (By.CLASS_NAME, 'el-message-box__content')
        self.wait.wait_check_element(locator)

    def wait_check_publish_tip_page(self):
        """删除作业提示页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"试卷为【提分版】功能")]')
        self.wait.wait_check_element(locator)
     
    def wait_check_assign_page(self):
        """布置试卷页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(),"考试信息")]')
        self.wait.wait_check_element(locator)
     
    def logo(self):
        """logo"""
        locator = (By.ID, 'logo')
        return self.wait.wait_find_element(locator)

    def exam_label(self):
        """试卷"""
        locator = (By.CSS_SELECTOR, '.head-banner-container  .tab-group .tab')
        return self.wait.wait_find_elements(locator)[-1]

    def mine_label(self):
        """我的"""
        locator = (By.CSS_SELECTOR, '.head-bottom-nav .page-container  a')
        return self.wait.wait_find_elements(locator)[-1]

    def exam_list(self):
        """试卷列表"""
        locator = (By.CSS_SELECTOR, '.page-content-container  .testbank-list tbody tr')
        return self.wait.wait_find_elements(locator)

    def exam_name(self, ele):
        """试卷名称"""
        name = ele.find_element_by_xpath('./td[1]/div/span')
        print('\n布置试卷：', name.text)
        return name

    def delete_btn(self):
        """删除试卷"""
        locator = (By.CSS_SELECTOR, '.test-detail  .controls  button:nth-child(4)')
        return self.wait.wait_find_element(locator)
    
    def publish_confirm_btn(self):
        """发布试卷确定按钮"""
        locator = (By.CSS_SELECTOR, '.dialog-footer  .el-button--primary')
        return self.wait.wait_find_element(locator)

    def delete_confirm_btn(self):
        """删除提示信息确定按钮"""
        locator = (By.CSS_SELECTOR, '.el-message-box__btns .el-button--primary')
        return self.wait.wait_find_element(locator)
 
    def assign_exam_btn(self):
        """布置试卷"""
        locator = (By.CSS_SELECTOR, '.test-detail  .controls  button:nth-child(2)')
        return self.wait.wait_find_element(locator)

    def student_card(self):
        """学生列表"""
        locator = (By.CSS_SELECTOR, '.student-card')
        return self.wait.wait_find_elements(locator)

    def vanclass_label(self):
        """班级标签"""
        locator = (By.CSS_SELECTOR, '.choose-students li  span.name')
        return self.wait.wait_find_elements(locator)

    def publish_btn(self):
        """发布试卷按钮"""
        locator = (By.CSS_SELECTOR, '.head-banner-container  button')
        return self.wait.wait_find_element(locator)

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
                                if x.text == 'MVP':
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








