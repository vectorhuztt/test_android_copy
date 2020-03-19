#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.login.object_page.home_page import HomePage
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class BuyTipsPage(BasePage):
    """购买提示 页面"""
    @teststeps
    def wait_check_page(self, var=20):
        """以“提示”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'提示')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def img_judge(self):
        """判断图片 是否存在"""
        try:
            self.driver \
                .find_element_by_class_name("android.widget.ImageView")
            return True
        except Exception:
            return False

    @teststeps
    def tips_title(self):
        """以“标题” 的id"""
        ele = self.driver\
            .find_element_by_id(self.id_type() + "head_hint").text
        print(ele)

    @teststeps
    def tips_content(self):
        """以“提示页面 页中文案”的xpath为依据"""
        ele = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,2)]").text
        print(ele)

    @teststep
    def goto_pay_button(self):
        """去购买 按钮 """
        self.driver \
            .find_element_by_id(self.id_type() + "goto_pay")\
            .click()

    @teststep
    def goto_verification(self):
        """购买 验证 """
        item = self.driver \
            .find_element_by_id(self.id_type() + "goto_verification")
        return item

    # 购买 页面
    @teststeps
    def wait_check_pay_page(self, var=20):
        """以“购买”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'购买')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def st_icon(self):
        """学生头像 """
        item = self.driver \
            .find_element_by_id(self.id_type() + "avatar")
        return item

    @teststeps
    def st_name(self):
        """学生name """
        item = self.driver \
            .find_element_by_id(self.id_type() + "name").text
        print(item)

    @teststeps
    def st_phone(self):
        """学生 手机号"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "phone").text
        print(item)

    @teststep
    def online_service(self):
        """在线客服"""
        self.driver \
            .find_element_by_id(self.id_type() + "goToCustomerService").click()

    @teststeps
    def buy_hint(self):
        """购买 提示信息"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "pay_hint").text
        print(item)

    @teststeps
    def hint_info(self):
        """提示信息"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "hint").text
        print(item)

    @teststep
    def check_button(self):
        """卡前的 单选框 """
        item = self.driver \
            .find_elements_by_id(self.id_type() + "check")
        return item

    @teststep
    def card_name(self):
        """卡的类型:月卡、季卡、半年卡、年卡 """
        item = self.driver \
            .find_elements_by_id(self.id_type() + "one")
        return item

    @teststep
    def card_price(self):
        """卡的 价格 """
        item = self.driver \
            .find_elements_by_id(self.id_type() + "two")
        return item

    @teststeps
    def current_card(self):
        """目前选定的是X卡"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "current_vip_card_hint").text
        print('目前选中的卡为：', item)

    @teststep
    def buy_agreement(self):
        """购买协议"""
        self.driver \
            .find_element_by_id(self.id_type() + "pay_agreement").click()

    @teststep
    def direct_buy_button(self):
        """直接购买"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "pay")
        return ele

    @teststep
    def discount_pbuy_button(self):
        """优惠购买"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "discount_pay")
        return ele

    # 在线客服
    @teststeps
    def wait_check_help_page(self, var=20):
        """以“帮助中心”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'帮助中心')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 购买协议
    @teststeps
    def wait_check_protocol_page(self, var=20):
        """以“购买协议”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'购买协议')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 支付确认 页面
    @teststeps
    def wait_check_pay_confirm_page(self, var=20):
        """以“支付确认”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'支付确认')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def price_unit(self, index=1):
        """货币单位"""
        item = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,0)]")[index].text
        return item

    @teststeps
    def price_info(self):
        """价格"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "money").text
        return item

    @teststeps
    def card_hint(self):
        """所购卡的 提示信息"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "vip_type_hint").text
        print(item)

    @teststeps
    def pay_type(self):
        """wording:支付方式"""
        item = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,0)]")[2].text
        print(item)

    @teststep
    def pay_icon(self):
        """微信、支付宝、代付icon """
        item = self.driver \
            .find_elements_by_class_name("android.widget.ImageView")
        return item

    @teststep
    def wechat_pay_check(self):
        """微信 单选框 """
        item = self.driver \
            .find_element_by_id(self.id_type() + "wechat_pay_check")
        return item

    @teststep
    def ali_pay_check(self):
        """支付宝 单选框 """
        item = self.driver \
            .find_element_by_id(self.id_type() + "ali_pay_check")
        return item

    @teststep
    def parent_pay_check(self):
        """家长代付 单选框 """
        item = self.driver \
            .find_element_by_id(self.id_type() + "parent_pay_check")
        return item

    @teststeps
    def pay_mode(self, index):
        """支付方式列表 wording：微信、支付宝、代付"""
        item = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,2)]")[index].text
        print(' ', item)

    @teststep
    def confirm_pay_button(self):
        """确认支付 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "pay").click()

    @teststeps
    def pay_delay_tips(self):
        """支付延迟 说明"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,4)]").text
        print(item)

    # 微信支付 页面

    # 支付宝支付 页面

    # 家长代付 页面
    @teststeps
    def wait_check_replace_page(self, var=20):
        """以“家长代付”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'家长代付')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wechat_replace_pay(self):
        """微信代付 tab"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,0)]")
        return item

    @teststeps
    def ali_replace_pay(self):
        """支付宝代付 tab"""
        item = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,0)]")[1]
        return item

    @teststeps
    def card_type(self):
        """卡的类型"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "card_type").text
        print(item)

    @teststeps
    def qr_code_hint(self):
        """wording：微信扫描二维码付款"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "pay_type_hint").text
        print(item)

    @teststeps
    def qr_code_judge(self):
        """微信二维码"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "qr_code")
            return True
        except Exception:
            return False

    @teststeps
    def pay_finish_tips(self):
        """支付完成 提示"""
        try:
            self.driver \
                .find_element_by_xpath("//android.widget.TextView[contains(@index,3)]")
            return True
        except Exception:
            return False

    @teststep
    def pay_finish_button(self):
        """支付完成 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "pay_complete").click()

    @teststeps
    def pay_statement(self):
        """收款公司 声明"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,5)]").text
        print(item)

    # 支付结果 页面  -支付失败
    @teststeps
    def wait_check_pay_result_page(self, var=20):
        """以“支付结果”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'支付结果')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def pay_result_img_judge(self):
        """支付结果页 图片"""
        try:
            self.driver \
                .find_element_by_id(self.id_type() + "pay_result_img")
            return True
        except Exception:
            return False

    @teststeps
    def pay_result(self):
        """付款结果"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "pay_result").text
        print(item)

    @teststeps
    def contact_services_tips(self):
        """联系客服 的提示"""
        item = self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@index,0)]").text
        print(item)

    @teststeps
    def qr_code_tips(self):
        """wording:"在线助教"客服二维码"""
        try:
            self.driver \
                .find_element_by_xpath("//android.widget.TextView[contains(@index,2)]")
            return True
        except Exception:
            return False

    # 支付结果 页面  -支付成功

    @teststeps
    def tips_goto_pay_operate(self):
        """去购买"""
        if self.wait_check_page(10):
            if self.img_judge():  # 判断图片 是否存在
                print('------------------------------')
                print('购买提示页：')
                self.tips_title()
                self.tips_content()
                self.goto_pay_button()  # 去购买 按钮

                self.buy_page_direct_operate()
                HomePage().click_back_up_button()  # 返回 购买提示页
                if self.wait_check_page(10):
                    self.goto_verification().click()  # 已有【提分版】， 去验证
                    Toast().find_toast('已更新账户信息')

    @teststeps
    def buy_page_direct_operate(self):
        """购买页 操作 -- 直接购买"""
        if self.wait_check_pay_page():  # 购买页 检查点
            print('------------------------------')
            print('购买页:')
            self.st_icon()  # 学生头像
            self.st_name()  # 学生name
            self.st_phone()  # 手机号

            self.buy_hint()  # 购买提示
            self.hint_info()  # 提分版 权力

            self.online_services_operate()  # 在线客服

            if self.wait_check_pay_page():
                check = self.check_button()  # 单选框
                for i in range(len(check)):
                    if GetAttribute().get_checked(check[i]) == 'true':
                        if i != 3:
                            print('❌❌❌ Error - 未默认选中 年卡')
                        else:
                            check[0].click()  # 选择季卡
                            if GetAttribute().get_checked(self.check_button()[0]) == 'true':
                                self.current_card()  # 左下角 目前选中的卡
                            else:
                                print('❌❌❌ Error - 未选中 月卡')

                card = self.card_name()  # 卡的类型
                price = self.card_price()  # 卡的价格

                if len(check) != len(card) != len(price) != 4:
                    print('❌❌❌ Error - 卡的个数有误', len(check), len(card), len(price))
                else:
                    print('--------------------')
                    for j in range(len(card)):
                        print(card[j].text, price[j].text)
                    print('--------------------')

                self.buy_agreement()  # 购买协议

                self.pay_confirm_operate()  # 支付确认页

    @teststeps
    def pay_confirm_operate(self):
        """支付确认页 操作"""
        direct = self.direct_buy_button()  # 直接购买 按钮
        if GetAttribute().get_enabled(direct) == 'true':
            direct.click()  # 点击 直接购买 按钮

            if self.wait_check_pay_confirm_page():  # 支付确认 页面检查点
                print('------------------------------')
                print('支付确认页:')
                self.st_icon()  # 学生头像
                self.st_name()  # 学生name
                self.st_phone()  # 手机号

                self.online_services_operate()  # 在线客服

                unit = self.price_unit()  # 货币单位
                print(unit, self.price_info())  # 价格
                self.card_hint()  # 卡的类型说明

                print('-----------------')
                self.pay_type()  # 支付方式
                icon = self.pay_icon()  # icon

                wechat_check = self.wechat_pay_check()  # 微信单选框
                if GetAttribute().get_checked(wechat_check) == 'false':
                    print('❌❌❌ Error - 未默认选中 微信支付')

                for k in range(1, len(icon)):
                    self.pay_mode(k)  # 支付方式
                print('-----------------')

                self.pay_delay_tips()  # 支付延迟 说明

                self.parent_replace_operate()  # 家长代付

    @teststeps
    def parent_replace_operate(self):
        """家长代付页 操作"""
        parent = self.parent_pay_check()  # 家长代付 单选框
        parent.click()
        self.confirm_pay_button()  # 确认支付 按钮
        if self.wait_check_replace_page():  # 家长代付页 检查点
            print('------------------------------')
            print('家长代付页:')

            wechat_tab = self.wechat_replace_pay()  # 微信代付
            if GetAttribute().get_selected(wechat_tab) == 'false':
                print('❌❌❌ Error - 未默认选中 微信代付')
            else:
                ali_tab = self.ali_replace_pay()  # 支付宝代付
                print(ali_tab.text)
                ali_tab.click()  # 切换到 支付宝代付
                if GetAttribute().get_selected(self.ali_replace_pay()) == 'false':
                    print('❌❌❌ Error - 未选中 支付宝代付')

            self.card_type()  # 卡的类型
            unit = self.price_unit(2)  # 货币单位
            print(unit, self.price_info())  # 价格

            if self.qr_code_judge():
                self.qr_code_hint()  # xx扫描二维码付款

            if not self.pay_finish_tips():  # 支付完成 提示
                print("❌❌❌ Error - 无支付完成 提示")
            self.pay_statement()  # 收款公司说明

            self.pay_finish_operate()  # 支付结果页

    @teststeps
    def pay_finish_operate(self):
        """支付结果页 操作"""
        self.pay_finish_button()  # 支付完成 按钮
        if self.wait_check_pay_result_page():  # 支付结果页 检查点
            print('------------------------------')
            print('支付结果页:')
            if self.pay_result_img_judge():
                self.pay_result()  # 支付结果
                self.contact_services_tips()  # 联系客服的提示
                if self.img_judge():
                    if not self.qr_code_tips():  # "在线助教"客服二维码
                        print('❌❌❌ Error - 无文案："在线助教"客服二维码')

    @teststeps
    def online_services_operate(self):
        """在线客服"""
        self.online_service()  # 点击在线客服
        if self.wait_check_help_page():
            HomePage().click_back_up_button()
