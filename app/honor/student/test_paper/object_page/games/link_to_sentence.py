from app.honor.student.games.sentence_link import SentenceLinkGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.word_book_rebuild.object_page.games.restore_word_page import WordRestore
from conf.decorator import teststep, teststeps


class Conjunctions(SentenceLinkGame):
    """连词成句"""

    @teststeps
    def play_conjunctions_game(self, num, exam_json):
        """连词成句 游戏过程"""
        exam_json['连词成句'] = bank_json = {}
        for x in range(num):
            explain = self.sentence_explain()
            print("句子解释：", explain)
            word_alpha = self.word_alpha()
            word = [alpha.text for alpha in word_alpha]
            print('连句前句子：', ' '.join(word))
            WordRestore().drag_operate(self.word_alpha()[0], self.word_alpha()[-1])

            finish_word = ' '.join([x.text for x in self.word_alpha()])
            print('连句后句子：', finish_word)
            bank_json[x] = finish_word
            AnswerPage().skip_operator(x, num, "连词成句", self.wait_check_link_sentence_page,
                                       self.judge_tip_status, finish_word)

    @teststep
    def judge_tip_status(self, finish_word):
        sentence = ' '.join([x.text for x in self.word_alpha()])
        if finish_word == sentence:
            print('题目跳转后句子顺序未发生变化')
        else:
            self.base_assert.except_error("题目跳转后句子顺序发生变化!")
