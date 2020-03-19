import random
from app.honor.student.games.word_guess import GuessWordGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps


class GuessingWord(GuessWordGame):

    @teststeps
    def play_guessing_word_game(self, num, exam_json):
        """猜词游戏 """
        exam_json['猜词游戏'] = bank_json = {}
        for x in range(num):
            explain = self.word_explain()
            print('解释：', explain)
            word = self.guess_word()
            print('填充前单词：', word)
            index = 0
            mine_answer = []
            while '_' in self.guess_word():
                select_alpha = self.keyboard_key()[index]
                mine_answer.append(select_alpha.text)
                select_alpha.click()
                index += 1

            print('我输入的单词：', ''.join(mine_answer))
            bank_json[x] = ''.join(mine_answer)
            finish_word = self.guess_word()
            print('最终提示单词：', finish_word)
            AnswerPage().skip_operator(x, num, '猜词游戏', self.wait_check_guess_word_page, self.judge_tip_status)

    @teststeps
    def judge_tip_status(self):
        if '_' in self.guess_word():
            self.base_assert.except_error('Error-- 跳转回来题目处于未完成状态')
        else:
            print('滑屏后题目处于完成状态')