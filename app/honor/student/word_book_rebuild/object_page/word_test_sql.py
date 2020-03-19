#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/29 15:58
# -----------------------------------------
from utils.sql import SqlDb


class WordTestSql(SqlDb):
    def find_f_glt_3_count(self, stu_id):
        """查询单词F值>=3的个数"""
        sql = "SELECT count(DISTINCT(wordbank_id)) FROM word_student_fluency WHERE student_id = {} " \
              "and fluency_level >=3 and deleted_at is NULL".format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_f_glt_3_words(self, stu_id):
        """获取F值大于3的单词 按照与今日时间差相比"""
        sql = 'SELECT DISTINCT(wordbank_id)  FROM word_student_fluency WHERE student_id = {} and fluency_level >=3 and deleted_at is NULL and ' \
              'translation_id not in(SELECT translation_id FROM word_student_test_overview WHERE student_id = {} and deleted_at is NULL) ' \
              'ORDER BY fluency_level asc, last_finish_at desc, id desc'.format(stu_id, stu_id)
        return self.execute_sql_return_result(sql)

    def find_test_fail_pass_words(self, stu_id):
        """查询测试未通过单词"""
        sql = 'SELECT wt.wordbank_id from word_student_test_overview wt, ' \
              'word_student_fluency wf WHERE wf.student_id=wt.student_id and wt.wordbank_id =wf.wordbank_id  and wt.translation_id = ' \
              'wf.translation_id and wt.student_id = {} and wt.deleted_at is NULL and wt.is_last_correct = 1 ' \
              'ORDER BY fluency_level asc, wt.last_finish_at desc, wt.id desc'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_test_success_pass_words(self, stu_id):
        """查询测试通过单词"""
        sql = 'SELECT wt.wordbank_id from word_student_test_overview wt, ' \
              'word_student_fluency wf WHERE wf.student_id=wt.student_id and wt.wordbank_id =wf.wordbank_id  and wt.translation_id = ' \
              'wf.translation_id and wt.student_id = {} and wt.deleted_at is NULL and wt.is_last_correct = 1 ' \
              'ORDER BY fluency_level asc , wt.last_finish_at desc, wt.id desc'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_student_translation_by_word_id(self, stu_id, words_id):
        """根据学生id, 单词id查询对应的解释id"""
        sql = "SELECT translation_id, fluency_level FROM word_student_fluency where student_id ={} and wordbank_id = {}" \
              " and fluency_level >=3 and deleted_at is NULL ".format(stu_id, words_id)
        return self.execute_sql_return_result(sql)

    def find_student_word_fvalue_by_word_explain_id(self, stu_id, word_id, explain_id):
        """根据学生id, 单词id，解释id, 定位F值"""
        sql = 'SELECT fluency_level FROM word_student_fluency WHERE student_id={} ' \
              'and wordbank_id={} and translation_id = {}'.format(stu_id, word_id, explain_id)
        return self.execute_sql_return_result(sql)

    def find_student_start_score_data(self, stu_id):
        """查询学生的星星积分"""
        sql = "SELECT `key`, `value` FROM user_student_data WHERE user_account_id={} ORDER BY " \
              "created_at desc limit {}".format(stu_id, 2)
        return self.execute_sql_return_result(sql)

    def find_test_result_data(self, test_id):
        """查询结果页结果"""
        sql = "SELECT right_count, wrong_count, DATE_FORMAT(spend_time, '%H:%i:%S'), accuracy, wrong_ids, right_ids FROM " \
              "word_student_test_record WHERE test_id = {} order by  created_at desc limit 1".format(test_id)
        return self.execute_sql_return_result(sql)

    def find_test_translation_by_word_ids(self, test_id, wordbank_ids):
        """根据单词id查询对应的解释id"""
        sql = 'SELECT translation_id FROM word_student_test_item_map where test_id = {} ' \
              'and wordbank_id in ({})'.format(test_id, wordbank_ids)
        return self.execute_sql_return_result(sql)

    def find_student_test_id(self, stu_id):
        sql = "SELECT `id` FROM word_student_test where student_id = {}".format(stu_id)
        return self.execute_sql_return_result(sql)

    def delete_student_test_item_map(self, test_id):
        """删除学生测试单词解释对照表"""
        sql = "DELETE FROM word_student_test_item_map where `test_id`={}".format(test_id)
        print(sql)
        self.execute_sql_only(sql)

    def delete_student_test(self, stu_id):
        """删除学生单词测试记录"""
        sql = "DELETE FROM word_student_test WHERE student_id = {}".format(stu_id)
        self.execute_sql_only(sql)

    def delete_student_test_overview(self, stu_id):
        """删除学生单词测试进度"""
        sql = "DELETE FROM word_student_test_overview WHERE student_id = {}".format(stu_id)
        self.execute_sql_only(sql)

    def delete_student_test_record(self, stu_id):
        """删除单词测试记录"""
        sql = "DELETE FROM word_student_test_record WHERE student_id = {}".format(stu_id)
        self.execute_sql_only(sql)

    def delete_student_word_data(self, stu_id):
        """删除学生测试单词记录"""
        sql = "DELETE FROM user_word_data WHERE account_id= {} and (`key` = 'word_test_count' or `key` = 'test_num')".format(stu_id)
        self.execute_sql_only(sql)

