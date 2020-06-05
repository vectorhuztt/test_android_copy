#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:38
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep


class GuessWordGame(GameCommonEle):
    """猜词游戏"""
    @teststep
    def wait_check_guess_word_page(self):
        """猜词游戏页面检查点"""
        locator = (By.ID, self.id_type() + 'level')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def keyboard(self):
        """键盘"""
        locator = (By.ID, self.id_type() + 'hm_keyboard')
        return self.wait.wait_find_element(locator)

    @teststep
    def keyboard_key(self):
        locator = (By.XPATH, '//*[@resource-id="{}hm_keyboard"]/android.widget.TextView'.format(self.id_type()))
        return self.wait.wait_find_elements(locator)

    @teststep
    def word_explain(self):
        """翻译"""
        locator = (By.ID, self.id_type() + 'chinese')
        return self.wait.wait_find_element(locator).text

    @teststep
    def guess_word(self):
        """单词"""
        locator = (By.ID, self.id_type() + 'english')
        return self.wait.wait_find_element(locator).text

    @teststep
    def word_guess_play_process(self, do_right=False, right_answer=None):
        """猜词游戏对错过程"""
        begin_num = self.rest_bank_num()
        if do_right:
            print('正确答案：', right_answer, '\n')
            for x in right_answer:
                for k in self.keyboard_key():
                    if x == k.text:
                        k.click()
                        break
            input_answer = right_answer
        else:
            mine_input = []
            index = 0
            while True:
                select_alpha = self.keyboard_key()[index]
                mine_input.append(select_alpha.text)
                select_alpha.click()
                time.sleep(0.5)
                index += 1
                if self.wait_check_guess_word_page():
                    if self.rest_bank_num() != begin_num:
                        break
                else:
                    break
            input_answer = ''.join(mine_input)
        return input_answer

    @teststep
    def guess_word_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """猜词游戏过程"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.rate_judge(total_count, x)
            explain = self.word_explain()
            print('解释：', explain)
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                answer = self.word_guess_play_process()
            else:
                right_answer = sec_answer[str(x)].lower()
                answer = self.word_guess_play_process(do_right=True, right_answer=right_answer)
            print('我的答案：', answer)
            mine_answer[str(x)] = answer
            if x != total_count - 1:
                timer.append(self.bank_time())
            time.sleep(3)
            print('-' * 30, '\n')
        self.judge_timer(timer)
        print('本次做题答案：', mine_answer)
        return mine_answer

