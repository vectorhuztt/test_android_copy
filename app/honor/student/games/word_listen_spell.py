#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:37
# -----------------------------------------
import random
import string

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep
from utils.games_keyboard import Keyboard


class ListenSpellGame(GameCommonEle):
    @teststep
    def wait_check_listen_spell_word_page(self):
        locator = (By.ID, self.id_type() + 'underline')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_answer_word_page(self):
        """判断 答案是否展示"""
        locator = (By.ID, self.id_type() + "tv_answer")
        return self.get_wait_check_page_result(locator)

    @teststep
    def click_voice(self):
        """声音按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + 'play_voice')\
            .click()

    @teststep
    def input_word(self):
        """完成的单词"""
        word = self.driver.find_element_by_id(self.id_type() + 'tv_word')
        return word.text[::2]

    @teststep
    def word_explain(self):
        """单词解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_explain')
        return ele

    @teststep
    def right_answer(self):
        """拼写单词答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return ele.text

    @teststep
    def input_wrap_side(self):
        """单词听写输入栏外侧"""
        ele = self.driver.find_element_by_id(self.id_type() + 'll_container')
        return ele

    @teststep
    def listen_spell_play_operate(self, do_right=False, right_answer=None):
        """单词听写对错操作"""
        if do_right:
            for j in range(len(right_answer)):  # 输入正确答案
                Keyboard().games_keyboard(right_answer[j])
        else:
            random_length = random.randint(3, 5)  # 创建随机字母
            random_string = ''.join(random.sample(string.ascii_letters, random_length))
            for j in range(len(random_string)):  # 输入随机字母
                Keyboard().games_keyboard(random_string[j])

    @teststep
    def listen_spell_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """单词听写游戏过程"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.rate_judge(total_count, x)
            self.next_btn_judge('false', self.fab_commit_btn)
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if self.input_word() != '点喇听单':
                self.base_assert.except_error('默写单词栏默认不为空！')
            if fq == 1:
                self.listen_spell_play_operate()
            else:
                self.listen_spell_play_operate(do_right=True, right_answer=sec_answer[str(x)])
            self.next_btn_operate('true', self.fab_commit_btn)
            finish_word = self.input_word()
            print('解释：', self.word_explain().text)
            print('我的答案：', finish_word)
            mine_answer[str(x)] = finish_word
            if fq == 1:
                if self.wait_check_answer_word_page():
                    print("正确答案：", self.right_answer())
            self.click_voice()
            timer.append(self.bank_time())
            self.fab_next_btn().click()
            print('-' * 20, '\n')
        self.judge_timer(timer)
        return mine_answer