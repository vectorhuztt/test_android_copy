
import random
from app.honor.student.games.article_cloze import ClozeGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps


class ClozeTest(ClozeGame):
    """完形填空"""

    @teststeps
    def play_cloze_test_game(self, num, exam_json):
        """完型填空  答卷过程"""
        exam_json['完形填空'] = bank_json = {}
        article = self.rich_text()
        print(article.text)
        for i in range(num):
            question = self.question()[0].text
            print('题目：', question)
            select_answer = self.cloze_game_play_process()
            print('选择答案：', select_answer)
            bank_json[i] = select_answer
            AnswerPage().skip_operator(i, num, "完形填空", self.wait_check_cloze_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        select_char = [x for x in self.opt_char() if x.get_attribute('selected') == 'true']
        if len(select_char) == 0:
            self.base_assert.except_error('Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')