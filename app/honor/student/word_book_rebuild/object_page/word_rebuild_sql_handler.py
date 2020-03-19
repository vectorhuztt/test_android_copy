#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 14:38
# -----------------------------------------

from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql import WordRebuildSql
from conf.base_page import BasePage
from conf.decorator import teststep


class WordDataHandlePage(BasePage):
    def __init__(self):
        self.mysql = WordRebuildSql()
        # self.home = HomePage()

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
    def get_word_list_by_explains(self, stu_id, explain_list):
        """根据解释列表获取单词列表"""
        return list(set([self.get_word_by_explain_id(stu_id, x) for x in explain_list]))

    @teststep
    def get_sys_words_trans_id(self, stu_id):
        """获取系统翻译ID列表"""
        sys_trans_ids = self.mysql.find_sys_words_trans_id(stu_id)
        return [x[0] for x in sys_trans_ids]

    @teststep
    def get_teacher_words_trans_id(self, stu_id):
        """获取老师布置单词"""
        sys_trans_ids = self.mysql.find_teacher_words_trans_id(stu_id)
        return [x[0] for x in sys_trans_ids]

    @teststep
    def get_level_by_explain_id(self, stu_id, explain_id):
        """根据解释id获取当前F值"""
        level = self.mysql.find_explain_level_by_id(stu_id, explain_id)
        return level[0][0]

    @teststep
    def check_has_other_studied_explain(self, stu_id, explain_id):
        """根据解释的id获取对应的F值"""
        other_has_studied_explain = self.mysql.find_flash_new_explain_words(stu_id, explain_id)
        if len(other_has_studied_explain):
            return True
        else:
            return False

    @teststep
    def clear_student_word_data(self, stu_id):
        """清除学生单词记录"""
        self.mysql.update_student_word_fluency_data(stu_id)
        self.mysql.delete_student_word_wrong_data(stu_id)
        self.mysql.delete_student_word_fluency_flag(stu_id)
        self.init_student_today_word_data(stu_id)

    @teststep
    def clear_word_finish_date(self, stu_id):
        self.mysql.update_student_finish_date(stu_id)

    @teststep
    def init_student_today_word_data(self, stu_id):
        """初始化学生今日单词数据，将value更改为0"""
        self.mysql.update_student_word_data(stu_id)

    @teststep
    def update_student_less_level_date(self, stu_id, level):
        """更改小于指定level的完成时间"""
        self.mysql.update_less_level_date(stu_id, level)


    def get_word_by_explain_id(self, stu_id, explain_id):
        """根据解释id获取单词"""
        word = self.mysql.find_word_by_explain_id(stu_id, explain_id)
        return word[0][0] if word else -1

    @teststep
    def get_explain_by_id(self, explain_id):
        """根据id查找解释"""
        explain = self.mysql.find_explain_by_id(explain_id)
        return explain[0][0] if explain else ''

    @teststep
    def change_level_limit_word_date(self, stu_id, level):
        """根据level更改单词完成时间"""
        interval = -(self.get_interval(level))
        self.mysql.update_limit_fluency_word_date(stu_id, interval, level)
        self.mysql.update_word_homework_record(stu_id, interval)

    @teststep
    def change_level_in_interval_date(self, stu_id, level):
        """更改F值在[1,level]区间内的时间"""
        interval = -(self.get_interval(level))
        self.mysql.update_level_between_level_date(stu_id, interval, level)
        self.mysql.update_word_homework_record(stu_id, interval)

    @teststep
    def get_recite_level_one_explains(self, stu_id):
        """获取需要复习的F=1单词"""
        explain_ids = self.mysql.find_level_equal_one(stu_id)
        return [x[0] for x in explain_ids]

    @teststep
    def get_recite_level_more_than_one_explains(self, stu_id, level):
        """获取F 值在【2，level】区间内的单词"""
        explain_ids = self.mysql.find_level_more_than_one(stu_id, level)
        return [x[0] for x in explain_ids]

    @teststep
    def get_student_studied_words_count(self, stu_id):
        """查询学生已背单词个数（单词去重）"""
        wordbank_ids = self.mysql.find_student_study_words(stu_id)
        return wordbank_ids[0][0] if wordbank_ids else 0

    @teststep
    def get_word_has_different_explains(self, stu_id):
        """获取具有不同解释的单词"""
        words = self.mysql.find_student_words_have_explains(stu_id)
        return [x[0] for x in words]

    @teststep
    def get_recite_new_explains(self, stu_id, level):
        """获取当前轮次复习单词中具有新释义的单词"""
        time_interval = self.get_interval(level)
        recite_new_explain_id = self.mysql.find_recite_new_explain_words(stu_id, level, time_interval)
        return [x[0] for x in recite_new_explain_id]

    @teststep
    def get_student_today_word_data(self, stu_id):
        """获取学生今日单词数据"""
        data = self.mysql.find_student_today_word_data(stu_id)
        return [x[0] for x in data]

    @teststep
    def get_student_new_all_right_explains(self, stu_id):
        """获取学生新词都正确的单词"""
        explains = self.mysql.find_student_new_right_words(stu_id)
        return [x[0] for x in explains]

    @teststep
    def reset_student_wordbook_rule(self, stu_id):
        """重置学生单词本设置规则"""
        self.mysql.update_student_study_rule_value(stu_id)

    @teststep
    def change_all_word_fl_equal_one(self, stu_id):
        """更改所有单词的F值为1"""
        self.mysql.update_student_all_word_fluency_f1(stu_id)

    @teststep
    def change_10_word_fl_equal_three(self, stu_id):
        """将F值小于3 的前10 个单词的F值更改为3"""
        self.mysql.update_student_10_word_f3(stu_id)


    @teststep
    def get_total_words(self, stu_id):
        """获取学生已被单词总数"""
        words_id = self.mysql.find_student_total_words_count(stu_id)
        if words_id:
            return [self.mysql.find_word_by_id(x[0])[0][0] for x in words_id]
        else:
            return []

    @teststep
    def get_student_familiar_explain_ids(self, stu_id):
        """获取学生标熟解释id"""
        familiar_explains = self.mysql.find_student_familiar_explain_id(stu_id)
        return [x[0] for x in familiar_explains] if familiar_explains else []

    @teststep
    def get_student_star_explain_ids(self, stu_id):
        """获取学生表象单词解释id"""
        star_explains = self.mysql.find_student_star_explain_id(stu_id)
        return [x[0] for x in star_explains] if star_explains else []