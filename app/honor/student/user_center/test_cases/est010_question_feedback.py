# coding=utf-8
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.login.test_data.login_failed_toast import VALID_LOGIN_TOAST
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage, Setting, QuestionFeedback
from conf.decorator import setup, teardown, testcase
from utils.toast_find import Toast


class ProblemFeedback(unittest.TestCase):
    """问题反馈"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.user_center = UserCenterPage()
        cls.setting = Setting()
        cls.question = QuestionFeedback()

    @classmethod
    @teardown
    def tearDown(cls):
        pass

    @testcase
    def test_question_feedback(self):
        self.login.app_status()  # 判断APP当前状态

        if self.home.wait_check_home_page():  # 页面检查点
            self.home.click_tab_profile()  # 进入首页后点击‘个人中心’按钮

            if self.user_center.wait_check_user_center_page():  # 页面检查点
                self.user_center.click_setting()  # 进入设置页面
                if self.setting.wait_check_page():
                    self.setting.question_feedback()  # 进入问题反馈页面

                    if self.question.wait_check_page():
                        self.question.edit_text().send_keys(r"123vxc567问题")
                        self.question.submit_button()
                        print('反馈的问题：', '123vxc567问题')

                        if self.setting.wait_check_page():
                            print('submit question success')
                        else:
                            print(' failed to submit question ')

                        self.setting.back_up()  # 返回主界面
                    else:
                        print("未进入问题反馈页面")
        else:
            Toast().find_toast(VALID_LOGIN_TOAST.login_failed())
            print("未进入主界面")
