# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/4/2 15:04
# -------------------------------------------
from app.honor.student.library.object_page.library_sql import LibrarySql
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep


class DataHandlePage(BasePage):

    mysql = LibrarySql()
    user = UserCenterPage()
    home = HomePage()

    @teststep
    def get_library_label_id(self, school_id, label_name):
        """获取图书馆标签id"""
        result = self.mysql.find_library_label_id_by_name(school_id, label_name)
        return result[0][0] if result else -1

    @teststep
    def get_label_book_list(self, school_id, label_id):
        """根据标签id获取图书id"""
        result = self.mysql.find_label_book_set_list(school_id, label_id)
        return {x[0]: (x[1], x[2]) for x in result}

    @teststep
    def get_book_book_set_list(self, book_id):
        """获取书籍下所有书单名称"""
        result = self.mysql.find_book_name_by_id(book_id)
        return [x[0] for x in result]

    @teststep
    def get_book_id_by_name_and_desc(self, school_id, book_name, description):
        """根据图书名称和图书简介获取图书id"""
        result = self.mysql.find_book_id_by_name_and_desc(school_id, book_name, description)
        return result[0][0]


    def student_today_is_submit_bank_record(self, stu_id,  book_name, book_description):
        """查询此书籍的书单该学生今日是否已经学习过"""
        book_set_ids = self.mysql.find_book_set_ids(book_name, book_description)
        if book_set_ids:
            reform_book_set_ids = str(book_set_ids[0][0].split(',')).replace('[', '').replace(']', '')
            book_record = self.mysql.find_student_book_today_study_record(stu_id, reform_book_set_ids)
            print('book_record', book_record)
            if len(book_record):
                return True
            else:
                return False
        else:
            return False













