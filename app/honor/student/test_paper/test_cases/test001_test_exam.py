# coding=utf-8
import unittest

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from app.honor.student.test_paper.object_page.exam_sql_handle import DataPage
from app.honor.student.test_paper.object_page.exam_page import ExamPage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.web.object_pages.driver import Driver
from app.honor.web.object_pages.resign_exam_page import ResignExamPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class ExamProcess(unittest.TestCase):
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
        cls.login.app_status()  # 判断APP当前状态
        cls.common = DataPage()
        BasePage().set_assert(cls.base_assert)
        cls.common.write_json_to_file({})

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(ExamProcess, self).run(result)

    @testcase
    def test_play_exam_game_progress(self):
        """做试卷"""
        # 删除所有试卷 重新布置
        # if self.home.wait_check_home_page():
        #     stu_id = UserCenterPage().get_user_info()[0]
        #     self.common.delete_student_exam_record(stu_id)
        #
        # web_driver = Driver()
        # web_driver.set_driver()
        ResignExamPage().reassign_exam_operate()      # web端随机布置一套试卷
        # web_driver.quit_web()

        if self.home.wait_check_home_page():          # 页面检查点
            print('进入主界面')
            self.home.click_hk_tab(3)                   # 点击 做试卷
            if self.exam.wait_check_exam_title_page():
                test_name = self.exam.select_one_exam()
                data_json = self.common.get_data_json_from_file()
                data_json[test_name] = {}
                if self.exam.wait_check_exam_confirm_page():
                    total = self.exam.exam_confirm_ele_operate()
                    self.exam.click_start_exam_button()
                    tips = self.exam.get_ques_name(int(total))
                    self.exam.play_examination(tips, data_json[test_name])
                    self.common.write_json_to_file(data_json)
