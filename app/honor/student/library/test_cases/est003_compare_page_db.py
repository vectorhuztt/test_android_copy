#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/5/31 9:32
# -----------------------------------------
import random
import re
import unittest

from app.honor.student.library.object_page.library_page import LibraryPage
from app.honor.student.library.object_page.library_data_handle import DataHandlePage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.login.object_page.login_page import LoginPage
from conf.base_page import BasePage
from conf.decorator import setup, teardown, testcase
from utils.assert_func import ExpectingTest


class CompareDb(unittest.TestCase):
    """标签核实"""

    @classmethod
    @setup
    def setUp(cls):
        """启动应用"""
        cls.result = unittest.TestResult()
        cls.base_assert = ExpectingTest(cls, cls.result)
        cls.login = LoginPage()
        cls.home = HomePage()
        cls.data = DataHandlePage()
        cls.library = LibraryPage()
        BasePage().set_assert(cls.base_assert)
        cls.login.app_status()

    @teardown
    def tearDown(self):
        for x in self.base_assert.get_error():
            self.result.addFailure(self, x)

    def run(self, result=None):
        self.result = result
        super(CompareDb, self).run(result)

    @testcase
    def test_compare_page_data(self):
        """对比页面数据，查看是否与数据库一致"""
        if self.home.wait_check_home_page():
            user_info = UserCenterPage().get_user_info()
            school_id = user_info[2]
            school_name = user_info[1]
            if self.home.wait_check_home_page():
                self.home.check_more()[0].click()
                if self.library.wait_check_library_page(school_name):
                    label_names = self.library.label_name()
                    select_label = random.choice([x.text for x in label_names if x.text != '其他'])
                    print('选择标签：', select_label)
                    label_id = self.data.get_library_label_id(school_id, select_label)
                    print('label_id:', label_id)
                    label_book_info = self.data.get_label_book_list(school_id, label_id)
                    print('label_book_info:', label_book_info)

                    self.library.course_more_btn(select_label).click()
                    book_name_list = [label_book_info[x][0] for x in label_book_info]
                    tips = []
                    while True:
                        if self.library.wait_check_test_label_page(select_label):
                            label_book_names = self.library.book_names()
                            for x in label_book_names:
                                if self.library.wait_check_test_label_page(select_label):
                                    if x.text in tips:
                                        continue
                                    else:
                                        tips.append(x.text)
                                        print('书籍：', x.text)
                                        x.click()
                                        if self.library.wait_check_book_page():
                                            book_name = self.library.book_title()
                                            total_set_count = int(re.findall(r'\d+', self.library.book_set_num())[0])
                                            book_desc = self.library.book_summary()
                                            book_id = self.data.get_book_id_by_name_and_desc(school_id, book_name, book_desc)
                                            if book_name not in book_name_list:
                                                self.base_assert.except_error("此书不在该标签中 " + book_name)
                                            set_tip = []
                                            bookset_ids = label_book_info[book_id][1]
                                            bookset_name_list = self.data.get_book_book_set_list(bookset_ids)

                                            while len(set_tip) < total_set_count:
                                                book_page_set_names = self.library.book_names()
                                                for y in book_page_set_names:
                                                    if self.library.wait_check_book_page():
                                                        if y.text in set_tip:
                                                            continue
                                                        else:
                                                            set_tip.append(y.text)
                                                            page_set_name = y.text
                                                            print(page_set_name, end=' | ')
                                                            y.click()
                                                            if self.library.wait_check_book_set_page():
                                                                bookset_name = self.library.book_title()
                                                                if bookset_name not in bookset_name_list:
                                                                    self.base_assert.except_error('此书单不在该书下的书单列表中， 但是在该书下展现 ' + book_name)
                                                                self.library.click_back_up_button()
                                                            else:
                                                                print('未进入书单页面 ', page_set_name)
                                                if self.library.wait_check_book_page():
                                                    self.library.screen_swipe_up(0.6, 0.9, 0.6, 1000)
                                        self.library.click_back_up_button()
                                        print('\n', '-'*30, '\n')
                        if self.library.wait_check_end_tip_page():
                            break
                        else:
                            self.library.screen_swipe_up(0.5, 0.9, 0.4, 1000)











