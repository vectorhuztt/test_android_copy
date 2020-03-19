#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/30 10:14
# -----------------------------------------
import random
import string

from math import floor
from selenium.webdriver.common.by import By

from app.honor.student.games.word_spell import SpellWordGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book_rebuild.object_page.word_test_sql_handler import WordTestSqlHandler
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.dict_slice import dict_slice
from utils.games_keyboard import Keyboard


class WordTestPage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.sql_handler = WordTestSqlHandler()
        self.spell = SpellWordGame()

    @teststep
    def wait_check_no_test_word_page(self):
        """测试次数不足页面检查点"""
        locator = (By.XPATH, '//android.widget.Button[contains(@text,"确定")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_start_test_page(self):
        """开始测试页面检查点"""
        locator = (By.XPATH, '//android.widget.Button[contains(@text,"开始复习")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_preview_word_page(self):
        """单词预览页面检查点"""
        locator = (By.ID, self.id_type() + "start")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_select_word_count_page(self):
        """单词测试数页面检查点"""
        locator = (By.ID, self.id_type() + "num_hint")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_test_game_page(self):
        """单词测试游戏页面检查点"""
        locator = (By.ID, self.id_type() + "time")
        return self.get_wait_check_page_result(locator)

    @teststep
    def word_count_select_tab(self):
        """单词测试数选项"""
        ele = self.driver.find_elements_by_xpath('//android.support.v7.widget.RecyclerView[contains(@resource-id, "test_num_container")]/'
                                                 'android.view.ViewGroup/android.widget.TextView')
        return ele

    @teststep
    def word_test_type(self):
        """测试类型"""
        ele = self.driver.find_elements_by_xpath("//android.support.v7.widget.RecyclerView[contains(@resource-id, 'test_type_container')]/"
                                                 "android.view.ViewGroup/android.widget.TextView")
        return ele


    @teststep
    def click_word_test_tab(self):
        """点击单词测试按钮"""
        self.driver.find_element_by_id(self.id_type() + "word_test").click()

    @teststep
    def click_confirm_btn(self):
        """点击复习或者确定按钮"""
        self.driver.find_element_by_id(self.id_type() + "next").click()

    @teststep
    def click_start_test_btn(self):
        """点击开始测试按钮"""
        self.driver.find_element_by_id(self.id_type() + "start").click()

    @teststep
    def preview_explain(self):
        """预览单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + "explain")
        return ele

    @teststep
    def preview_voice_icon(self, explain):
        """预览单词喇叭图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/preceding-sibling'
                                                '::android.widget.ImageView'.format(explain))
        return ele

    @teststep
    def preview_word(self, explain):
        """预览单词解释"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/preceding-sibling::'
                                                'android.widget.TextView[contains(@resource-id,"word")]'.format(explain))
        return ele

    @teststep
    def test_select_page_operate(self, tab_index):
        """单词测试数页面操作过程"""
        if self.wait_check_select_word_count_page():
            select_tab = self.word_count_select_tab()
            test_type = self.word_test_type()
            for x in select_tab:
                if '50' in x.text:
                    if x.get_attribute('selected') != 'true':
                        self.base_assert.except_error('单词个数没有默认选择50')
                    break

            if test_type[0].get_attribute("selected") != "true":
                self.base_assert.except_error("默写类型没有被选中")

            test_count = int(select_tab[tab_index].text)
            print('test_count:', test_count)
            if test_count is None:
                self.base_assert.except_error('未获取单词个数')

            select_tab[tab_index].click()
            self.click_confirm_btn()
            return test_count

    @teststep
    def get_test_word_list(self, fvalue_glt_3_words, test_fail_words, test_pass_words, tab_index):
        """获取测试单词数
            :param fvalue_glt_3_words: 未测且F值大于3的单词
            :param test_fail_words:  测试失败单词
            :param test_pass_words: 测试通过单词
            :param tab_index: 选择题目个数
        """
        # 测试数量小于未测单词数   取未测单词数[:测试数量]
        # 测试数量大于未测单词数  需补充测试未通过单词 获取补充数量 测试数-未测单词数
        # 若补充数小于测试未通过数， 去补充数，测试单词未未测+未通过[:补充]
        # 若补充数大于测试未通过单词数，需补充测试通过单词 获取补充数量2 补充数 - 未通过单词
        # 若补充数量2小于测试通过单词数， 测试数为  未测 + 未通过 + 通过[:补充数量2]
        # 若补充数量2大于测试通过单词数， 测试数为  未测 + 未通过 + 通过

        test_count = self.test_select_page_operate(tab_index)
        dcg_value = test_count - len(fvalue_glt_3_words)
        if dcg_value <= 0:
            test_word_list = dict_slice(fvalue_glt_3_words, end=test_count)
        else:
            test_word_list = fvalue_glt_3_words
            if dcg_value <= len(test_fail_words):
                fail_words = dict_slice(test_fail_words, end=dcg_value)
                test_word_list.update(fail_words)
            else:
                test_word_list.update(test_fail_words)
                ddf_value = dcg_value - len(test_pass_words)
                if ddf_value <= 0:
                    pass_words = dict_slice(test_pass_words, end=dcg_value)
                else:
                    pass_words = test_pass_words
                test_word_list.update(pass_words)
        return test_word_list if test_word_list else {}

    @teststeps
    def check_preview_word_operate(self, test_word_info):
        """预览单词校验操作"""
        # 循环遍历单词与解释，对比已获得的测试单词，判断是否在测试列表中，解释是否合并或者相同
        test_answer = {}
        word_id_list = []
        if self.wait_check_preview_word_page():
            explain_list = []
            while len(explain_list) < len(test_word_info):
                if self.wait_check_preview_word_page():
                    preview_explain = self.preview_explain()
                    for i, x in enumerate(preview_explain):
                        if x.text in explain_list:
                            continue
                        else:
                            word = self.preview_word(x.text)
                            word_id = word.get_attribute('contentDescription')
                            word_id_list.append(word_id)
                            explain_list.append(x.text)
                            test_answer[x.text] = word.text

                            if word_id not in list(test_word_info.keys()):
                                self.base_assert.except_error('此单词不在测试单词列表内， 但是出现在预览列表中 ' + word_id)
                            else:
                                explain_info = test_word_info[word_id]
                                query_explains = self.sql_handler.get_word_explain_list(explain_info)
                                page_explain_list = x.text.split('；')
                                page_explain_list.sort()
                                query_explains.sort()
                                if query_explains != page_explain_list:
                                    self.base_assert.except_error("页面单词不等于单词解释集合 " + word_id)

                                voice_icon = self.preview_voice_icon(x.text)
                                voice_icon.click()
                self.screen_swipe_up(0.5, 0.9, 0.45, 1000)
            print('页面单词id列表, ', word_id_list)
        return test_answer, word_id_list

    @teststeps
    def play_test_word_spell_operate(self, test_count, test_answer, do_pass, no_wrong=False):
        """单词默写游戏过程
           :param no_wrong: 是否做全对
           :param test_count: 测试单词个数
           :param test_answer: 预览时记录的答案
           :param do_pass: 测试是否达到90%
        """
        if self.wait_check_test_game_page():
            game_count = self.spell.rest_bank_num()
            if test_count != game_count:
                self.base_assert.except_error("默写数量与测试单词数不一致")

            if no_wrong:
                wrong_count = 0
            else:
                if do_pass:
                    wrong_count = floor(game_count * 0.1)
                else:
                    wrong_count = floor(game_count * 0.1) + 2

            timer = []
            game_word_id_list = []
            wrong_index = list(range(wrong_count))
            for x in range(game_count):
                self.spell.next_btn_judge('false', self.spell.fab_commit_btn)  # 判断下一题按钮状态
                self.spell.rate_judge(game_count, x)  # 校验剩余题数
                explain = self.spell.word_explain().text
                print('解释：', explain)
                self.spell.normal_word_spell_hint_word_check()

                if x in wrong_index:
                    self.spell.word_spell_play_process(game_mode=1)
                    self.spell.next_btn_operate("true", self.spell.fab_commit_btn)
                    if not self.spell.wait_check_right_answer_page():
                        self.base_assert.except_error("拼写单词错误，提交后未显示正确答案" + explain)
                    else:
                        print("正确答案：", self.spell.right_answer_word())
                else:
                    right_answer = test_answer[explain]
                    self.spell.word_spell_play_process(game_mode=1, do_right=True, right_answer=right_answer)
                    self.spell.next_btn_operate("true", self.spell.fab_commit_btn)
                    print('正确答案：', right_answer)

                mine_input_word = self.spell.spell_word()
                word_id = mine_input_word.get_attribute('contentDescription')
                game_word_id_list.append(word_id)
                print('输入答案：', mine_input_word.text[::2])
                timer.append(self.spell.bank_time())

                self.spell.click_voice()
                self.spell.fab_next_btn().click()
                print('-'*30, '\n')
            self.spell.judge_timer(timer)  # 时间校验
            return wrong_count, game_word_id_list






