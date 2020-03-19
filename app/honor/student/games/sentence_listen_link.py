#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/2 9:03
# -----------------------------------------
import random

from selenium.webdriver.common.by import By
from app.honor.student.games.sentence_link import SentenceLinkGame
from conf.decorator import teststep
from utils.get_attribute import GetAttribute


class ListenLinkSentenceGame(SentenceLinkGame):
    """听音连句"""

    @teststep
    def wait_check_listen_sentence_page(self):
        """听音连句页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_clear_btn_page(self):
        """检查是否存在清除按钮"""
        locator = (By.ID, '{}clear'.format(self.id_type()))
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def listen_link_clear_btn(self):
        """听音连句"""
        ele = self.driver.find_element_by_id(self.id_type() + 'clear')
        return ele

    @teststep
    def text_for_select(self):
        """下方可点击的文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + "text")
        return [x for x in ele if x.text]

    @teststep
    def right_sentence_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_right')
        return ele.text

    @teststep
    def sentence_explain(self):
        """解释"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_explain')
        return ele


    @teststep
    def group_right_answer(self, index):
        """句型转换正确句子"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.TextView[contains(@resource-id, 'tv_right')]".format(index))
        return ele.text

    @teststep
    def group_sentence_explain(self, index):
        """听音连句 句子解释"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.TextView[contains(@resource-id, 'tv_explain')]".format(index))
        return ele.text

    @teststep
    def group_sentence_speck_icon(self, index):
        """听音连句 句子喇叭"""
        ele = self.driver.find_element_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[@content-desc='{}']//"
                                                "android.widget.ImageView[contains(@resource-id, 'iv_speak')]".format(index))
        return ele

    @teststep
    def listen_link_sentence_play_process(self, do_right=False, right_answer=None):
        """听音连句对错操作"""
        if do_right:
            print('正确答案：', right_answer)
            index = 0
            while ' '.join(self.rich_text().text.split()) != ' '.join(right_answer):
                text_for_select = self.text_for_select()
                for x in text_for_select:  # 每次只点击一个（与答案相同的词组）
                    if x.text == right_answer[index]:
                        index += 1
                        x.click()
        else:
            input_item = self.get_rich_text_input_count()
            for j in range(input_item):
                random.choice(self.text_for_select()).click()

    @teststep
    def sentence_listen_link_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """听音连句游戏过程"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.next_btn_judge('false', self.fab_commit_btn)  # 下一步按钮状态校验
            self.next_btn_judge('false', self.listen_link_clear_btn)  # 清除按钮状态校验

            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                self.listen_link_sentence_play_process()
            else:
                right_answer = sec_answer[str(x)].split()
                self.listen_link_sentence_play_process(do_right=True, right_answer=right_answer)

            self.next_btn_judge('true', self.listen_link_clear_btn)
            self.next_btn_operate('true', self.fab_commit_btn)

            if self.wait_check_clear_btn_page():
                self.base_assert.except_error('点击下一步后，清除按钮依然存在')

            finish_answer = ' '.join(self.rich_text().text.split())
            mine_answer[str(x)] = finish_answer
            print('我的答案: ', finish_answer)
            print(self.right_sentence_answer())
            print(self.sentence_explain()[0].text)
            timer.append(self.bank_time())
            self.fab_next_btn().click()
            print('-' * 20, '\n')
        self.judge_timer(timer)
        print('本次做题答案：', mine_answer)
        return mine_answer

    @teststep
    def sentence_listen_link_result_operate(self, mine_answer):
        """听音连句结果页处理"""
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
            mine_done_answer = mine_answer[str(x)]
            self.group_sentence_speck_icon(x).click()
            right_wrong_icon = self.group_sentence_right_wrong_icon(x)
            page_answer = self.group_right_answer(x).split('答案: ')[1].strip()
            page_mine_answer = self.group_mine_answer(x).split('我的: ')[1].strip()
            sentence_explain = self.group_sentence_explain(x)

            print(sentence_explain,
                  "答案：" + page_answer,
                  '我的：' + page_mine_answer,
                  sep='\n')

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
        print('错题再练答案：', right_answer)
        return right_answer, right_count, len(mine_answer)




