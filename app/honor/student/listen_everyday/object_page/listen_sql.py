#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 15:48
# -----------------------------------------
from utils.sql import SqlDb


class ListenSql(SqlDb):
    #  -------- 删除作业记录操作 ------------------
    def delete_student_listen_status_record(self, stu_id):
        sql = 'DELETE FROM listening_student_status_record WHERE `student_id` = {}'.format(stu_id)
        self.execute_sql_only(sql)

    def delete_student_listen_record(self, stu_id):
        sql = 'DELETE FROM `listening_student_record` WHERE `student_id` = {}'.format(stu_id)
        self.execute_sql_only(sql)

    def delete_student_listening_wrong(self, stu_id):
        sql = 'DELETE FROM `listening_student_wrong` WHERE `student_id` = {}'.format(stu_id)
        self.execute_sql_only(sql)