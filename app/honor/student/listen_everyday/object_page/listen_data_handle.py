#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 15:48
# -----------------------------------------
from app.honor.student.listen_everyday.object_page.listen_sql import ListenSql
from conf.decorator import teststep


class ListenDataHandle:

    def __init__(self):
        self.mysql = ListenSql()

    @teststep
    def delete_student_all_listening_records(self, stu_id):
        """删除听力记录"""
        # 删除听力记录表中数据
        self.mysql.delete_student_listen_record(stu_id)
        # 删除听力状态记录
        self.mysql.delete_student_listen_status_record(stu_id)
        # 删除听力错题记录
        self.mysql.delete_student_listening_wrong(stu_id)