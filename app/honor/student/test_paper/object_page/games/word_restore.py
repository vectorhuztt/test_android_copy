from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.word_restore import RestoreWordGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class RestoreWord(RestoreWordGame):

    @teststeps
    def play_restore_word_game(self, num, exam_json):
        """还原单词"""
        exam_json['还原单词'] = bank_json = {}
        for i in range(num):
            explain = self.word_explain()
            print('解释：', explain.text)
            word_alpha = self.word_alpha()
            word = []
            for char in word_alpha:
                word.append(char.text)
            print('还原前单词：', ''.join(word))

            self.drag_operate(word_alpha[0], word_alpha[-1])
            finish_word = [x.text for x in self.word_alpha()]
            final_word = ''.join(finish_word)
            print('还原后单词：', ''.join(finish_word))
            bank_json[i] = ''.join(finish_word)
            AnswerPage().skip_operator(i, num, '还原单词', self.wait_restore_word_explain_page,
                                       self.judge_tip_status, final_word)

    @teststeps
    def judge_tip_status(self, final_word):
        if final_word == ''.join([x.text for x in self.word_alpha()]):
            print('跳转题目后单次顺序未发生改变')
        else:
            self.base_assert.except_error("跳转题目后单词顺序发生改变！")








