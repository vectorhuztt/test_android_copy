# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/11 16:54
# -------------------------------------------
import random
import time

import numpy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from conf.base_page import BasePage
from conf.decorator import teststep


class PurchasePage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.user_center = UserCenterPage()

    @teststep
    def wait_check_buy_page(self):
            """以“购买”的xpath @text为依据"""
            locator = (By.XPATH, "//android.widget.TextView[contains(@text,'在线客服')]")
            try:
                WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
                return True
            except:
                return False

    @teststep
    def wait_check_help_center_page(self):
        """以“帮助中心”的xpath @text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'帮助中心')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_card_page(self):
        """以“优惠购买”的id 为依据"""
        locator = (By.ID, self.id_type() + "discount_pay")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_agreement_page(self):
        """以“购买协议”的xpath 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'购买协议')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_pay_confirm_page(self):
        """以“支付确认”的xpath 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'支付确认')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_parent_pay_page(self):
        """以“支付完成”的ID 为依据"""
        locator = (By.ID, self.id_type() + "pay_complete")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_magic_page(self):
        """以“支付完成”的ID 为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'在线助教家长端')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def online_server(self):
        """在线客服"""
        ele = self.driver.find_element_by_id(self.id_type() + 'goToCustomerService')
        return ele

    @teststep
    def magics(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'function_des')
        return ele

    @teststep
    def upgrade_button(self):
        """马上购买"""
        ele = self.driver.find_element_by_id(self.id_type() + 'goToUpgrade')
        return ele

    @teststep
    def discount_buy(self):
        """优惠购买"""
        ele = self.driver.find_element_by_id(self.id_type() + 'discount_pay')
        return ele

    @teststep
    def card_type(self):
        """优惠卡类型"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'one')
        return ele

    @teststep
    def check_radio(self, card_name):
        """选项按钮"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{}")]/../'
                                                'preceding-sibling::android.widget.RadioButton'.format(card_name))
        return ele

    @teststep
    def card_price(self, card_name):
        """卡片的价格  根据卡的类型获取"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "{}")]/../'
                                                'following-sibling::android.widget.LinearLayout/'
                                                'android.widget.TextView'.format(card_name))
        return ele

    @teststep
    def selected_card(self):
        """已选卡型"""
        ele = self.driver.find_element_by_id(self.id_type() + 'current_vip_card_hint')
        return ele

    @teststep
    def direct_buy_button(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'pay')
        return ele

    @teststep
    def confirm_pay_button(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'pay')
        return ele

    @teststep
    def discount_buy_button(self):
        """优惠购买按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'discount_pay')
        return ele

    @teststep
    def agreement(self):
        """购买协议"""
        ele = self.driver.find_element_by_id(self.id_type() + 'pay_agreement')
        return ele

    @teststep
    def ali_pay_tab(self):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"支付宝代付")]')
        return ele

    @teststep
    def wechat_pay_tab(self):
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"微信代付")]')
        return ele

    @teststep
    def parent_check_button(self):
        ele = self.driver.find_element_by_id(self.id_type() + 'parent_pay_check')
        return ele

    @teststep
    def get_all_text_view(self):
        """获取页面所有不为空的文本值"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        all_text = [ele[i].text for i in range(len(ele)) if ele[i].text != '' and ele[i].text is not None]
        return all_text

    @teststep
    def online_server_ele_check(self):
        self.online_server().click()
        if self.wait_check_help_center_page():
            print('在线助教客服二维码')
            self.home.click_back_up_button()

    @teststep
    def magic_ele_check(self):
        all_magics = self.magics()
        all_magics[random.randint(0, len(all_magics)-1)].click()
        if self.wait_check_magic_page():
            print('法宝详情页....\n')
            self.home.click_back_up_button()
            if self.wait_check_buy_page():
                pass


    @teststep
    def switch_card(self):
        """切换卡片"""
        card_type = self.card_type()
        for card in card_type:
            card.click()
            check_radio = self.check_radio(card.text)
            if check_radio.get_attribute('checked') != 'true':
                print('❌❌❌ Error-- 选项按钮状态未发生变化')
            current_card = self.selected_card()
            if card.text.split(' ')[0] != current_card.text:
                print('❌❌❌ Error-- 当前卡的类型与所选类型不一致')
            else:
                print('已选择', current_card.text, '\n')

            if '年卡' in card.text:
                card_price = self.card_price(card.text)
                discount_button = self.discount_buy_button()
                if '优惠价' in card_price.text:
                    if discount_button.get_attribute('enabled') != 'true':
                        print('❌❌❌ Error-- 有优惠价，但是优惠购买按钮置灰', card.text)
                else:
                    if discount_button.get_attribute('enabled') != 'false':
                        print('❌❌❌ Error-- 无优惠价，但是优惠购买按钮未置灰', card.text)

    @teststep
    def check_agreement(self):
        agreement = self.agreement()
        location = agreement.location
        self.driver.tap([(location['x']+520, location['y']+50), ])
        if self.wait_check_agreement_page():
            print('在线助教【提分版】购买协议 .....')
            self.home.screen_swipe_down(0.5, 0.5, 0.9, 1500)
            self.home.click_back_up_button()

    @teststep
    def direct_buy(self):
        if self.wait_check_card_page():
            self.direct_buy_button().click()
            if self.wait_check_pay_confirm_page():
                self.pay_confirm_page_ele_operate()
                self.parent_check_button().click()
                self.confirm_pay_button().click()
                if self.wait_check_parent_pay_page():
                    self.ali_pay_tab().click()
                    time.sleep(2)
                    self.parent_page_ele_operate()

                    self.wechat_pay_tab().click()
                    time.sleep(2)
                    self.parent_page_ele_operate()

    @teststep
    def magics_page_ele_operate(self):
        """法宝页面元素信息"""
        text = self.get_all_text_view()
        if len(text) != 16:
            print('❌❌❌ Error-- 页面元素缺失', text)
        else:
            magic_types = numpy.reshape(text[6:-1], (3, 3))
            print("<" + text[0] + '页面>', '\n',
                  '学生:', text[1], '\n',
                  '手机:', text[2], '\n',
                  '提示:', text[4] + text[5], '\n',
                  '法宝:', '\n', magic_types, '\n')

    @teststep
    def buy_page_ele_operate(self):
        """购买页面（优惠卡类型） 页面"""
        text = self.get_all_text_view()
        print(len(text))
        if len(text) not in range(18, 21):
            print('❌❌❌ Error-- 页面元素缺失', text)
        else:
            print('<选择优惠卡页面>\n'
                  '学生:', text[1], '\n',
                  '手机:', text[2], '\n',
                  '提示:', text[4] + text[5], '\n',
                  )
            if len(text) == 20:
                print('优惠卡类型', '\n',
                      text[6],  text[7], '\n',
                      text[8],  text[9], '\n',
                      text[10], text[11], text[12], '\n',
                      text[13], text[14], text[15], '\n',
                      '协议:', text[16], '\n',
                      '已选类型:', text[17], '\n',
                      text[18], text[19], '\n',
                      )
            else:
                print(
                    '优惠卡类型', '\n',
                    text[6],  text[7], '\n',
                    text[8],  text[9], '\n',
                    text[10], text[11], '\n',
                    text[12], text[13], '\n',
                    '协议:', text[14], '\n',
                    '已选类型:', text[15], '\n',
                    text[16], text[17], '\n',
                )

    @teststep
    def pay_confirm_page_ele_operate(self):
        text = self.get_all_text_view()
        if len(text) != 12:
            print('❌❌❌ Error-- 页面元素缺失', text)
        else:
            print('<支付确认页面>\n'
                  '学生:', text[1], '\n',
                  '手机:', text[2], '\n',
                  '卡型:', text[6], '\n',
                  "价格:", text[4] + text[5], '\n',
                  text[7] + ":", '\n',
                  text[8], text[9], text[10], '\n',
                  text[11], '\n'
                  )

    @teststep
    def parent_page_ele_operate(self):
        text = self.get_all_text_view()
        if len(text) != 9:
            print('❌❌❌ Error-- 页面元素缺失', text)
        else:
            print(
                '<'+text[0]+"页面>", '\n',
                text[1], text[2], '\n',
                '卡型:', text[3], '\n',
                '价格:', text[4] + text[5], '\n',
                text[6], '\n',
                text[7], '\n',
                text[8], '\n',
            )

    @teststep
    def back_to_home(self):
        self.home.click_back_up_button()
        if self.wait_check_pay_confirm_page():
            self.home.click_back_up_button()
            if self.wait_check_card_page():
                self.home.click_back_up_button()
                if self.wait_check_buy_page():
                    self.home.click_back_up_button()
                    if self.user_center.wait_check_user_center_page():
                        self.home.click_tab_hw()
                        if self.home.wait_check_home_page():
                            print('返回主界面')
