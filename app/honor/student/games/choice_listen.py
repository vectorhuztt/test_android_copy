#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:42
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from app.honor.student.games.article_cloze import ClozeGame
from conf.decorator import teststep


class ListenChoiceGame(ClozeGame):
    @teststep
    def wait_check_listen_choice_page(self):
        """听力选择页面 以选项id作为依据"""
        locator = (By.ID, self.id_type() + "exo_progress")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_red_hint_page(self):
        """红色提示检查点"""
        locator = (By.ID, self.id_type() + "tv_hint")
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_commit_btn(self):
        locator = (By.ID, self.id_type() + "fab_commit")
        return self.get_wait_check_page_result(locator)

    @teststep
    def red_hint(self):
        """红色提示"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_hint')
        return ele.text

    @teststep
    def listen_choice_lib_hw_operate(self, fq, half_exit,  sec_answer=None):
        """听后选择 游戏处理"""
        time.sleep(3)
        print(self.red_hint())
        self.voice_button().click()
        time.sleep(5)
        if self.wait_check_red_hint_page():
            self.base_assert.except_error('听后选择点击开始音频按钮后， 红色提示未消失')
        mine_answer = {}
        timer, ques_info = [], []
        total_num = self.rest_bank_num()
        self.drag_up_down(drag_down=False)
        for x in range(total_num):
            if x != total_num - 1:
                index_num = x + 1
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

            print('选择答案：', select_answer)
            mine_answer[str(x)] = select_answer
            timer.append(self.bank_time())
            print('-'*30,'\n')
        self.judge_timer(timer)
        while not self.wait_check_commit_btn():
            time.sleep(3)
        self.next_btn_operate('true', self.fab_commit_btn)
        return mine_answer