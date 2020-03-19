import random
import re
import string
from app.honor.student.games.word_spell import SpellWordGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep
from utils.games_keyboard import Keyboard


class WordSpell(SpellWordGame):

    def play_word_spell_game(self, num, exam_json):
        """单词拼写 """
        exam_json['单词拼写'] = bank_json = {}
        game_mode = 1 if self.wait_check_normal_spell_page() else 0
        for i in range(num):
            explain = self.word_explain().text
            print('解释：', explain)
            self.word_spell_play_process(game_mode)
            finish_answer = self.spell_word().text[1::2] if game_mode == 0 else self.spell_word().text[::2]
            bank_json[i] = finish_answer
            print('我的答案：', finish_answer)
            func = self.wait_check_normal_spell_page if game_mode == 1 else self.wait_check_tv_word_or_random_page
            AnswerPage().skip_operator(i, num, '单词拼写', func, self.judge_tip_status, finish_answer)

    @teststep
    def judge_tip_status(self, word):
        if self.wait_check_normal_spell_page:
            game_mode = 1
        else:
            game_mode = 0

        page_answer = self.spell_word().text[1::2] if game_mode == 0 else self.spell_word().text[::2]
        if word != page_answer:
            self.base_assert.except_error('Error-- 题目跳转回来后拼写单词发生改变')
        else:
            print('题目跳转回来后拼写单词未发生改变')


