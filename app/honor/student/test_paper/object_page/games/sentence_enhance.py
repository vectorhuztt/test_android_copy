import random
import re
import string
import time

from app.honor.student.games.sentence_strengthen import SentenceStrengthenGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.test_paper.object_page.exam_sql_handle import DataPage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard


class SentenceEnhance(SentenceStrengthenGame):

    @teststeps
    def play_sentence_enhance_game(self, num, exam_json):
        """强化炼句 """
        exam_json['强化炼句'] = bank_json = {}
        for i in range(num):
            explain = self.sentence_explain()
            print(explain)
            sentence = self.rich_text().text
            print('提示句：', sentence)
            self.sentence_strengthen_play_process()
            finish_answer = ' '.join(self.rich_text().text.split())[:-2]
            print('我输入的：', finish_answer)
            bank_json[i] = finish_answer
            time.sleep(2)
            AnswerPage().skip_operator(i, num, '强化炼句', self.wait_check_sentence_page, self.judge_tip_status, finish_answer)

    @teststeps
    def judge_tip_status(self, input_word):
        page_input_text = ' '.join(self.rich_text().text.split())
        if input_word == page_input_text[:-2]:
            print('跳转后填空文本未发生变化')
        else:
            self.base_assert.except_error('Error-- 跳转回来填空内容发生改变')

