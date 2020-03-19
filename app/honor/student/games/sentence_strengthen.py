#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:46
# -----------------------------------------
import random
import re
import string
import time

from selenium.webdriver.common.by import By
from app.honor.student.games.sentence_link import SentenceLinkGame
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class SentenceStrengthenGame(SentenceLinkGame):

    @teststep
    def wait_check_sentence_page(self):
        """强化炼句页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_correct_answer_page(self):
        """检查是否出现正确答案页面"""
        locator = (By.ID, '{}correct'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def sentence_explain(self):
        """文章"""
        ele = self.driver.find_element_by_id(self.id_type() + 'explain')
        return ele.text


    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'correct')
        return ele.text


    @teststep
    def sentence_strengthen_play_process(self, do_right=False, right_answer=None):
        """强化炼句对错操作"""
        if do_right:
            for word in right_answer:
                for x in list(word):
                    Keyboard().games_keyboard(x)
                time.sleep(0.5)
                Keyboard().games_keyboard('enter')
        else:
            input_item = self.get_rich_text_input_count()
            for j in range(input_item):
                random_str = random.sample(string.ascii_letters, random.randint(2, 4))  # 随机输入2个字母
                for x in random_str:
                    Keyboard().games_keyboard(x)
                time.sleep(0.5)
                Keyboard().games_keyboard('enter')

    @teststep
    def sentence_strengthen_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """强化炼句主要过程"""
        total_count = self.rest_bank_num()
        mine_answer = {}
        timer = []
        for x in range(total_count):
            self.next_btn_judge('false', self.fab_commit_btn)
            explain = self.sentence_explain().strip()
            print('解释：', explain)
            sentence = self.rich_text().text  # 获取答案
            print('句子：', sentence)
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break
            if fq == 1:
                self.sentence_strengthen_play_process()
            else:
                right_answer = sec_answer[str(x)].split()
                reform_sentence_array =[re.sub(r'[.!?]', '', x.replace(u'\xa0', u'-')) for x in sentence.split(' ')]
                reform_sentence = [x for x in reform_sentence_array if x]
                right_input_words = [x for x, y in zip(right_answer, reform_sentence) if x not in y]
                print('输入单词：', right_input_words)
                self.sentence_strengthen_play_process(do_right=True, right_answer=right_input_words)

            if not self.wait_check_correct_answer_page():
                self.base_assert.except_error('点击下一步后未出现正确答案')
            else:
                page_answer = ' '.join(self.rich_text().text.split())
                finish_answer = re.sub(r'[.!?]', '', page_answer).strip()
                print('我的答案：', finish_answer)
                mine_answer[str(x)] = finish_answer
                right_answer = self.right_answer()
                print('正确答案：', right_answer)
                timer.append(self.bank_time())

                self.fab_next_btn().click()
                time.sleep(2)
                print('-' * 30, '\n')
        self.judge_timer(timer)
        print('本题做题答案：', mine_answer)
        return mine_answer

    @teststeps
    def sentence_strengthen_result_operate(self, mine_answer):
        """强化炼句结果页处理"""
        right_answer = {}
        right_count = 0
        for x in range(len(mine_answer)):
            if x != len(mine_answer) - 1:
                index_num = x + 1
            else:
                index_num = x
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            while not self.wait_check_sentence_container_by_content_desc(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.85, 500)
            mine_done_answer = mine_answer[str(x)]
            right_wrong_icon = self.group_sentence_right_wrong_icon(x)
            sentence_hint_explain = self.group_hint_explain(x)
            page_sentence_answer = self.group_answer_sentence(x)
            print('解释：', sentence_hint_explain)
            print('句子：', page_sentence_answer)

            reform_right_ans, reform_mine_ans = self.get_right_and_mine_answer(page_sentence_answer)
            if '(' in page_sentence_answer:
                right_answer[str(len(right_answer))] = reform_right_ans
                if mine_done_answer != reform_mine_ans:
                    self.base_assert.except_error('输入的答案与页面展示的不一致 ' + mine_done_answer)

                if GetAttribute().get_selected(right_wrong_icon) == 'true':
                    self.base_assert.except_error('我的答案与正确答案不一致，但是图标显示正确！' + mine_done_answer)
                else:
                    print('图标验证正确')
            else:
                right_count += 1
                if GetAttribute().get_selected(right_wrong_icon) == 'false':
                    self.base_assert.except_error('我的答案与正确答案一致，但是图标显示不正确！' + mine_done_answer)
                else:
                    print('图标验证正确')
            print('-'*30, '\n')
        print('错题再练答案：', right_answer)
        return right_answer, right_count, len(mine_answer)

    @teststep
    def get_right_and_mine_answer(self, ans):
        """获取正确答案和我的答案"""
        mine, right = [], []
        for x in ans.split():
            if x:
                if '(' in x:
                    right.append(x.split('(')[0])
                    mine.append(x.split('(')[1].replace(')', ''))
                else:
                    mine.append(x)
                    right.append(x)
        pattern = re.compile(r'[.,!?，。！？]')
        mine_ans = pattern.sub('', ' '.join(mine))
        print('我的答案：', mine_ans)
        right_answer = pattern.sub('', ' '.join(right))
        print('正确答案：', right_answer)
        return right_answer, mine_ans

