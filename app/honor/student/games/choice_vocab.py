#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:45
# -----------------------------------------
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep


class VocabChoiceGame(GameCommonEle):
    @teststep
    def wait_check_head_page(self):
        """判断是否有题目"""
        locator = (By.ID, "{}tv_head".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_voice_page(self):
        """以“词汇选择 -句子选单词模式”的 提示按钮 为依据"""
        locator = (By.ID, self.id_type() + "sound")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_explain_page(self):
        """单词解释"""
        locator = (By.ID, self.id_type() + "explain")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_vocab_apply_explain_page(self):
        """词汇运用解释页面检查点"""
        locator = (By.ID, self.id_type() + "tv_explain")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_listen_explain_page(self):
        """词汇运用解释页面检查点"""
        locator = (By.ID, self.id_type() + "explain")
        return self.get_wait_check_page_result(locator)

    @teststep
    def vocab_question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_head')
        return ele

    @teststep
    def vocab_options(self):
        """选项"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'option')
        return ele

    @teststep
    def vocab_right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_accessibility_id('true')
        return ele.text

    @teststep
    def vocab_word_explain(self):
        """听音选词的单词解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'explain')
        return ele

    @teststep
    def listen_choice_speak_icon(self):
        """听音选词的上方喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "iv_speak")
        return ele

    @teststep
    def apply_hint_button(self):
        """提示按钮"""
        ele = self.driver \
                  .find_element_by_id(self.id_type() + "hint")
        return ele

    @teststep
    def apply_sentence_explain(self):
        """点击 提示按钮后，出现中文解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "tv_explain").text
        return explain

    @teststep
    def vocab_choice_play_process(self, do_right=False, right_answer=None):
        """词汇选择对错过程"""
        select_answer = ''
        if do_right:
            for x in self.vocab_options():
                if do_right:
                    if x.text == right_answer:
                        select_answer = x.text
                        x.click()
                        break
        else:
            random_index = random.randint(0, len(self.vocab_options()) - 1)
            random_choice = self.vocab_options()[random_index]
            select_answer = random_choice.text
            random_choice.click()
        return select_answer

    @teststep
    def vocab_choice_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """词汇选择游戏处理"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        bank_type = 1 if self.wait_check_head_page() else 2  # 区分听音选词和 选单词、选解释
        for x in range(total_count):
            self.next_btn_judge('false', self.fab_next_btn)  # 判断下一步按钮
            if bank_type == 2:
                self.listen_choice_speak_icon().click()
                question = x
            else:
                question = self.vocab_question().text

            print('问题：', question)
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                select_answer = self.vocab_choice_play_process()
            else:
                right_answer = sec_answer[str(x)]
                select_answer = self.vocab_choice_play_process(do_right=True, right_answer=right_answer)

            print('我的答案：', select_answer)
            mine_answer[str(x)] = select_answer
            print('正确答案：', self.vocab_right_answer())
            timer.append(self.bank_time())
            self.fab_next_btn().click()
            print('-'*30, '\n')
        print('本次做题答案：', mine_answer)
        return mine_answer







