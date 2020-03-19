#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:46
# -----------------------------------------
import random
import re
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.sentence_link import SentenceLinkGame
from conf.decorator import teststep
from utils.get_attribute import GetAttribute


class SentenceChangeGame(SentenceLinkGame):

    @teststep
    def wait_check_exchange_sentence_page(self):
        """句型转换页面检查点，以输入答案的id作为依据"""
        locator = (By.ID, self.id_type() + "rv_answer")
        return self.get_wait_check_page_result(locator)

    @teststep
    def text_bottom(self):
        """下方后补选择文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv_hint')
        return ele.find_elements_by_xpath('.//android.widget.TextView')

    @teststep
    def input_text(self):
        """需要填空的文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv_answer')
        return ele.find_elements_by_xpath('.//android.widget.TextView')

    @teststep
    def sentence_question(self):
        """问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_question')
        return ele

    @teststep
    def sentence_answer(self):
        """提交后的答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_answer')
        return ele.text

    @teststep
    def finish_answer_list(self):
        """已完成的句子"""
        ele = self.driver.find_elements_by_xpath('//android.support.v7.widget.RecyclerView[contains(@resource-id, "rv_answer")]/'
                                                 'android.widget.LinearLayout/android.widget.TextView')
        answer_array = [x.text for x in ele]
        return answer_array

    # 句型转换
    @teststep
    def group_question(self, index):
        """句型转换的问题"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.TextView[contains(@resource-id, 'tv_question')]".format(index))
        return ele.text

    @teststep
    def sentence_exchange_play_process(self, do_right=False, right_answer=None):
        """句型转换对错过程"""
        if do_right:
            index = 0
            while len([x for x in self.finish_answer_list() if not x]):
                wait_click_text = self.text_bottom()
                for x in wait_click_text:
                    if x.text == right_answer[index]:
                        x.click()
                        index += 1
                        break
        else:
            while len([x for x in self.finish_answer_list() if not x]):
                random.choice(self.text_bottom()).click()

    @teststep
    def sentence_change_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """句型转换游戏过程"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            question = self.sentence_question()[0].text
            print('问题:', question)
            self.next_btn_judge('false', self.fab_commit_btn)
            self.next_btn_judge('false', self.clear_btn)
            if fq == 1:
                self.sentence_exchange_play_process()
            else:
                right_answer = sec_answer[str(x)].split()
                self.sentence_exchange_play_process(do_right=True, right_answer=right_answer)

            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break
            finish_answer = ' '.join([x.text for x in self.input_text()])
            print('我的答案：', finish_answer)
            mine_answer[str(x)] = finish_answer
            self.next_btn_judge('true', self.clear_btn)
            self.next_btn_operate('true', self.fab_commit_btn)
            print(self.sentence_answer())
            timer.append(self.bank_time())
            self.next_btn_operate('true', self.fab_next_btn)
            time.sleep(1)
            print('-' * 20, '\n')
        self.judge_timer(timer)
        print('本次做题答案：', mine_answer)
        return mine_answer

    @teststep
    def sentence_change_result_operate(self, mine_answer):
        """句型转换结果页处理"""
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
            sentence_question = self.group_question(x)
            page_answer = self.group_answer_sentence(x)
            page_mine_answer = self.group_mine_answer(x)
            print(sentence_question, '\n',
                  "答案：", page_answer, '\n',
                  '我的：', page_mine_answer)
            if mine_done_answer != page_mine_answer:
                self.base_assert.except_error('做题答案与页面展示的不一致 ' + page_mine_answer)

            if page_answer != page_mine_answer:
                if GetAttribute().get_selected(right_wrong_icon) == 'true':
                    self.base_assert.except_error('我的答案与正确答案不一致，但是图标显示正确！' + page_answer)
                else:
                    print('图标验证正确')
                right_answer[str(len(right_answer))] = page_answer
            else:
                right_count += 1
                if GetAttribute().get_selected(right_wrong_icon) == 'false':
                    self.base_assert.except_error('我的答案与正确答案一致，但是图标显示不正确！' + page_answer)
                else:
                    print('图标验证正确')
            print('-'*30, '\n')
        print('错题再练答案:', right_answer)
        return right_answer, right_count, len(mine_answer)









