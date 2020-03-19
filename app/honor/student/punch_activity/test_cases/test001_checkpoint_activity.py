#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/27 13:59
# -----------------------------------------

import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.punch_activity.object_page.punch_page import PunchActivityPage
from app.honor.student.punch_activity.object_page.punch_sql_handle import PunchSqlHandle
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class CheckPointTest(unittest.TestCase):
    @classmethod
    @setup
    def setUp(cls):
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.punch = PunchActivityPage()
        cls.login = LoginPage()
        cls.data = PunchSqlHandle()
        cls.home = HomePage()
        BasePage().set_assert(cls.base_assert)
        cls.login.app_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(CheckPointTest, self).run(result)


    @testcase
    def test_checkpoint_activity(self):
        if self.punch.wait_check_alert_punch_tip_page():
            self.punch.click_alert_tip()
            if not self.punch.wait_check_activity_book_item_page():
                self.base_assert.except_error("点击主页的打卡弹框未进入打卡页面")
            else:
                self.punch.punch_page_back_icon().click()

        if not self.home.wait_check_home_page():
            self.base_assert.except_error('在打卡页面点击退回页面未进入主页面')
        else:
            stu_info = UserCenterPage().get_user_info()
            stu_id = stu_info[0]
            nickname = stu_info[-1]
            class_ids = VanclassPage().get_vanclass_id()
            print('学生班级id：', class_ids)
            activity_class_info = self.data.get_has_punch_activity_class(class_ids)
            print('打开活动班级信息：', activity_class_info, '\n')
            if self.home.wait_check_home_page():
                self.punch.home_page_punch_tab().click()
                class_activity_book_info = self.punch.checkpoint_core_process(stu_id, activity_class_info)
                select_quoted_id = self.punch.punch_page_select_book_operate(class_activity_book_info, nickname)
                self.punch.checkpoint_page_operate(nickname, select_quoted_id)





