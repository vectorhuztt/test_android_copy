#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 15:44
# -----------------------------------------
from utils.sql import SqlDb


class LibrarySql(SqlDb):
    # ============================= 图书馆sql相关操作 ====================================

    def find_school_id(self, school_name):
        """查询学校id"""
        sql = 'SELECT id FROM school WHERE `name`= "{}"'.format(school_name)
        return self.execute_sql_return_result(sql)

    def find_school_id_by_short_name(self, short_name):
        """根据学校简称获取学校id"""
        sql = 'SELECT school_id FROM `school_attribute` WHERE `key`="short_name" AND `value`="{}"'.format(short_name)
        return self.execute_sql_return_result(sql)

    def find_library_label_id_by_name(self, school_id, label_name):
        """获取学校或者系统的标签名称和id"""
        sql = 'SELECT `id` FROM school_label WHERE `school_id` = {} and type= "library"' \
              'and `name` = "{}"'.format(school_id, label_name)
        print(sql)
        return self.execute_sql_return_result(sql)

    def find_label_book_set_list(self, school_id, label_id):
        """根据学校id, 标签id 获取书籍名称"""
        sql = "SELECT `id`, `name`, item_ids FROM library_books WHERE school_id ={} and `label_ids` LIKE '%{}%' and deleted_at is NULL " \
              "and school_visible=1".format(school_id, label_id)
        return self.execute_sql_return_result(sql)

    def find_book_name_by_id(self, book_id):
        sql = "SELECT `name` FROM library_books where id in ({})".format(book_id)
        return self.execute_sql_return_result(sql)

    def find_book_id_by_name_and_desc(self, school_id, book_name, desc):
        """根据图书id"""
        sql = "SELECT `id` FROM library_books WHERE school_id ={} and `name` = '{}' " \
              "and description = '{}' and type='book_set'".format(school_id, book_name, desc)
        return self.execute_sql_return_result(sql)

    def find_book_set_ids(self, book_name, book_description):
        """查询学生今日是否对本书提交过大题"""
        sql = 'SELECT item_ids from library_books where `name`="{}" and description="{}"'.format(book_name, book_description)
        return self.execute_sql_return_result(sql)

    def find_student_book_today_study_record(self, stu_id,  set_ids):
        """查询书籍下任意书单的学习记录"""
        sql = 'SELECT id FROM library_student_book_record WHERE `student_id` ={}  and ' \
              'DATEDIFF(start_time,NOW())=0 and book_id in ({})'.format(stu_id, set_ids)
        print(sql)
        return self.execute_sql_return_result(sql)

