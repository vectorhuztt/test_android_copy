#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.common.by import By

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from utils.click_bounds import ClickBounds
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage


class UserInfoPage(BasePage):
    """个人信息页面"""

    @teststep
    def wait_check_page(self):
        """以“title:个人信息”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'个人信息')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def image(self):
        """以“头像”的id为依据
            用于判断是否有展示头像，但是具体头像内容不能判定"""
        ele = self.driver\
            .find_element_by_id("{}avatar".format(self.id_type()))
        return ele

    @teststep
    def nickname(self):
        """以“昵称”的id为依据
            用于判断昵称修改前后是否相同，默认修改后的昵称与修改前不同"""
        ele = self.driver\
            .find_element_by_id('{}nick'.format(self.id_type()))
        return ele.text

    @teststep
    def buy_page_nickname(self):
        """购买页昵称"""
        ele = self.driver \
            .find_element_by_id('{}name'.format(self.id_type()))
        return ele.text

    @teststep
    def phone(self):
        """以“手机号”的id为依据
            用于判断手机号修改前后是否相同，默认修改后的手机号与修改前不同"""
        ele = self.driver\
            .find_element_by_id("{}phone".format(self.id_type()))
        return ele.text

    @teststep
    def click_image(self):
        """以“头像”的id为依据"""
        self.driver\
            .find_element_by_id("{}avatar_profile".format(self.id_type()))\
            .click()
        time.sleep(2)

    @teststep
    def click_nickname(self):
        """以“昵称”的id为依据"""
        self.driver\
            .find_element_by_id("{}nick_profile".format(self.id_type()))\
            .click()
        time.sleep(2)

    @teststep
    def click_username(self):
        """以“用户名”的id为依据"""
        self.driver\
            .find_element_by_id("{}name_profile".format(self.id_type()))\
            .click()

    @teststep
    def click_phone_number(self):
        """以“手机号”的id为依据"""
        self.driver\
            .find_element_by_id("{}phone_profile".format(self.id_type()))\
            .click()

    @teststep
    def click_password(self):
        """以“密码”的id为依据"""
        self.driver\
            .find_element_by_id("{}pwd_profile".format(self.id_type()))\
            .click()

    @teststep
    def input(self):
        """以“修改昵称/用户名/手机号的二级页面中输入框”的class_name为依据"""
        ele = self.driver\
            .find_element_by_class_name('android.widget.EditText')
        return ele

    @teststep
    def click_negative_button(self):
        """以“取消按钮”的id为依据"""
        self.driver\
            .find_element_by_id('{}md_buttonDefaultNegative'.format(self.id_type()))\
            .click()

    @teststep
    def positive_button(self):
        """以“确认按钮”的id为依据"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'确定')]")
        value = ele.get_attribute('enabled')
        return value

    @teststep
    def click_positive_button(self):
        """以“确认按钮”的id为依据"""
        self.driver\
            .find_element_by_id('{}md_buttonDefaultPositive'.format(self.id_type()))\
            .click()

    @teststep
    def click_photograph(self):
        """以“拍照”的xpath @index为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'拍照')]") \
            .click()
        print('点击 拍照 按钮')

    @teststep
    def click_album(self):
        """以“从相册选择”的xpath @index为依据"""
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'从相册选择')]") \
            .click()
        print('点击 从相册选择 按钮')

    @teststep
    def click_block(self):
        """点击页面空白区域"""
        ClickBounds().click_bounds(540, 300)

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class name为依据"""
        self.driver\
            .find_element_by_class_name("android.widget.ImageButton")\
            .click()

    @teststeps
    def back_up(self):
        """从个人信息页 返回主界面"""
        if self.wait_check_page():
            self.back_up_button()  # 返回按钮
            if UserCenterPage().wait_check_user_center_page():  # 页面检查点
                HomePage().click_tab_hw()
