#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:49
# -----------------------------------------
import random

from selenium.webdriver.common.by import By
from app.honor.student.games.article_cloze import ClozeGame
from conf.decorator import teststep


class ReadUnderstandGame(ClozeGame):

    @teststep
    def wait_check_read_understand_page(self):
        locator = (By.ID, self.id_type() + "rich_text")
        return self.get_wait_check_page_result(locator)

    @teststep
    def article_understand_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """阅读理解游戏过程 """
        mine_answer = {}
        timer, ques_info = [], []
        total_num = self.rest_bank_num()
        if fq == 1:
            article = self.rich_text()
            print(article.text)
        self.next_btn_judge('false', self.fab_commit_btn)
        self.drag_up_down(drag_down=False)
        for x in range(total_num):
            if x != total_num - 1:
                index_num = x+1
            else:
                index_num = x
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            while not self.wait_check_article_container_by_index(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.8, 500)
            question = self.get_question_by_bank_index(x).text
            print('问题：', question)
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                select_answer = self.cloze_game_play_process(index=x)
            else:
                right_answer = sec_answer[str(x)]
                select_answer = self.cloze_game_play_process(index=x, do_right=True, right_answer=right_answer)
            mine_answer[str(x)] = select_answer
            timer.append(self.bank_time())
            print('-'*30, '\n')

        if not half_exit:
            self.judge_timer(timer)
            self.drag_up_down(drag_down=True)
            self.check_position_change()
            self.next_btn_operate("true", self.fab_commit_btn)
            print('本次做题答案：', mine_answer)
        return mine_answer




