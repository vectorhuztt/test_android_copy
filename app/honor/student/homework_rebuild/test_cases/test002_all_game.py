#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/18 11:38
# -----------------------------------------
import unittest
from ddt import ddt, data, unpack
from app.honor.student.homework_rebuild.object_pages.homework_data_handle import HomeworkDataHandle
from app.honor.student.homework_rebuild.object_pages.homework_game_page import HomeworkGameOperate
from app.honor.student.homework_rebuild.test_data.homework_type_page import HomeworkTypePage as ht
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


@ddt
class PlayAllGame(unittest.TestCase):
    """练习所有游戏"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.home = HomePage()
        cls.login_page = LoginPage()
        cls.library = LibraryGamePage()
        BasePage().set_assert(cls.base_assert)
        cls.login_page.app_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(PlayAllGame, self).run(result)

    @data(
        # ['单词跟读游戏', '单词跟读'],
        # [ht.HW1, '闪卡练习'],
        # [ht.HW1, '猜词游戏'],
        # [ht.HW1, '还原单词'],
        # [ht.HW1, '连连看'],
        # [ht.HW2, '单项选择'],
        # [ht.HW2, '单词听写'],
        # [ht.HW2, '连词成句'],
        # [ht.HW2, '单词拼写'],
        # [ht.HW2, '选词填空'],
        # [ht.HW3, '词汇选择'],
        # [ht.HW3, '听音选图'],
        # [ht.HW3, '句型转换'],
        # [ht.HW3, '听后选择'],
        # [ht.HW4, '强化炼句'],
        # [ht.HW4, '听音连句'],
        # [ht.HW4, '完形填空'],
        # [ht.HW4, '阅读理解'],
        # [ht.HW4, '补全文章'],
    )
    @unpack
    @testcase
    def test_all_game(self, hw_name, bank_type):
        if self.home.wait_check_home_page():
            nickname = 0
            try:
                user_info = UserCenterPage().get_user_info()
                stu_id = user_info[0]
                nickname = user_info[-1]
                HomeworkDataHandle().delete_student_homework_data(stu_id)
            except:
                self.base_assert.except_error("删除作业记录失败")

            if self.home.wait_check_home_page():
                self.home.click_hk_tab(index=2)
                self.library.enter_into_game(hw_name, bank_type)
                bank_list = self.library.bank_name_by_type(bank_type)
                for i in range(len(bank_list)):
                    if self.library.wait_check_bank_list_page():
                        bank_name = self.library.bank_name_by_type(bank_type)[i].text
                        bank_progress = self.library.bank_progress_by_name(bank_name)
                        print('大题名称：', bank_name, '大题进度：', bank_progress)
                        self.library.click_bank_by_name(bank_name)
                        HomeworkGameOperate().homework_game_operate(nickname)

                if self.library.wait_check_bank_list_page():
                    self.library.click_back_up_button()
                    if self.library.wait_check_homework_list_page():
                        self.library.click_back_up_button()




