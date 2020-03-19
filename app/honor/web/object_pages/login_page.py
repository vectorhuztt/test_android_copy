# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/1/26 12:29
# -------------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.honor.web.object_pages.base import BaseDriverPage
from app.honor.web.test_data.teacher_account import TeacherAccount
from conf.decorator import teststeps, teststep


class LoginWebPage(BaseDriverPage):
    @teststeps
    def wait_check_rocket_page(self):
        """判断是否有小火箭页面"""
        locator = (By.CLASS_NAME, "rocket-box")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_login_page(self):
        """登录页面检查点"""
        locator = (By.CLASS_NAME, "login-form")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_identity_page(self):
        """身份选择页面检查点"""
        locator = (By.CLASS_NAME, "identity-form")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def close_page_btn(self):
        """关闭页面"""
        ele = self.driver.find_element_by_class_name('icon-cross')
        return ele

    @teststep
    def username(self):
        """用户名"""
        username = self.driver.find_element_by_xpath('//*[@class="login-form"]/div[1]/input')
        return username

    @teststep
    def password(self):
        """密码"""
        password = self.driver.find_element_by_xpath('//*[@class="login-form"]/div[2]/div/input')
        return password

    @teststep
    def login_btn(self):
        """登录"""
        login_btn = self.driver.find_element_by_xpath('//*[@class="login-form"]/button')
        return login_btn

    @teststep
    def teacher_ele(self):
        """自由/在编教师"""
        ele = self.driver.find_element_by_xpath('//*[contains(text(),"在编教师")]')
        return ele

    @teststep
    def head_pic_icon(self):
        """头像"""
        ele = self.driver.find_element_by_css_selector('.menu .name')
        return ele

    @teststep
    def logout_btn(self):
        """退出"""
        ele = self.driver.find_elements_by_css_selector('.menu .list a')
        return ele[1]


    @teststep
    def login_operate(self, teacher_account=TeacherAccount.Account[-1][0],
                      teacher_pass=TeacherAccount.Account[-1][1]):
        """登录操作"""
        if self.wait_check_login_page():
            self.username().click()
            self.username().send_keys(teacher_account)
            self.password().send_keys(teacher_pass)
            self.login_btn().click()
            time.sleep(2)
            if self.wait_check_identity_page():
                self.teacher_ele().click()
                time.sleep(2)

    @teststep
    def logout_operate(self):
        """账号退出操作"""
        self.head_pic_icon().click()
        time.sleep(0.5)
        self.logout_btn().click()


