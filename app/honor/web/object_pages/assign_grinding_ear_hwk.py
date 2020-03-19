import time

from app.honor.web.object_pages.assign_homework import AssignHomeworkPage
from app.honor.web.object_pages.login_page import LoginWebPage
from app.honor.web.test_data.teacher_account import TeacherAccount
from conf.decorator import teststep


class AssignGrindEarHomeWork(AssignHomeworkPage):
    @teststep
    def clear_blanket_operate(self):
        blanket_bank_num = self.blanket_bank_num()
        if blanket_bank_num:
            self.blanket_tab().click()
            if self.wait_check_blanket_page():
                self.blanket_page_select_all_checkbox().click()
                self.multi_like_or_delete_btn()[0].click()
                self.tip_box_operate()
            self.click_logo()


    @teststep
    def put_my_like_banks_into_blanket(self):
        """将收藏的大题放入题筐"""
        if self.wait_check_home_page():
            self.mine_bank_pool().click()
            time.sleep(1)
            self.mine_pool_bank_type_tab()[1].click()
            time.sleep(5)
            self.tag_list()[0].click()
            time.sleep(2)
            self.select_all_checkbox().click()
            self.join_blanket().click()
            self.tips_operate()
            self.select_all_checkbox().click()
            self.join_blanket().click()
            time.sleep(3)

    @teststep
    def build_homework_from_blanket(self):
        """从题筐中大题生成作业并布置"""
        self.blanket_tab().click()
        if self.wait_check_blanket_page():
            self.blanket_page_select_all_checkbox().click()
            self.bank_control_btn()[-1].click()
            self.tip_box_operate()
            if self.wait_check_assign_homework_page():
                self.homework_name_input_warp().send_keys('口语测试作业')
                self.select_test_class()
                self.publish_homework()
                self.tips_operate()
            if self.wait_check_empty_blanket_page():
                self.click_logo()


    @teststep
    def assign_grind_ear_hwk_operate(self):
        LoginWebPage().login_operate(TeacherAccount.Account[-1][0],
                                     TeacherAccount.Account[-1][1])         # 登陆操作
        hwk_name = '口语测试作业'
        self.clear_blanket_operate()
        self.delete_homework_operate(hwk_name)
        self.click_logo()
        time.sleep(2)
        self.put_my_like_banks_into_blanket()
        self.build_homework_from_blanket()