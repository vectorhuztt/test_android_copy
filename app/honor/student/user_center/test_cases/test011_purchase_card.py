# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/11 16:40
# -------------------------------------------
import unittest

from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.user_center.object_page.buy_card_page import PurchasePage
from conf.decorator import setupclass, teardownclass, teststeps, teardown
from utils.assert_func import ExpectingTest


class PurchaseCard(unittest.TestCase):
    """购买"""
    @classmethod
    @setupclass
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.buy = PurchasePage()
        cls.login.set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(PurchaseCard, self).run(result)

    @teststeps
    def test_purchase_card(self):
        self.login.app_status()  # 判断APP当前状态

        if self.buy.home.wait_check_home_page():
            self.buy.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.buy.user_center.wait_check_user_center_page():  # 页面检查点
                self.buy.user_center.click_buy()
                if self.buy.wait_check_buy_page():
                    self.buy.magics_page_ele_operate()
                    # self.buy.magic_ele_check()
                    self.buy.online_server_ele_check()

                    if self.buy.wait_check_buy_page():
                        self.buy.upgrade_button().click()
                        if self.buy.wait_check_card_page():
                            self.buy.buy_page_ele_operate()
                            self.buy.switch_card()
                            self.buy.check_agreement()
                            self.buy.direct_buy()
                            self.buy.back_to_home()






