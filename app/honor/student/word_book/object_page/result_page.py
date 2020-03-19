#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/27 10:41
# -----------------------------------------
import re

from app.honor.student.word_book.object_page.check_sql_handle import CheckSqlHandle
from app.honor.student.word_book_rebuild.object_page.word_rebuild_result_page import ResultPage
from conf.decorator import teststep


class WordResultPage(ResultPage):
    data = CheckSqlHandle()

    @teststep
    def verify_result_page_data(self, stu_id, today_already_study_word_data, new_word_info, recite_word_count, group_count, new_explain_word=0):
        if self.wait_check_result_page():
            print('进入结果页面')
        print('新词个数：', len(new_word_info))
        today_new_count = int(today_already_study_word_data[0])
        word_play_times = int(today_already_study_word_data[1])
        today_old_count = int(today_already_study_word_data[2])
        print('数据库记载今日新词数：', today_new_count)
        print('数据库记载组数：', word_play_times)
        print('数据库记载复习数', today_old_count)

        print(' <结果页>：')
        print('今日已练单词：%s' % self.today_word())
        print('日期：%s' % self.date())
        print(self.already_remember_word())
        print(self.word_detail_info())
        today_word_count = int(self.today_word())  # 今日已练单词 （复习+ 新词）
        already_count = int(re.findall(r'\d+', self.already_remember_word())[0])  # 已背单词
        detail = re.findall(r'\d+', self.word_detail_info())  # 最后一句统计文本

        student_studied_word_count = self.data.get_student_words_count(stu_id)
        sys_new_words = self.data.get_student_new_word(stu_id, 0)
        teacher_new_words = self.data.get_student_new_word(stu_id, 1)
        student_new_words = teacher_new_words if teacher_new_words else sys_new_words

        if recite_word_count > 28:
            if group_count == 1:
                if len(new_word_info) != 0:
                    print('❌❌❌ 复习个数大于等于28个, 不应存在新词个数')
            else:
                print('❌❌❌ 复习组数非第一组, 但是复习个数大于27')
        else:
            if len(new_word_info) == 0:
                print('❌❌❌ 复习单词个数小于27, 新词个数为0')
            else:
                if group_count == 1:
                    if len(new_word_info) not in range(3, 11):
                        print('❌❌❌ 复习单词个数小于28， 第一组新词个数不在3-10之间')
                else:
                    if len(new_word_info) < 3:
                        print('❌❌❌ 复习单词个数小于28，非第一组新词个数小于3个')

        print('~-' * 20)
        # print('需要练习的新词：', student_new_words)
        for x in list(new_word_info.keys()):
            if x not in student_new_words:
                print('❌❌❌ 此单词不在已布置的新词列表中', x)
        print('~-' * 20, '\n')
        if len(detail) == 1:
            if already_count != int(detail[0]):
                print('❌❌❌ 已练单词与描述文本中数值不一致')

        if len(detail) > 1:
            study_group_count = int(detail[0])  # 已练组数
            recite_count = int(detail[1])  # 复习个数
            new_set_words = int(detail[2])  # 新词个数
            new_explain_count = int(detail[3])  # 新释义个数

            if already_count != student_studied_word_count:
                print('❌❌❌ 已学单词数不正确，应为', student_studied_word_count)

            if today_word_count != recite_count + new_set_words + new_explain_count:
                print('❌❌❌ 今日已练单词不等于复习+新词+新释义, 应为', recite_count + new_set_words + new_explain_count)

            if study_group_count != group_count + word_play_times:
                print('❌❌❌ 已练组数不正确， 应为', group_count + word_play_times)

            if new_set_words != len(new_word_info) + today_new_count:
                print('❌❌❌ 新词学单词数不正确，应为', len(new_word_info) + today_new_count)

            if new_explain_count != new_explain_word:
                print('❌❌❌ 新释义单词个数不正确， 应为', new_explain_word)

            if recite_count != recite_word_count + today_old_count:
                print('❌❌❌ 复习单词个数不正确， 应为', recite_word_count + today_old_count)


        self.more_again_button()  # 再练一次
        if self.wait_check_next_grade():  # 继续挑战页面
            self.level_up_text()
