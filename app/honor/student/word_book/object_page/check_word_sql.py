#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/27 9:36
# -----------------------------------------
from utils.sql import SqlDb


class CheckWordSql(SqlDb):

    def find_student_words_count(self, stu_id):
        """查询学生已背单词个数"""
        sql = "SELECT count(*) FROM word_student_fluency WHERE student_id = {}  and fluency_level >= 1".format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_student_all_recite_count(self, stu_id, level, interval):
        """查询各个等级的复习单词"""
        sql = 'SELECT count(*) FROM word_student_fluency wst, wordbank WHERE wst.wordbank_id = ' \
              'wordbank.id  AND student_id = {}  AND fluency_level = {} AND ' \
              'DATEDIFF( now( ), wst.last_finish_at) >={} and wst.deleted_at is NULL'.format(stu_id, level, interval)
        return self.execute_sql_return_result(sql)

    def find_student_different_recite_count(self, stu_id, level, interval, push_type):
        """查询不同身份复习的单词个数"""
        sql = 'SELECT count(*) FROM word_student_fluency wst, wordbank WHERE wst.wordbank_id = ' \
              'wordbank.id  AND student_id = {}  AND fluency_level = {} AND ' \
              'DATEDIFF( now( ), wst.last_finish_at) >={} and wst.deleted_at is NULL and is_system = {}'\
              .format(stu_id, level, interval, push_type)
        return self.execute_sql_return_result(sql)

    def find_student_new_word(self, stu_id, push_type):
        """查询老师布置的新词个数"""
        sql = 'SELECT vocabulary FROM wordbank, word_student_fluency wsf WHERE wordbank.id = wsf.wordbank_id ' \
              'and wsf.student_id= {} and wsf.is_system = {} and wsf.fluency_level = 0'.format(stu_id, push_type)
        return self.execute_sql_return_result(sql)

    def find_today_student_word(self, stu_id):
        """查询学生今日已被单词数据"""
        sql = 'SELECT `value` FROM user_word_data WHERE account_id = "{}"'.format(stu_id)
        return self.execute_sql_return_result(sql)