#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:38
# -----------------------------------------
import re
import time

from math import ceil
from selenium.webdriver.common.by import By
from app.honor.student.games.word_spell import SpellWordGame
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class LinkWordGame(SpellWordGame):
    @teststep
    def wait_check_word_match_page(self):
        """连连看页面检查点"""
        locator = (By.ID, '{}mg_1'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_result_image_page(self):
        """结果页图片页面检查点"""
        locator = (By.ID, '{}img'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def get_word_cards(self):
        """获取所有卡片"""
        cards = self.driver.find_elements_by_xpath('//*[contains(@resource-id, "mg_")]/android.widget.TextView')
        return cards

    @teststep
    def is_hans(self, word):
        """判断 是否为字母"""
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        if pattern.search(word):
            return True
        else:
            return False

    @teststep
    def get_img_status_by_text(self, text):
        """根据文本内容获取卡片状态"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/following-sibling::android.view.View'.format(text))
        return ele.get_attribute('selected')

    @teststep
    def get_ch_or_en_cards(self, text_mode=True, hans=True):
        """获取英文卡片"""
        cards_list = []
        for x in self.get_word_cards():
            text_is_hans = self.is_hans(x.text)
            if text_mode:
                if hans:
                    if text_is_hans and self.get_img_status_by_text(x.text) == 'false':
                        cards_list.append(x)
                else:
                    if not text_is_hans and self.get_img_status_by_text(x.text) == 'false':
                        cards_list.append(x)
            else:
                if hans:
                    if not x.text:
                        cards_list.append(x)
                else:
                    if x.text:
                        cards_list.append(x)

        return cards_list

    @teststep
    def is_image_text_mode(self):
        """判断是否是图文模式"""
        no_text_cards = [x for x in self.get_word_cards() if not x.text]
        if len(no_text_cards):
            return True
        else:
            return False

    @teststep
    def result_words(self):
        """结果页图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'word')
        return ele

    @teststep
    def get_result_voice_by_word_ele(self, word):
        """根据图片元素获取结单词喇叭按钮"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/preceding-sibling::'
                                                'android.widget.ImageView[contains(@resource-id, "audio")]'.format(word))
        return ele

    @teststep
    def get_result_icon_by_word_ele(self, word):
        """根据图片元素获取结果单词"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/following-sibling::'
                                                'android.widget.ImageView[contains(@resource-id, "result")]'.format(word))
        return ele

    @teststep
    def get_result_explain_by_word_ele(self, word):
        """根据图片元素获取结果页单词解释"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/following-sibling::'
                                                'android.widget.TextView[contains(@resource-id, "explain")]'.format(word))
        return ele

    @teststeps
    def word_match_lib_hw_operate(self, fq, half_exit):
        """连连看游戏过程"""
        if self.wait_check_word_match_page():
            text_mode = False if self.is_image_text_mode() else True
            total_num = self.rest_bank_num()
            print('总题数：', total_num, '\n')
            timer = []
            mine_answer = {}
            if fq == 1:
                tips = []
                while len(tips) < total_num:
                    if self.wait_check_word_match_page():
                        if half_exit:
                            if len(tips) == 1:
                                self.click_back_up_button()
                                self.tips_operate()
                                break
                        hans_card = self.get_ch_or_en_cards(text_mode=text_mode, hans=True)
                        for ch in hans_card:
                            hans_text = ch.text
                            tips.append(hans_text)
                            reset_num = self.rest_bank_num()
                            english_card = self.get_ch_or_en_cards(text_mode=text_mode, hans=False)
                            for en in english_card:
                                english_word = en.text
                                if self.rest_bank_num() != 1:
                                    ch.click()
                                    en.click()
                                    time.sleep(0.8)
                                    if self.rest_bank_num() < reset_num:
                                        timer.append(self.bank_time())
                                        mine_answer[str(len(tips) -1)] = english_word
                                        print('单词解释：', hans_text)
                                        print('英文：', english_word)
                                        print('-'*30, '\n')
                                        break
                                else:
                                    mine_answer[str(len(tips) - 1)] = english_word
                                    print('单词解释：', hans_text)
                                    print('英文：', english_word)
                                    print('-' * 30, '\n')
                                    timer.append(self.bank_time())
                                    ch.click()
                                    en.click()
                                    break
                        time.sleep(2)
                self.judge_timer(timer)
                print('本次做题答案：', mine_answer)
            else:
                pass
            return mine_answer

    @teststeps
    def word_match_result_operate(self, mine_answer):
        """连连看结果页处理"""
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
            self.group_word_voice(x).click()
            result_icon = self.group_right_wong_icon(x)
            print('解释：', result_explain)
            print('单词：', result_word)

            if GetAttribute().get_selected(result_icon) == 'false':
                self.base_assert.except_error('单词判断状态为错误！' + result_word)
            else:
                print('图标标识正确\n')

        return {}, len(mine_answer), len(mine_answer)

