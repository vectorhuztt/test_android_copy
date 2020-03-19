#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/29 16:19
# -----------------------------------------
import time
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.word_test_sql import WordTestSql
from conf.base_page import BasePage
from conf.decorator import teststep


class WordTestSqlHandler(BasePage):

    def __init__(self):
        self.mysql = WordTestSql()
        self.rebuild_handler = WordDataHandlePage()

    @teststep
    def get_f_glt_3_count(self, stu_id):
        """获取单词F值>=3的个数"""
        word_count = self.mysql.find_f_glt_3_count(stu_id)
        return word_count[0][0] if word_count else 0

    @teststep
    def get_student_test_star_score(self, stu_id):
        """获取测试的星星积分"""
        result = {}
        star_score_data = self.mysql.find_student_start_score_data(stu_id)
        for x in star_score_data:
            if x[0] in list(result.keys()):
                result['score'] = 0
            else:
                result[x[0]] = x[1]
        return result

    @teststep
    def get_result_data(self, test_id):
        """获取结果页结果"""
        result = self.mysql.find_test_result_data(test_id)
        return result[0]

    @teststep
    def get_test_words(self, stu_id, get_type, word_count=0):
        """获取学生单词F值>=3的单词个数
           :param word_count: 需要测试的单词数, 0 为该类型的全部单词
           :param get_type: 测试类型 1：F>=3 单词 2：测试未通过单词  3：测试通过单词
           :param stu_id 学生id
        """
        if get_type == 1:
            word_result = self.mysql.find_f_glt_3_words(stu_id)
        elif get_type == 2:
            word_result = self.mysql.find_test_fail_pass_words(stu_id)
        else:
            word_result = self.mysql.find_test_success_pass_words(stu_id)

        test_list = word_result[:word_count] if word_count else word_result
        word_info = {}
        for x in test_list:
            if str(x[0]) not in list(word_info.keys()):
                word_info[str(x[0])] = list(self.mysql.find_student_translation_by_word_id(stu_id, x[0]))
            else:
                continue
        return word_info

    @teststep
    def get_word_explain_list(self, explain_info):
        """获取测试单词对应解释列表"""
        explain_list = [self.rebuild_handler.get_explain_by_id(x[0]) for x in explain_info]
        reform_list = '；'.join(explain_list).split('；')
        return reform_list

    @teststep
    def get_translation_count_by_word_id(self, test_id,  word_ids):
        """获取解释个数根据单词id"""
        result = self.mysql.find_test_translation_by_word_ids(test_id, word_ids)
        return len(result)

    @teststep
    def get_fvalue_by_word_explain_id(self, stu_id, word_id, explain_id):
        """根据单词、解释id定位学生已被单词的F值"""
        result = self.mysql.find_student_word_fvalue_by_word_explain_id(stu_id, word_id, explain_id)
        return result[0][0] if result else -1

    @teststep
    def delete_student_test_data(self, stu_id):
        """删除学生单词测试相关数据"""
        student_test_ids = self.mysql.find_student_test_id(stu_id)
        if len(student_test_ids):
            for x in student_test_ids:
                self.mysql.delete_student_test_item_map(x[0])
        self.mysql.delete_student_test(stu_id)
        self.mysql.delete_student_test_record(stu_id)
        self.mysql.delete_student_test_overview(stu_id)
        self.mysql.delete_student_word_data(stu_id)












