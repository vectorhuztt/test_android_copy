import random
import re
import time

from app.honor.student.games.sentence_listen_link import ListenLinkSentenceGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class ListenSentence(ListenLinkSentenceGame):
    """听音连句"""

    @teststeps
    def play_listen_sentence_game(self, num, exam_json):
        """听音连句"""
        exam_json['听音连句'] = bank_json = {}
        for i in range(num):
            if self.wait_check_listen_sentence_page():
                self.next_btn_judge("false", self.listen_link_clear_btn)          # 清除按钮状态判断
                self.listen_link_sentence_play_process()
                self.next_btn_judge("true", self.listen_link_clear_btn)    # 清除按钮
                finish_answer = ' '.join(self.rich_text().text.split())
                print("我的答案：", finish_answer)
                bank_json[i] = finish_answer
                AnswerPage().skip_operator(i, num, '听音连句', self.wait_check_listen_sentence_page,
                                           self.judge_tip_status, finish_answer)

    @teststeps
    def judge_tip_status(self, finish_sentence):
        page_finish_answer = ' '.join(self.rich_text().text.split())
        if finish_sentence == page_finish_answer:
            print('跳转后填空文本未发生变化')
        else:
            self.base_assert.except_error('Error-- 跳转回来填空内容发生改变')
