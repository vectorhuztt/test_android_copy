import random
import time
from app.honor.student.games.choice_vocab import VocabChoiceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.test_paper.object_page.exam_sql_handle import DataPage
from conf.decorator import teststep, teststeps


class VocabSelect(VocabChoiceGame):
    @teststeps
    def play_vocab_select_game(self, num, exam_json):
        """词汇选择 """
        exam_json['词汇选择'] = bank_json = {}
        for i in range(num):
            if self.wait_check_head_page():
                word = self.vocab_question()
                print('题目：', word.text)
                select_opt = self.vocab_choice_play_process()
                print('选择选项：', select_opt)
                bank_json[i] = select_opt
                AnswerPage().skip_operator(i, num, '词汇选择', self.wait_check_head_page, self.judge_tip_status, select_opt)

    @teststeps
    def judge_tip_status(self, select_opt):
        page_opt = [x.text for x in self.vocab_options() if x.get_attribute('selected') == 'true']
        if len(page_opt) == 0:
            self.base_assert.except_error('Error-- 跳转回来后题目选中状态被取消')
        else:
            if select_opt != page_opt[0]:
                self.base_assert.except_error('题目跳转选择内容发生改变')
            else:
                print('题目跳转后题目状态未改变：已完成')










