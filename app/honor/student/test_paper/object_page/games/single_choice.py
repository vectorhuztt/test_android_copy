import random

from app.honor.student.games.choice_single import SingleChoiceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps


class SingleChoice(SingleChoiceGame):
    """单项选择"""

    @teststeps
    def play_single_choice_game(self, num, exam_json):
        """单项选择 游戏过程 """
        exam_json['单项选择'] = bank_json = {}
        for x in range(num):
            question = self.question()[0].text
            print(x+1, '.', question)
            opt_char = self.opt_char()
            opt_text = self.opt_options()
            for j in range(len(opt_char)):
                print(opt_char[j].text, '  ', opt_text[j].text)
            select_answer = self.single_choice_play_process()
            print('选择选项：', select_answer)
            bank_json[x] = select_answer + '-无解析'
            AnswerPage().skip_operator(x, num, "单项选择", self.wait_check_single_choice_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        selected_char = [x for x in self.opt_char() if x.get_attribute('selected') == 'true']
        if len(selected_char) == 0:
            self.base_assert.except_error('Error-- 跳转回来后题目完成状态发生变化')
        elif len(selected_char) == 1:
            print('题目跳转后题目状态未改变：已完成')