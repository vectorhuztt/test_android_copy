#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/27 10:43
# -----------------------------------------
from utils.sql import SqlDb


class PunchSql(SqlDb):
    def find_class_activity(self, class_id):
        """查询班级活动id"""
        sql = "SELECT `id`, template_id FROM activity WHERE id in (SELECT activity_id FROM activity_vanclass_map WHERE vanclass_id = '{}') " \
              "and deleted_at is NULL and DATEDIFF(end_at, NOW()) >=0".format(class_id)
        return self.execute_sql_return_result(sql)

    def find_activity_name_by_id(self, activity_id):
        """根据活动id查询名称"""
        sql = "SELECT `name` FROM activity WHERE `id`={}".format(activity_id)
        return self.execute_sql_return_result(sql)

    def find_activity_book_name_by_template_id(self, template_id):
        """根据template_id 获取书籍id和名称"""
        sql = "SELECT id, item_count FROM library_books WHERE id in (SELECT item_id FROM " \
              "activity_template_item_map WHERE template_id = {})".format(template_id)
        return self.execute_sql_return_result(sql)

    def find_library_quoted_book_origin_id_by_id(self, quoted_id):
        sql = "SELECT origin_id FROM library_quoted_books WHERE id ='{}'".format(quoted_id)
        return self.execute_sql_return_result(sql)

    def delete_student_activity_book_record(self, stu_id, activity_id):
        """删除学生活动书籍记录"""
        sql = "DELETE FROM activity_student_book_record where student_id = {} and activity_id = {}".format(stu_id, activity_id)
        return self.execute_sql_only(sql)

    def delete_student_activity_book_review(self, stu_id, activity_id):
        """删除学生活动书籍"""
        sql = "DELETE FROM activity_student_books WHERE student_id = {} AND activity_id ={}".format(stu_id, activity_id)
        return self.execute_sql_only(sql)

    def delete_student_activity_book_wrong_record(self, stu_id, activity_id):
        sql = "DELETE FROM activity_student_book_wrong WHERE student_id = {} AND activity_id ={}".format(stu_id, activity_id)
        return self.execute_sql_only(sql)

    def delete_student_activity_overview(self, stu_id, activity_id):
        """删除学生活动进度"""
        sql = "DELETE FROM activity_student_overview WHERE student_id = {} AND activity_id ={}".format(stu_id, activity_id)
        return self.execute_sql_only(sql)