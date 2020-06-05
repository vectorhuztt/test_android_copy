#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.library.object_page.library_sql import LibrarySql
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book.object_page.wordbook_sql import WordBookSql
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.wait_element import WaitElement


class UserCenterPage(BasePage):
    """个人中心 页面"""

    wait = WaitElement()

    @teststep
    def wait_check_user_center_page(self):
        """以“设置”业务的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_nickname_page(self):
        """以“设置”业务的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'昵称')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def click_avatar_profile(self):
        """以“头像”的id为依据"""
        locator = (By.ID, self.id_type() + 'avatar_profile')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_cards(self):
        """以“卡片”的id为依据"""
        locator = (By.ID, self.id_type() + 'cards')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_setting(self):
        """以“设置”的id为依据"""
        locator = (By.ID, self.id_type() + 'setting')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_buy(self):
        """购买"""
        locator = (By.ID, self.id_type() + 'study_card')
        self.wait.wait_find_element(locator).click()

    @teststep
    def wait_check_buy_page(self):
        """购买页面检查点"""
        locator = (By.ID, self.id_type() + "goToCustomerService")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_logout_page(self):
        """退出登录页面检查点"""
        locator = (By.ID, self.id_type() + "logout")
        return self.wait.wait_check_element(locator)

    @teststep
    def nickname(self):
        """昵称"""
        locator = (By.ID, self.id_type() + 'name')
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def school_name(self):
        """学校名称"""
        locator = (By.ID, self.id_type() + 'school_name')
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def purchase(self):
        """购买"""
        locator = (By.ID, self.id_type() + 'study_card')
        return self.wait.wait_find_element(locator)

    @teststep
    def phone(self):
        """学生的手机号"""
        locator = (By.ID, self.id_type() + 'phone')
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def setting_up(self):
        """设置"""
        locator = (By.ID, self.id_type() + 'setting')
        return self.wait.wait_find_element(locator)

    @teststep
    def clear_cache(self):
        """清除缓存"""
        locator = (By.ID, self.id_type() + 'clear_cache')
        return self.wait.wait_find_element(locator)

    @teststep
    def get_user_info(self):
        """:return 学生id、学校名称、学校id、昵称"""
        HomePage().click_tab_profile()  # 点击个人中心
        if self.wait_check_user_center_page():  # 个人中心页面检查点
            self.screen_swipe_up(0.5, 0.2, 0.8, 1000)
            nickname = self.nickname()  # 昵称
            self.screen_swipe_up(0.5, 0.8, 0.2, 1000)
            self.purchase().click()  # 点击购买
            if self.wait_check_buy_page():  # 购买页面检查点
                phone = self.phone()  # 手机号
                stu_id = WordBookSql().find_student_id(phone)  # 根据手机号获取学生ID
                self.click_back_up_button()
                if self.wait_check_user_center_page():
                    school_name = self.school_name()  # 学习名称
                    school_id = 0
                    if school_name:
                        id1 = LibrarySql().find_school_id(school_name)
                        id2 = LibrarySql().find_school_id_by_short_name(school_name)
                        if id1:
                            school_id = id1[0][0]
                        else:
                            school_id = id2[0][0]

                    self.setting_up().click()
                    if self.wait_check_logout_page():  # 清除缓存
                        self.clear_cache().click()
                        time.sleep(2)

                    self.click_back_up_button()  # 返回个人中心
                    if self.wait_check_user_center_page():
                        HomePage().click_tab_hw()  # 点击学习返回主页面

                    print('学生昵称：', nickname, '\n',
                          '学校名称：', school_name, '\n',
                          '学校id：', school_id, '\n',
                          '学生id：', stu_id[0][0], '\n'
                          )
                    return stu_id[0][0], school_name, school_id, nickname



class MessageCenter(BasePage):
    """消息中心页面"""
    wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:消息中心”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'消息中心')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def iv_read_count(self):
        """以“未读消息数”的id为依据"""
        locator = (By.ID, self.id_type() + 'iv_read')
        ele = self.wait.wait_find_elements(locator)
        return len(ele)

    @teststep
    def message_count(self):
        """以“消息总数”的class_name为依据"""
        locator = (By.CLASS_NAME, "android.widget.RelativeLayout")
        return self.wait.wait_find_elements(locator)

    @teststep
    def click_message(self):
        """以“消息”的class_name为依据"""
        locator = (By.CLASS_NAME, "android.widget.RelativeLayout")
        self.wait.wait_find_element(locator).click()

    @teststep
    def del_message(self, size, rollsize=1):
        """以“删除消息”的class_name为依据"""
        # # 设定系数
        # a = 554.0 / 1080
        # b = 1625.0 / 1794
        elements = self.message_count()
        print('len(elements):', len(elements))
        # for i in range(len(elements))

    @teststep
    def click_negative_button(self):
        """以“取消按钮”的id为依据"""
        locator = (By.ID, self.id_type() + "md_buttonDefaultNegative")
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_positive_button(self):
        """以“确认按钮”的id为依据"""
        locator = (By.ID, self.id_type() + "md_buttonDefaultPositive")
        self.wait.wait_find_element(locator).click()

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class_name为依据"""
        locator = (By.CLASS_NAME, "android.widget.ImageButton")
        self.wait.wait_find_element(locator).click()


class Setting(BasePage):
    """设置页面"""
    wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:设置”的xpath @index为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'设置')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def help_center(self):
        """以“帮助中心”的id为依据"""
        locator = (By.ID, self.id_type() + "help")
        self.wait.wait_find_element(locator).click()

    @teststep
    def question_feedback(self):
        """以“问题反馈”的id为依据"""
        locator = (By.ID, self.id_type() + "feed")
        self.wait.wait_find_element(locator).click()

    def privacy_clause(self):
        """以“隐私条款”的id为依据"""
        locator = (By.ID, self.id_type() + "right")
        self.wait.wait_find_element(locator).click()

    @teststep
    def register_protocol(self):
        """以“注册协议”的id为依据"""
        locator = (By.ID, self.id_type() + "protocol")
        self.wait.wait_find_element(locator).click()

    @teststep
    def version_check(self):
        """以“版本检测”的id为依据"""
        locator = (By.ID, self.id_type() + "version_check")
        self.wait.wait_find_element(locator).click()

    @teststep
    def logout_button(self):
        """以“退出登录按钮”的id为依据"""
        locator = (By.ID, self.id_type() + "logout")
        self.wait.wait_find_element(locator).click()

    @teststeps
    def back_up(self):
        """从个人信息页 返回主界面"""
        if self.wait_check_page():
            HomePage().click_back_up_button()  # 返回按钮
            if UserCenterPage().wait_check_user_center_page():  # 页面检查点
                HomePage().click_tab_hw()

    @teststep
    def logout_operate(self):
        """退出登录"""
        HomePage().click_tab_profile()  # 进入首页后点击‘个人中心’按钮
        if UserCenterPage().wait_check_user_center_page():  # 页面检查点
            self.screen_swipe_up(0.5, 0.9, 0.3, 1000)
            UserCenterPage().click_setting()  # 进入设置页面

            if self.wait_check_page():  # 页面检查点
                self.logout_button()  # 退出登录按钮
                print('----------------')
                HomePage().tips_operate_commit()  # 退出登录提示框


class Privacy(BasePage):
    """版权申诉"""
    wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:版权申诉”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'版权申诉')]")
        return self.wait.wait_check_element(locator)


class ProtocolPage(BasePage):
    """注册协议"""
    wait = WaitElement()

    @teststep
    def wait_check_page(self):
        """以“title:注册协议”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'注册协议')]")
        return self.wait.wait_check_element(locator)

