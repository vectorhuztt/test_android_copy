import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.choice_listen import ListenChoiceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class ListenSelect(ListenChoiceGame):

    @teststeps
    def play_listening_select_game(self, num, exam_json):
        """听力选择 """
        if self.wait_check_listen_choice_page():
            print(self.red_hint())
            self.voice_button().click()
            time.sleep(2)
            if self.wait_check_red_hint_page():
                self.base_assert.except_error('Error-- 红色标识未消失')

            exam_json['听后选择'] = bank_json = {}
            for x in range(num):
                if x != num - 1:
                    index_num = x + 1
                else:
                    index_num = x
                    self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                while not self.wait_check_article_container_by_index(index_num):
                    self.screen_swipe_up(0.5, 0.9, 0.8, 500)
                question = self.get_question_by_bank_index(x).text
                print('问题：', question)
                select_answer = self.cloze_game_play_process(index=x)
                print('选择答案：', select_answer)
                bank_json[x] = select_answer
                func = self.wait_check_listen_choice_page
                AnswerPage().skip_operator(x, num, '听后选择', func, self.judge_tip_status, x, select_answer)

    @teststep
    def judge_tip_status(self, opt_index, opt_text):
        options = self.get_opt_text_by_index(opt_index)
        selected_text = [x for x in options if x.text == opt_text]
        if selected_text[0].get_attribute('selected') != 'true':
            self.base_assert.except_error('Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')

