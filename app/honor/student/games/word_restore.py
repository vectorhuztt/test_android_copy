#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:37
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep, teststeps


class RestoreWordGame(GameCommonEle):

    @teststep
    def wait_restore_word_explain_page(self):
        """还原单词页面检查点"""
        locator = (By.ID, self.id_type() + "tv_prompt")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_restore_answer_word_page(self):
        """还原单词页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@resource-id, "tv_word") and @index=1]')
        return self.get_wait_check_page_result(locator, timeout=5)


    @teststep
    def word_explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def word(self, index=0):
        """展示的 待还原的单词"""
        word = self.driver.find_elements_by_xpath('//android.widget.TextView[@resource-id= '
                                                  '"{}tv_word" and @index={}]'.format(self.id_type(), index))
        return word

    @teststep
    def voice(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_sound')
        return ele

    @teststep
    def button_swipe(self, from_x, from_y, to_x, to_y, steps=1000):
        """拖动单词button"""
        self.driver.swipe(from_x, from_y, to_x, to_y, steps)

    @teststep
    def get_element_location(self, ele):
        """获取元素坐标"""
        x = ele.location['x']
        y = ele.location['y']
        return x, y

    @teststeps
    def drag_operate(self, word2, word):
        """拖拽 操作"""
        loc = self.get_element_location(word2)
        y2 = self.get_element_location(word)[1] - 40
        self.button_swipe(loc[0], loc[1], loc[0], y2, 1000)
        time.sleep(1)

    @teststeps
    def restore_word_right_operate(self, right_answer):
        """还原单词做对操作"""
        print('正确答案：', right_answer)
        index, count = 0, 0
        sort_word = ''
        while True:
            alphas = self.word()
            for x in range(count, len(alphas)):
                alpha_len = len(alphas[x].text)
                if index + alpha_len >= len(right_answer) - 1:
                    right_answer += ' ' * alpha_len
                word_part = ''.join([right_answer[x] for x in range(index, index + alpha_len)])

                if alphas[x].text.lower() == word_part.strip().lower():
                    if count != x:
                        self.drag_operate(alphas[x], alphas[count])
                        sort_word = ''.join([k.text for k in self.word()])
                    index += alpha_len
                    count += 1
                    break

            if right_answer.strip().lower() == sort_word.lower():
                break
        return sort_word

    @teststep
    def restore_word_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """还原单词主要操作步骤"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.rate_judge(total_count, x)
            explain = self.word_explain().text
            print('解释：', explain)
            self.next_btn_judge('false', self.fab_commit_btn)
            word_alpha = self.word_alpha()
            before_word = ''.join([x.text for x in word_alpha])
            print('还原前单词：', before_word)

            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                self.drag_operate(word_alpha[-1], word_alpha[0])
                if len(before_word) > 2:
                    finish_word = before_word[-1] + before_word[0:-1]
                else:
                    finish_word = before_word[-1] + before_word[0]
            else:
                finish_word = self.restore_word_right_operate(sec_answer[str(x)])
            print('还原后单词：', finish_word)
            mine_answer[str(x)] = finish_word
            timer.append(self.bank_time())
            time.sleep(3)
            if self.wait_restore_word_explain_page():
                if self.word_explain().text == explain:
                    self.next_btn_operate('true', self.fab_commit_btn)
                    if self.wait_restore_answer_word_page():
                        print('正确答案：', self.word_alpha()[0].text)
                    self.fab_next_btn().click()

            print('-'*30, '\n')
        self.judge_timer(timer)
        return mine_answer