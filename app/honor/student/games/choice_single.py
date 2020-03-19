#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:47
# -----------------------------------------
import random
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep, teststeps


class SingleChoiceGame(GameCommonEle):
    @teststep
    def wait_check_single_choice_page(self):
        """单项选择页面检查点"""
        locator = (By.ID, "{}question".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_analysis_tab_page(self):
        """解析字样页面检查点 代表单选有解析文本"""
        locator = (By.ID, "{}hint_text".format(self.id_type()))
        return self.get_wait_check_page_result(locator, timeout=4)

    @teststep
    def wait_check_analysis_text_page(self):
        """解析文本 页面检查点"""
        locator = (By.ID, "{}analysis_text".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_analysis_audio_page(self):
        """解析音频 页面检查点"""
        locator = (By.ID, "{}analysis_audio".format(self.id_type()))
        return self.get_wait_check_page_result(locator)


    @teststep
    def wait_check_result_analysis_page(self, index):
        """结果页单选解析字样检查点"""
        locator = (By.XPATH, "//android.widget.LinearLayout[@index='{}']//android.widget.TextView"
                             "[contains(@resource-id, 'hint_text')]".format(index))
        return self.get_wait_check_page_result(locator, timeout=4)

    @teststep
    def wait_check_result_analysis_audio_page(self, index):
        """结果页单选解析音频检查点"""
        locator = (By.XPATH, "//android.widget.LinearLayout[@index='{}']//android.widget.TextView"
                             "[contains(@resource-id, 'audio_parse_container')]".format(index))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_result_analysis_text_page(self, index):
        """结果页单选解析内容检查点"""
        locator = (By.XPATH, "//android.widget.LinearLayout[@index='{}']//android.widget.TextView"
                             "[contains(@resource-id, 'analysis_text')]".format(index))
        return self.get_wait_check_page_result(locator)

    @teststep
    def analysis_text(self):
        """解析内容"""
        ele = self.driver.find_element_by_id(self.id_type() + 'analysis_text')
        return ele.text

    @teststep
    def analysis_audio_btn(self):
        """解析内容"""
        ele = self.driver.find_element_by_id(self.id_type() + 'analysis_audio')
        return ele

    @teststep
    def right_choice(self):
        """正确选项内容"""
        ele = self.driver.find_element_by_xpath('//*[@content-desc="right"]/following-sibling::android.widget.TextView')
        return ele.text

    # 听后选择  音频播放按钮
    @teststep
    def voice_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'exo_play')
        return ele

    @teststep
    def get_question_by_bank_index(self, index):
        question = self.driver.find_element_by_xpath("//android.widget.LinearLayout[@index='{}']/android.widget.TextView"
                                                     "[contains(@resource-id, 'question')]".format(index))
        return question

    @teststep
    def get_opt_text_by_index(self, index):
        """根据索引查询选项内容"""
        options = self.driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='{}']/android.view.ViewGroup//android.widget.TextView"
                                                     "[contains(@resource-id, 'tv_item')]".format(index))
        return options

    @teststep
    def get_opt_char_by_index(self, index):
        """根据索引查询选项索引"""
        chars = self.driver.find_elements_by_xpath("//android.widget.LinearLayout[@index='{}']/android.view.ViewGroup//android.widget.TextView"
                                                   "[contains(@resource-id, 'tv_char')]".format(index))
        return chars

    @teststep
    def get_analysis_text_by_index(self, index):
        analysis = self.driver.find_element_by_xpath("//android.widget.LinearLayout[@index='{}']/android.widget.LinearLayout/"
                                                     "android.view.ViewGroup//android.widget.TextView"
                                                     "[contains(@resource-id, 'analysis_text')]".format(index))
        return analysis.text

    @teststep
    def get_analysis_audio_by_index(self, index):
        analysis = self.driver.find_element_by_xpath("//android.widget.LinearLayout[@index='{}']/android.widget.LinearLayout/"
                                                     "android.view.ViewGroup//android.widget.TextView"
                                                     "[contains(@resource-id, 'audio_parse_container')]".format(index))
        return analysis

    # 试卷部分需要根据文本查询选项是否被选中
    # @teststep
    # def opt_text_is_selected(self, opt_text):
    #     ele

    @teststep
    def single_choice_play_process(self, do_right=False, right_answer=None):
        """单选对错操作"""
        opt_text = self.opt_options()
        select_choice = ''
        if do_right:
            for x, opt in enumerate(opt_text):
                if opt.text in right_answer:
                    select_choice = opt.text
                    self.opt_char()[x].click()
                    break
        else:
            select_index = random.randint(0, len(opt_text) - 1)
            select_choice = opt_text[select_index].text
            opt_text[select_index].click()
        return select_choice

    @teststep
    def single_choice_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """单选操作"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.next_btn_judge('false', self.fab_next_btn)
            ques = self.question()[0].text
            print('问题：', ques)

            opt_char = self.opt_char()
            opt_text = self.opt_options()
            for j in range(len(opt_char)):
                print(opt_char[j].text, '  ', opt_text[j].text)

            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                select_answer = self.single_choice_play_process()
            else:
                right_answer = sec_answer[str(x)]
                select_answer = self.single_choice_play_process(do_right=True, right_answer=right_answer)
            print('选择答案：', select_answer)
            mine_answer[str(x)] = select_answer

            # 单选解析 操作
            if self.wait_check_analysis_tab_page():
                if self.wait_check_analysis_text_page():
                    analysis_text = self.analysis_text()
                    mine_answer[str(x)] = select_answer + '-' + analysis_text
                    print('解析：', self.analysis_text())
                else:
                    mine_answer[str(x)] = select_answer + '-无文字解析'
                    print('无文字解析')

                if self.wait_check_analysis_audio_page():
                    print('存在音频解析')
                    mine_answer[str(x)] = select_answer + '-音频解析'
                    self.analysis_audio_btn().click()
                    time.sleep(3)
            else:
                mine_answer[str(x)] = select_answer + '-无解析'

            timer.append(self.bank_time())
            self.fab_next_btn().click()
            print('-' * 20, '\n')
        self.judge_timer(timer)
        print('本次做题答案：', mine_answer)
        return mine_answer

    @teststeps
    def single_choice_result_operate(self, mine_answer, game_name):
        """页面滑动查看答案"""
        if game_name != '单项选择':
            self.drag_up_down(drag_down=False)

        again_right_answer = {}
        right_count = 0
        for x in range(len(mine_answer)):
            if x != len(mine_answer) - 1:
                index_num = x + 1
            else:
                index_num = x
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            while not self.wait_check_article_container_by_index(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.8, 500)

            question = self.get_question_by_bank_index(x).text
            print('问题：', question)
            options = self.get_opt_text_by_index(x)
            opt_chars = self.get_opt_char_by_index(x)
            mine_answer_with_analysis = mine_answer[str(x)]
            mine_done_answer = mine_answer_with_analysis.split('-')[0]
            print('我的答案：', mine_done_answer)

            for i, opt in enumerate(options):
                opt_char_content = opt_chars[i].get_attribute('contentDescription')
                if opt.text == mine_done_answer:
                    if not opt_char_content:
                        self.base_assert.except_error('选项已选择， 但是结果页未被选中')
                    else:
                        if opt_char_content == 'right':
                            right_count += 1
                            print('选项校验正确')
                            if game_name in ['阅读理解', '听后选择']:
                                again_right_answer[str(len(again_right_answer))] = opt.text
                else:
                    if opt_char_content == 'right':
                        again_right_answer[str(len(again_right_answer))] = opt.text
                    elif opt_char_content == 'error':
                        print('选项校验正确')

            if game_name == '单项选择':
                if self.wait_check_result_analysis_page(x):
                    if '无解析' in mine_answer_with_analysis:
                        self.base_assert.except_error('记录解析为无解析，答案页存在解析内容')

                    if self.wait_check_result_analysis_text_page(x):
                        analysis_text = self.get_analysis_text_by_index(x)
                        if analysis_text not in mine_answer_with_analysis:
                            self.base_assert.except_error('记录解析文本与答案页不同, 不为解析内容， 记录为%s' % mine_answer_with_analysis)

                    if self.wait_check_result_analysis_audio_page(x):
                        self.get_analysis_audio_by_index(x).click()
                        if '音频解析' not in mine_done_answer:
                            self.base_assert.except_error('记录解析与答案页不同，不为音频解析，记录为%s' % mine_answer_with_analysis)
                else:
                    if '无解析' not in mine_answer_with_analysis:
                        self.base_assert.except_error('记录解析为有解析，答案页不存在解析内容')
            print('-'*30, '\n')
        print('错题再练答案：', again_right_answer)
        return again_right_answer, right_count, len(mine_answer)

