#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/27 14:32
# -----------------------------------------
from app.honor.student.punch_activity.object_page.punch_sql import PunchSql


class PunchSqlHandle:

    def __init__(self):
        self.mysql = PunchSql()

    def get_activity_info_by_class_id(self, class_id):
        """根据班级id获取当前班级的打卡活动"""
        result = self.mysql.find_class_activity(class_id)
        return result[0] if result else 0

    def get_activity_name_by_id(self, activity_id):
        """获取当前打卡活动的名称"""
        result = self.mysql.find_activity_name_by_id(activity_id)
        return result[0][0]

    def get_activity_book_by_template_id(self, template_id):
        """根据template id获取活动书籍信息"""
        result = self.mysql.find_activity_book_name_by_template_id(template_id)
        return {x[0]: x[1] for x in result}

    def get_activity_book_id_by_quoted_id(self, quoted_id):
        """根据图书id获取对应活动中书籍id"""
        result = self.mysql.find_library_quoted_book_origin_id_by_id(quoted_id)
        return result[0][0]

    def delete_student_activity_record(self, stu_id, activity_id):
        """删除学生活动记录"""
        self.mysql.delete_student_activity_book_record(stu_id, activity_id)
        self.mysql.delete_student_activity_book_review(stu_id, activity_id)
        self.mysql.delete_student_activity_book_wrong_record(stu_id, activity_id)
        self.mysql.delete_student_activity_overview(stu_id, activity_id)

    def get_has_punch_activity_class(self, class_ids):
        """获取有打卡活动的班级"""
        activity_class = {}
        for x in class_ids:
            activity_info = self.get_activity_info_by_class_id(x)
            if activity_info:
                activity_class[x] = {}
                activity_id = activity_info[0]
                activity_name = self.get_activity_name_by_id(activity_id)
                activity_class[x]['活动名称'] = activity_name
                activity_class[x]['活动id'] = activity_id
                template_id = activity_info[1]
                book_info = self.get_activity_book_by_template_id(template_id)
                activity_class[x]['书籍信息'] = book_info
        return activity_class

