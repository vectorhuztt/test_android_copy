#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/9 15:34
# -----------------------------------------
from utils.sql import SqlDb


class HomeworkSql(SqlDb):

    def delete_student_homework_record(self, stu_id):
        """删除 homework_student_record中有关学生的数据"""
        sql = 'DELETE FROM  `homework_student_record` WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_homework_wrong(self, stu_id):
        """删除homework_student_wrong 表中学生数据"""
        sql = 'DELETE FROM `homework_student_wrong` WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_homework_overview(self, stu_id):
        """删除homework_student_overview 表中学生数据"""
        sql = 'DELETE FROM `homework_student_overview` WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def update_homework_complete_data(self, stu_id):
        """更改班级作业数据，更改作业完成进度"""
        sql = 'UPDATE `vanclass_student_homework` SET `is_finish` = 0, `completion_rate` = 0, ' \
              '`is_finish_for_teacher` = 0, `completion_rate_for_teacher` = 0, `finished_at` = NULL ' \
              'WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)
