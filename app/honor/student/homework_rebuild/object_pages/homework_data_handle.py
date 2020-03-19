#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/9 15:45
# -----------------------------------------
from app.honor.student.homework_rebuild.object_pages.homework_sql import HomeworkSql
from conf.base_page import BasePage
from conf.decorator import teststep


class HomeworkDataHandle(BasePage):

    def __init__(self):
        self.mysql = HomeworkSql()


    @teststep
    def delete_student_homework_data(self, stu_id):
        """删除学生作业相关信息"""
        self.mysql.delete_student_homework_overview(stu_id)
        self.mysql.delete_student_homework_record(stu_id)
        self.mysql.delete_student_homework_wrong(stu_id)
        self.mysql.update_homework_complete_data(stu_id)