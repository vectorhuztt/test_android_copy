#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:37
# -----------------------------------------
import random
import re
import string

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class SpellWordGame(GameCommonEle):

    @teststep
    def wait_check_normal_spell_page(self):
        """单词拼写(默写模式)页面检查点"""
        locator = (By.ID, self.id_type() + "underline")
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_tv_word_or_random_page(self):
        """单词拼写（随机模式）页面检查点"""
        locator = (By.ID, self.id_type() + "tv_word")
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_right_answer_page(self):
        """正确单词页面检查点"""
        locator = (By.ID, self.id_type() + "tv_answer")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_hint_page(self):
        """默写模式页面检查点"""
        locator = (By.ID, self.id_type() + "hint")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_hint_word_page(self):
        """提示字母页面检查点"""
        locator = (By.ID, self.id_type() + "tv_word")
        return self.wait.wait_check_element(locator, timeout=3)

    @teststep
    def word_explain(self):
        """拼写翻译"""
        locator = (By.ID, self.id_type() + "tv_explain")
        return self.wait.wait_find_element(locator)

    @teststep
    def hint_btn(self):
        """提示按钮"""
        locator = (By.ID, self.id_type() + "hint")
        return self.wait.wait_find_element(locator)

    @teststep
    def spell_word(self):
        """拼写单词"""
        locator = (By.ID, self.id_type() + "tv_word")
        return self.wait.wait_find_element(locator)

    @teststep
    def right_answer_word(self):
        """正确答案"""
        locator = (By.ID, self.id_type() + "tv_answer")
        return self.wait.wait_find_element(locator).text

    # 结果页答案对比
    @teststep
    def group_word(self, index):
        """结果页一组单词"""
        locator = (By.XPATH, '//*[@content-desc="{}" and contains(@resource-id, "item_container")]/'
                             'android.widget.TextView[contains(@resource-id, "word")]'.format(index))
        return self.wait.wait_find_element(locator).text

    @teststep
    def group_explain(self, index):
        """结果页 解释"""
        locator = (By.XPATH,  '//*[@content-desc="{}" and contains(@resource-id, "item_container")]/'
                              'android.widget.TextView[contains(@resource-id, "explain")]'.format(index))
        return self.wait.wait_find_element(locator).text

    @teststep
    def group_word_voice(self, index):
        """结果页单词喇叭"""
        locator = (By.XPATH, '//*[@content-desc="{}" and contains(@resource-id, "item_container")]/'
                             'android.widget.ImageView[contains(@resource-id, "audio")]'.format(index))
        return self.wait.wait_find_element(locator)

    @teststep
    def group_right_wong_icon(self, index):
        """结果页 单词对错标识"""
        locator = (By.XPATH,  '//*[@content-desc="{}" and contains(@resource-id, "item_container")]'
                              '/android.widget.ImageView[contains(@resource-id, "result")]'.format(index))
        return self.wait.wait_find_element(locator)

    @teststep
    def word_spell_play_process(self, game_mode, do_right=False, right_answer=None):
        """单词拼写游戏做对操作"""
        if game_mode == 1:
            if do_right:
                for i in range(len(right_answer)):
                    Keyboard().keyboard_operate(right_answer[i], i)
            else:
                random_str = ''.join(random.sample(string.ascii_lowercase, random.randint(2, 5)))
                for j in range(len(random_str)):
                    Keyboard().keyboard_operate(random_str[j], j)
        else:
            page_wait_input_word = self.spell_word().text[1::2]
            print('页面字符：', page_wait_input_word)

            if do_right:
                answer_word_list = list(right_answer)
                input_word_list = [x for x, y in zip(answer_word_list, list(page_wait_input_word)) if x != y]
                for x in range(len(input_word_list)):
                    Keyboard().keyboard_operate(input_word_list[x], x)
            else:
                input_count = len(re.findall(r'_', self.spell_word().text))
                for x in range(input_count):
                    Keyboard().games_keyboard(random.choice(string.ascii_lowercase))

    @teststep
    def word_spell_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """单词拼写在图书馆、作业中的游戏过程"""
        game_mode = 1 if self.wait_check_normal_spell_page() else 0
        total_count = self.rest_bank_num()
        mine_answer = {}
        timer = []
        for x in range(total_count):
            self.rate_judge(total_count, x)
            self.next_btn_judge('false', self.fab_commit_btn)  # 判断下一题按钮状态
            explain = self.word_explain().text
            print('解释：', explain)

            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                self.word_spell_play_process(game_mode)
            else:
                self.word_spell_play_process(game_mode, do_right=True, right_answer=sec_answer[str(x)])

            self.next_btn_operate('true', self.fab_commit_btn)  # 判断下一题按钮状态
            finish_answer = self.spell_word().text[1::2] if game_mode == 0 else self.spell_word().text[::2]
            mine_answer[str(x)] = finish_answer
            print('我的答案：', finish_answer)
            if fq == 1:
                if self.wait_check_right_answer_page():
                    print('正确答案：', self.right_answer_word())
            timer.append(self.bank_time())
            self.fab_next_btn().click()
            print('-' * 30, '\n')
        self.judge_timer(timer)
        print('本次做题答案：', mine_answer)
        return mine_answer

    @teststep
    def word_game_result_check_operate(self, mine_answer):
        """单词类游戏结果页处理"""
        right_answer = {}
        right_count = 0
        value_is_explain = self.value_is_explain(mine_answer)
        for x in range(len(mine_answer)):
            if x != len(mine_answer) - 1:
                index_num = x + 1
            else:
                index_num = x
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            while not self.wait_check_word_container_by_index_and_id(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.85, 500)
            result_explain = self.group_explain(x)
            result_word = self.group_word(x)
            result_word_voice = self.group_word_voice(x)
            result_icon = self.group_right_wong_icon(x)
            check_answer = result_explain if value_is_explain else result_word
            print('解释：', result_explain)
            print('单词：', result_word)

            result_word_voice.click()

            if mine_answer[str(x)].lower() != check_answer.lower():
                if GetAttribute().get_selected(result_icon) == 'true':
                    self.base_assert.except_error('单词与我输入的不一致，但图标显示正确\n')
                else:
                    print('图标标识正确\n')
                right_answer[str(len(right_answer))] = check_answer
            else:
                right_count += 1
                if GetAttribute().get_selected(result_icon) == 'false':
                    self.base_assert.except_error('单词与我输入一致，但图标显示错误\n')
                else:
                    print('图标标识正确\n')
        print('错题再练答案：', right_answer)
        return right_answer, right_count, len(mine_answer)
