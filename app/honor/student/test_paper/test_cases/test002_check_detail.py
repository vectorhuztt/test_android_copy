# coding=utf-8
import unittest

from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.test_paper.object_page.exam_sql_handle import DataPage
from app.honor.student.test_paper.object_page.exam_detail import DetailPage
from app.honor.student.test_paper.object_page.exam_page import ExamPage
from conf.base_page import BasePage
from conf.decorator import setup, teststeps, teardown
from utils.assert_func import ExpectingTest


class ExamDetail(unittest.TestCase):
    """试卷"""
    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login = LoginPage()
        cls.exam = ExamPage()
        cls.detail = DetailPage()
        cls.login.app_status()  # 判断APP当前状态
        cls.common = DataPage()
        BasePage().set_assert(cls.base_assert)

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ExamDetail, self).run(result)

    @teststeps
    def test_check_exam_detail(self):
        """查看试卷详情"""
        if self.home.wait_check_home_page():
            nick_name = UserCenterPage().get_user_info()[-1]
            if self.home.wait_check_home_page():  # 页面检查点
                print('进入主界面')
                self.home.click_hk_tab(3)  # 点击 做试卷
            if self.detail.wait_check_exam_title_page():
                exam_name = self.exam.select_one_exam()
                data_json = self.common.get_data_json_from_file()
                exam_data = data_json[exam_name]
                if self.exam.wait_check_rank_page():
                    self.detail.rank_page_operate(nick_name)
                if self.exam.wait_check_rank_page():
                    self.detail.check_detail()
                    if self.detail.wait_check_detail_page():
                        self.detail.check_ques_detail(exam_data)
                        self.home.click_back_up_button()
                        if self.detail.wait_check_rank_page():
                            self.home.click_back_up_button()






