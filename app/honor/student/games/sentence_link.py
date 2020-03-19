#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:47
# -----------------------------------------
from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.games.word_restore import RestoreWordGame
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class SentenceLinkGame(GameCommonEle):
    """连词成句"""

    @teststep
    def wait_check_link_sentence_page(self):
        """连词成句页面检查点"""
        locator = (By.ID, '{}tv_prompt'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_right_answer_page(self):
        """检查是否出现正确答案"""
        locator = (By.ID, '{}tv_sentence'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def word_alpha(self):
        """每个字母"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def sentence_explain(self):
        """解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_prompt')
        return ele.text

    @teststep
    def right_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_sentence')
        return ele.text

    @teststep
    def group_answer_sentence(self, index):
        """句子正确答案"""
        ele = self.driver.find_element_by_xpath('//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc="{}"]//'
                                                'android.widget.TextView[contains(@resource-id, "tv_answer")]'.format(index))
        return ele.text

    @teststep
    def group_hint_explain(self, index):
        """句子解释"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.TextView[contains(@resource-id, 'tv_hint')]".format(index))
        return ele.text

    @teststep
    def group_sentence_right_wrong_icon(self, index):
        """正确错误图标"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.ImageView[contains(@resource-id, 'iv_mine')]".format(index))
        return ele


    # 句型转换、听音连句的句型转换
    @teststep
    def group_mine_answer(self, index):
        """我的答案"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.TextView[contains(@resource-id, 'tv_mine')]".format(index))
        return ele.text

    @teststep
    def do_right_operate(self, right_answer):
        """连词成绩做对操作"""
        right_word_list = right_answer.split(' ')
        index = 0
        print('初始句子：', ' '.join([x.text for x in self.word_alpha()]).strip())
        for i in range(index, len(right_word_list)):
            alpha_list = self.word_alpha()
            for j in range(len(alpha_list)):
                if alpha_list[j].text == right_word_list[i]:
                    if alpha_list[j].text != alpha_list[index].text:
                        RestoreWordGame().drag_operate(alpha_list[j], alpha_list[index])
                    index += 1
                    break
            if ' '.join([x.text for x in self.word_alpha()]).strip() == right_answer:
                break

    @teststeps
    def sentence_link_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """连词成句游戏过程"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.next_btn_judge('false', self.fab_commit_btn)  # 判断下一步状态
            explain = self.sentence_explain().strip()
            print('解释：', explain)
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                RestoreWordGame().drag_operate(self.word_alpha()[-1], self.word_alpha()[0])
                if self.wait_check_commit_btn_page():
                    self.next_btn_operate('true', self.fab_commit_btn)
            else:
                right_answer = sec_answer[str(x)]
                self.do_right_operate(right_answer)

            if not self.wait_check_right_answer_page():
                self.base_assert.except_error('点击下一步后未发现正确答案')
            else:
                right_answer = self.right_answer()
                print('正确答案：', right_answer)

            mine = ' '.join([x.text for x in self.word_alpha()])
            mine_answer[str(x)] = mine
            print('我的答案：', mine)
            timer.append(self.bank_time())
            self.fab_next_btn().click()
            print('-' * 20, '\n')
        print('本次做题答案：', mine_answer)
        self.judge_timer(timer)
        return mine_answer

    @teststeps
    def sentence_link_result_operate(self, mine_answer):
        """连词成句结果页处理"""
        right_answer = {}
        right_count = 0
        for x in range(len(mine_answer)):
            if x != len(mine_answer) - 1:
                index_num = x + 1
            else:
                index_num = x
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            while not self.wait_check_sentence_container_by_content_desc(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.8, 500)

            right_wrong_icon = self.group_sentence_right_wrong_icon(x)
            sentence_hint_explain = self.group_hint_explain(x)
            page_sentence_answer = self.group_answer_sentence(x)
            print('解释：', sentence_hint_explain)
            print('句子：', page_sentence_answer)

            if mine_answer[str(x)] != page_sentence_answer:
                right_answer[str(len(right_answer))] = page_sentence_answer
                if GetAttribute().get_selected(right_wrong_icon) == 'true':  # 校验图标是否正确
                    self.base_assert.except_error('我的答案与正确答案不一致，但是图标显示正确！' + page_sentence_answer)
                else:
                    print('图标验证正确')
            else:
                right_count += 1
                if GetAttribute().get_selected(right_wrong_icon) == 'false':
                    self.base_assert.except_error('我的答案与正确答案一致，但是图标显示不正确！' + page_sentence_answer)
                else:
                    print('图标验证正确')
            print('-'*30, '\n')
        print('错题再练答案：', right_answer)
        return right_answer, right_count, len(mine_answer)
