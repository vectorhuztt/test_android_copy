#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/27 9:40
# -----------------------------------------
from app.honor.student.word_book.object_page.check_word_sql import CheckWordSql
from conf.decorator import teststep


class CheckSqlHandle:

    def __init__(self):
        self.mysql = CheckWordSql()

    @teststep
    def get_interval(self, level):
        if level == 1:
            interval = 1
        elif level == 2:
            interval = 10
        elif level == 3:
            interval = 30
        elif level == 4:
            interval = 60
        else:
            interval = 0

        return interval

    @teststep
    def get_student_words_count(self, stu_id):
        """获取学生已背单词数"""
        count = self.mysql.find_student_words_count(stu_id)
        return count[0][0] if count else 0

    @teststep
    def get_student_new_word(self, stu_id, push_type):
        """获取老师布置新词"""
        teacher_new_word = self.mysql.find_student_new_word(stu_id, push_type)
        return [x[0] for x in teacher_new_word] if teacher_new_word else []

    @teststep
    def get_all_recite_count(self, stu_id, level):
        """获取老师复习和系统复习的单词个数"""
        interval = self.get_interval(level)
        count = self.mysql.find_student_all_recite_count(stu_id, level, interval)
        return count[0][0] if count else 0

    @teststep
    def get_different_recite_count(self, stu_id, level, push_type):
        """根据布置身份确定复习个数"""
        interval = self.get_interval(level)
        count = self.mysql.find_student_different_recite_count(stu_id, level, interval, push_type)
        return count[0][0] if count else 0

    @teststep
    def get_student_today_word_data(self, stu_id):
        """获取学生今天背单词数据"""
        data = self.mysql.find_today_student_word(stu_id)
        word_data = [x[0] for x in data]
        return word_data

    @teststep
    def get_student_recite_count(self, stu_id):
        """获取学生需要复习单词个数"""
        teacher_new_words = self.get_student_new_word(stu_id, 1)
        all_recite_count = sum([self.get_all_recite_count(stu_id, x) for x in range(1, 5)])
        teacher_recite_count = sum([self.get_different_recite_count(stu_id, x, 1) for x in range(1, 5)])
        sys_recite_count = sum([self.get_different_recite_count(stu_id, x, 0) for x in range(1, 5)])

        print('老师剩余布置新词个数：', len(teacher_new_words))
        print('老师复习单词个数：', teacher_recite_count)
        print('系统复习单词个数：', sys_recite_count)
        print('老师 + 系统 复习单词个数：', all_recite_count)

        if len(teacher_new_words) >= 3:
            if teacher_recite_count:
                recite_count = teacher_recite_count
            else:
                recite_count = sys_recite_count
        else:
            recite_count = all_recite_count

        print('最终计算复习单词个数：', recite_count)
        return recite_count




