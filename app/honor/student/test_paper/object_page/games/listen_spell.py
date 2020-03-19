from app.honor.student.games.word_listen_spell import ListenSpellGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class ListenSpell(ListenSpellGame):

    @teststeps
    def play_listen_spell_game(self, num, exam_json):
        """单词听写 """
        exam_json['单词听写'] = bank_json = {}
        for i in range(num):
            self.click_voice()
            self.listen_spell_play_operate()
            finish_word = self.input_word()
            print('我的答案：', finish_word)
            bank_json[i] = finish_word
            AnswerPage().skip_operator(i, num, '单词听写', self.wait_check_listen_spell_word_page,
                                       self.judge_tip_status, finish_word)

    @teststep
    def judge_tip_status(self, word):
        if self.input_word() != word:
            self.base_assert.except_error('Error-- 题目跳转回来后拼写单词发生改变')
        else:
            print('题目跳转回来后拼写单词未发生改变')


