from app.honor.student.games.sentence_change import SentenceChangeGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class ExamSentenceExchange(SentenceChangeGame):

    @teststeps
    def play_sentence_exchange_game(self, num, exam_json):
        """句型转换"""
        exam_json['句型转换'] = bank_json = {}
        for i in range(num):
            question = self.sentence_question()[0].text
            print(question)
            self.next_btn_judge('false', self.clear_btn)
            print('提示词序：', ' '.join([x.text for x in self.text_bottom()]))

            self.sentence_exchange_play_process()
            mine_answer = ' '.join([x.text for x in self.input_text()])
            print('我的答案：', mine_answer)
            self.next_btn_judge('true', self.clear_btn)
            bank_json[i] = mine_answer
            AnswerPage().skip_operator(i, num, "句型转换", self.wait_check_exchange_sentence_page, self.judge_tip_status, mine_answer)

    @teststeps
    def judge_tip_status(self, input_answer):
        answer_array = [x.text for x in self.input_text()]
        if input_answer != ' '.join(answer_array):
            self.base_assert.except_error('Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')

