# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/1/26 12:29
# -------------------------------------------
import time

from selenium.webdriver.common.by import By

from conf.base_web import BaseDriverPage
from app.honor.web.test_data.teacher_account import TeacherAccount
from conf.decorator import teststeps, teststep
from utils.wait_element import WaitElement


class LoginWebPage(BaseDriverPage):
    wait = WaitElement()

    @teststep
    def wait_check_login_page(self):
        """登录页面检查点"""
        locator = (By.CLASS_NAME, "login-form")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_identity_page(self):
        """身份选择页面检查点"""
        locator = (By.CLASS_NAME, "identity-form")
        return self.wait.wait_check_element(locator)

    @teststep
    def close_page_btn(self):
        """关闭页面"""
        locator = (By.CLASS_NAME, 'icon-cross')
        return self.wait.wait_find_element(locator)

    @teststep
    def username(self):
        """用户名"""
        locator = (By.CSS_SELECTOR, '.login-form input:nth-child(1)')
        return self.wait.wait_find_element(locator)

    @teststep
    def password(self):
        """密码"""
        locator = (By.CSS_SELECTOR, '.login-form input:nth-child(2)')
        return self.wait.wait_find_element(locator)

    @teststep
    def login_btn(self):
        """登录"""
        locator = (By.CSS_SELECTOR, '.login-form  .btn')
        return self.wait.wait_find_element(locator)

    @teststep
    def teacher_ele(self):
        """自由/在编教师"""
        locator = (By.CSS_SELECTOR, '.identity-form  .select img[alt$="教师"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def head_pic_icon(self):
        """头像"""
        locator = (By.CSS_SELECTOR, '.menu .name')
        return self.wait.wait_find_element(locator)

    @teststep
    def logout_btn(self):
        """退出"""
        locator = (By.CSS_SELECTOR, '.menu .list a')
        return self.wait.wait_find_elements(locator)[1]

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


