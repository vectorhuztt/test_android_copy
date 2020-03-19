#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 16:41
# -----------------------------------------
from utils.sql import SqlDb


class WordRebuildSql(SqlDb):

    def find_sys_words_trans_id(self, stu_id):
        """获取系统的解释的id"""
        sql = "SELECT translation_id FROM word_student_fluency WHERE student_id = {} and " \
              "deleted_at is NULL and auth_type_ids like '%1%'".format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_teacher_words_trans_id(self, stu_id):
        """获取老师单词的解释的id"""
        sql = "SELECT translation_id FROM word_student_fluency WHERE student_id = {} and " \
              "deleted_at is NULL and auth_type_ids like '%2&' order by created_at".format(stu_id)
        return self.execute_sql_return_result(sql)

    def update_student_word_fluency_data(self, stu_id):
        """更新学生单词数据"""
        sql = 'UPDATE word_student_fluency SET fluency_level=0, last_finish_at = NULL, ' \
              'deleted_at = NULL WHERE student_id = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def update_student_finish_date(self, stu_id):
        """更新学生完成单词的时间， 全部设置为null"""
        sql = "UPDATE word_student_fluency SET last_finish_at = NULL where student_id ={}".format(stu_id)
        return self.execute_sql_only(sql)

    def update_student_word_data(self, stu_id):
        """更改学生单词数据value为0"""
        sql = 'UPDATE `user_word_data` SET `value` = 0 WHERE `account_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_word_wrong_data(self, stu_id):
        """删除学生单词错题表数据"""
        sql = 'DELETE FROM `word_homework_student_record` WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def delete_student_word_fluency_flag(self, stu_id):
        """删除flag表中关于学生数据"""
        sql = 'DELETE FROM `word_student_fluency_flag` WHERE `student_id` = {}'.format(stu_id)
        return self.execute_sql_only(sql)

    def find_explain_level_by_id(self, stu_id, explain_id):
        """根据解释id 获取当前解释的F值"""
        sql = 'SELECT fluency_level FROM word_student_fluency WHERE translation_id = {0} and student_id = {1}'\
              .format(explain_id, stu_id)
        return self.execute_sql_return_result(sql)

    def update_has_studied_word_date(self, stu_id, update_date, fluency_level):
        """更改F值》=1的最后完成时间"""
        sql = 'UPDATE `word_student_fluency` SET `last_finish_at` = {} WHERE ' \
              '`student_id` = {} and fluency_level = {}'.format(str(update_date), stu_id, fluency_level)
        return self.execute_sql_only(sql)

    def find_word_by_explain_id(self, stu_id, explain_id):
        """根据解释id查找单词"""
        sql = 'SELECT vocabulary from wordbank, word_student_fluency wsf WHERE wsf.wordbank_id= wordbank.id and ' \
              'wsf.student_id= {0} and wsf.translation_id = {1}'.format(stu_id, explain_id)
        return self.execute_sql_return_result(sql)

    def find_level_equal_one(self, stu_id):
        """用于判断二轮复习时，获取B轮复习单词"""
        sql = 'select translation_id from word_student_fluency where student_id = {} ' \
              'and fluency_level = 1'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_level_more_than_one(self, stu_id, level):
        """获取F值在[2,level] 的单词"""
        sql = 'select translation_id from word_student_fluency where student_id = {} and ' \
              'fluency_level between 2 and {}'.format(stu_id, level)
        return self.execute_sql_return_result(sql)

    def update_limit_fluency_word_date(self, stu_id, interval, level):
        """更改单词时间"""
        sql = 'UPDATE word_student_fluency set last_finish_at = DATE_ADD(now(),INTERVAL {0} DAY) WHERE ' \
              'student_id = {1} and fluency_level={2} limit 10'.format(interval, stu_id, level)
        return self.execute_sql_return_result(sql)

    def update_level_between_level_date(self, stu_id, interval, level):
        """更改F值在[1, level] 区间内的完成时间"""
        sql = 'UPDATE word_student_fluency set last_finish_at = DATE_ADD(now(),INTERVAL {0} DAY) WHERE ' \
              'student_id = {1} and fluency_level between 1 and {2}'.format(interval, stu_id, level)
        return self.execute_sql_return_result(sql)

    def update_word_homework_record(self, stu_id, interval):
        """根据student_id 对已学单词去重"""
        sql = "UPDATE `word_homework_student_record` SET `created_at` = DATE_ADD(now(),INTERVAL {0} DAY) " \
              "WHERE `student_id` = {1}" .format(interval, stu_id)
        self.execute_sql_only(sql)

    def find_level_word(self, stu_id, level):
        """查找指定level的单词"""
        sql = 'select translation_id from word_student_fluency where student_id = {} ' \
              'and fluency_level = {}'.format(stu_id, level)
        return self.execute_sql_return_result(sql)

    def find_explain_by_id(self, explain_id):
        """根据解释id查找解释"""
        sql = 'SELECT translation FROM wordbank_translation where id = {}'.format(explain_id)
        return self.execute_sql_return_result(sql)

    def find_student_study_words(self, stu_id):
        """查询学生已背单词"""
        sql = 'SELECT count_level_gt_0 FROM word_student_fluency_overview where student_id = {}'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_student_words_have_explains(self, stu_id):
        """查询具有多个解释的单词"""
        sql = 'SELECT vocabulary FROM wordbank WHERE id in (SELECT wordbank_id FROM word_student_fluency ' \
              'WHERE student_id = {} GROUP BY wordbank_id HAVING count(translation_id)> 1)' .format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_recite_new_explain_words(self, stu_id, level, interval):
        """查询学生一轮复习单词中具有F值大于等于level 的单词"""

        sql = 'SELECT translation_id FROM word_student_fluency WHERE student_id = {} AND wordbank_id IN ' \
              '( SELECT wordbank_id FROM word_student_fluency WHERE student_id = {} AND fluency_level >= {} GROUP BY ' \
              'wordbank_id having count(*) > 1)  ' \
              'AND word_student_fluency.fluency_level = {} AND DATEDIFF(now(),last_finish_at) >={}'\
            .format(stu_id, stu_id, level, level, interval)
        return self.execute_sql_return_result(sql)

    def find_flash_new_explain_words(self, stu_id, translation_id):
        """根据新词解释id查询对应其他解释F>=1 的单词"""
        sql = 'SELECT translation_id FROM word_student_fluency WHERE student_id = {} AND ' \
              'wordbank_id = ( SELECT wordbank_id FROM word_student_fluency WHERE student_id = {} AND ' \
              'translation_id ={}) and fluency_level >= 1'.format(stu_id, stu_id, translation_id)
        return self.execute_sql_return_result(sql)

    def update_less_level_date(self, stu_id, level):
        """更改小于指定level的完成时间"""
        sql = 'UPDATE word_student_fluency set last_finish_at = now() WHERE ' \
              'student_id = {} and fluency_level<{}'.format(stu_id, level)
        return self.execute_sql_return_result(sql)

    def find_student_today_word_data(self, stu_id):
        """查询学生今日单词数据"""
        sql = 'SELECT value FROM user_word_data WHERE account_id = {} and `key` in ("today_new_count",' \
              '"today_old_count", "word_play_times")'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_student_new_right_words(self, stu_id):
        """查询学生新词做对的单词"""
        sql = 'SELECT translation_id FROM word_student_fluency_flag where `flag`= "review_game_to_b3"' \
              ' and student_id = {}'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def update_student_study_rule_value(self, stu_id):
        """更改学生单词本学习设置"""
        sql = 'UPDATE user_word_data set value = 1, created_at= DATE_ADD(now(),INTERVAL -1 DAY), updated_at=' \
              'DATE_ADD(now(),INTERVAL -1 DAY) WHERE ' \
              'account_id = {} and `key`= "word_learn_rule"'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def update_student_all_word_fluency_f1(self, stu_id):
        """更改学生所有单词F值为1"""
        sql = 'UPDATE word_student_fluency set fluency_level = 1, last_finish_at=now() ' \
              'WHERE student_id = {} '.format(stu_id)
        return self.execute_sql_return_result(sql)

    def update_student_10_word_f3(self, stu_id):
        """将F值小于3的单词的前十个的F值更改为3， 时间改为10天前"""
        sql = 'UPDATE word_student_fluency set fluency_level = 3, last_finish_at= DATE_ADD(now(),INTERVAL -10 day) ' \
              'WHERE student_id = {} and fluency_level< 3 LIMIT 10'.format(stu_id)
        return self.execute_sql_return_result(sql)

    # ======================== 我的单词 ================================
    def find_student_total_words_count(self, stu_id):
        sql = 'SELECT DISTINCT(wordbank_id) FROM word_student_fluency ' \
              'WHERE student_id = {} and fluency_level > 0'.format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_student_familiar_explain_id(self, stu_id):
        """查询学生标熟单词"""
        sql = "SELECT translation_id FROM `word_student_fluency_flag` " \
              "WHERE `student_id` = '{}' and flag = 'familiar_word'".format(stu_id)
        return self.execute_sql_return_result(sql)

    def find_student_star_explain_id(self, stu_id):
        """查询学生标星单词"""
        sql = "SELECT translation_id FROM `word_student_fluency_flag` " \
              "WHERE `student_id` = '{}' and flag = 'star_word'".format(stu_id)
        return self.execute_sql_return_result(sql)