#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:35
# -----------------------------------------
import random
import re
import string
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class FlashCardGame(GameCommonEle):
    @teststep
    def wait_check_flash_study_page(self):
        """学习模式页面检查点"""
        locator = (By.ID, self.id_type() + "side")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_copy_page(self):
        """抄写模式页面检查点 以键盘id作为索引"""
        locator = (By.ID, self.id_type() + "mine_word")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_sentence_page(self):
        """以“闪卡练习 -句子模式”的句子id为依据"""
        locator = (By.ID, self.id_type() + "sentence")
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_explain_page(self):
        """判断解释是否存在"""
        try:
            self.driver.find_element_by_id(self.id_type() + "tv_chinese")
            return True
        except:
            return False

    @teststep
    def wait_check_flash_result_page(self):
        """结果页页面检查点"""
        locator = (By.XPATH, "//*[@text='完成学习']")
        return self.get_wait_check_page_result(locator)

    @teststep
    def study_word(self):
        """页面单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_english')
        return ele.text

    @teststep
    def copy_word(self):
        """抄写页面单词"""
        ele = self.driver.find_element_by_id('{}english'.format(self.id_type()))
        return ele.text

    @teststep
    def copy_explain(self):
        """抄写模式单词解释"""
        ele = self.driver.find_element_by_id('{}chinese'.format(self.id_type()))
        return ele

    @teststep
    def copy_input(self):
        """抄写模式输入答案"""
        ele = self.driver.find_element_by_id('{}mine_word'.format(self.id_type()))
        return ele

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver.find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def pattern_switch(self):
        """点击右上角的全英/英汉，切换模式"""
        self.driver \
            .find_element_by_id(self.id_type() + "side") \
            .click()

    @teststep
    def author(self):
        """例句推荐老师"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "author")
        return english.text

    @teststep
    def english_study(self):
        """全英模式 页面内展示的word"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "tv_english")
        return english.text

    @teststep
    def study_word_explain(self):
        """英汉模式 页面内展示的word解释"""
        explain = self.driver.find_element_by_id(self.id_type() + "tv_chinese")
        return explain

    @teststep
    def study_sentence(self):
        """全英模式 页面内展示的句子"""
        english = self.driver \
            .find_element_by_id(self.id_type() + "sentence").text
        return english

    @teststep
    def study_sentence_explain(self):
        """英汉模式 页面内展示的句子解释"""
        explain = self.driver \
            .find_element_by_id(self.id_type() + "sentence_explain").text
        return explain

    @teststep
    def star_button(self):
        """星标按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "iv_star")
        return ele

    @teststep
    def familiar_button(self):
        """熟词按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "expert")
        return ele

    @teststep
    def change_model_btn(self):
        """英汉切换按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'side')
        return ele

    # 结果页元素
    @teststep
    def study_sum(self):
        """学习统计"""
        ele = self.driver.find_element_by_id(self.id_type() + 'study_sum')
        return ele.text

    @teststep
    def get_start_sum(self):
        """星星标记个数"""
        return int(re.findall(r'\d+', self.study_sum())[1])

    @teststep
    def study_again(self):
        """再学一遍"""
        ele = self.driver.find_element_by_id(self.id_type() + 'study_again')
        return ele

    @teststep
    def study_star_again(self):
        """把标星的单词再练一遍"""
        ele = self.driver.find_element_by_id(self.id_type() + 'star_again')
        return ele

    @teststep
    def result_words(self):
        """结果页单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_word')
        return ele

    @teststep
    def word_voice(self, word):
        """单词左侧声音按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/preceding-sibling::android.widget.ImageView'
                                                '[contains(@resource-id,"{}iv_voice")]'.format(word, self.id_type()))
        return ele

    @teststep
    def word_explain(self, word):
        """单词对应的解释"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../following-sibling::android.widget.LinearLayout/'
                                                'android.widget.TextView'.format(word))
        return ele.text

    @teststep
    def word_star(self, word):
        """单词对应的星标按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../../following-sibling::android.widget.ImageView'
                                                .format(word))
        return ele

    @teststep
    def sentence_voice(self, sentence):
        """句子左侧喇叭按钮"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../preceding-sibling::android.widget.ImageView'
                                                '[contains(@resource-id,"{}iv_voice")]'.format(sentence, self.id_type()))
        return ele

    @teststep
    def sentence_explain(self, sentence):
        """句子对应的解释"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/following-sibling::android.widget.TextView'.format(sentence))
        return ele.text

    @teststep
    def sentence_star(self, sentence):
        """句子的标星"""
        ele = self.driver.find_element_by_xpath('//*[@text="{}"]/../following-sibling::android.widget.ImageView'
                                                .format(sentence))
        return ele


    @teststep
    def flash_card_game_operate(self, fq, half_exit, star_list=None, ):
        """图书馆、作业内闪卡游戏过程"""
        flash_type = 0
        star_words = [] if fq == 1 else star_list
        if self.wait_check_flash_study_page():
            total_num = self.rest_bank_num()
            for x in range(0, total_num):
                self.rate_judge(total_num, x)  # 待完成数校验
                self.next_btn_judge('true', self.fab_next_btn)  # 下一步按钮状态检验
                self.click_voice()
                word = self.study_word()
                print('单词：', word)

                if half_exit:
                    if x == 1:
                        self.click_back_up_button()
                        self.tips_operate()

                if not self.wait_check_explain_page():  # 验证页面是否默认选择英汉模式
                    self.base_assert.except_error('未发现单词解释，页面没有默认选择英汉模式' + word)
                else:
                    print('解释：', self.study_word_explain().text)  # 单词解释

                if self.wait_check_sentence_page():
                    flash_type = 1
                    print("句子：", self.study_sentence())  # 句子
                    print("句子解释：", self.study_sentence_explain())  # 句子解释
                    print("推荐老师：", self.author())  # 推荐老师

                self.change_model_btn().click()  # 切换全英模式
                if self.wait_check_explain_page():  # 校验翻译是否出现
                    self.base_assert.except_error('切换至全英模式依然存在解释' + word)

                self.change_model_btn().click()  # 切换回英汉模式

                if x % 2 == 0:  # 第一次，部分单词点击标星按钮
                    if fq == 1:
                        self.star_button().click()
                        star_words.append(word)
                        print('加入标星单词')
                    else:
                        if GetAttribute().get_selected(self.star_button()) == 'true':
                            print('标星校验正确')
                        else:
                            self.base_assert.except_error('单词已标星但标星按钮未被选中')

                print('-' * 20, '\n')
                self.fab_next_btn().click()
                time.sleep(2)
            return total_num, star_words, flash_type

    @teststep
    def flash_copy_game_operate(self,  fq, half_exit, star_list=None,):
        flash_type = 1
        star_words = [] if fq == 1 else star_list
        if self.wait_check_copy_page():
            total_num = self.rest_bank_num()
            for x in range(total_num):
                self.click_voice()
                self.rate_judge(total_num, x)
                copy_word = self.copy_word()
                print('单词：', copy_word)
                if half_exit:
                    if x == 1:
                        self.click_back_up_button()
                        self.tips_operate()
                        break

                if x % 2 == 0:  # 奇数题
                    if fq == 1:  # 若为第一次
                        self.star_button().click()  # 标星
                        star_words.append(copy_word)
                        print('加入标星单词')
                    else:  # 若为第二次 校验是否被标星
                        if GetAttribute().get_selected(self.star_button()) == 'true':
                            print('标星校验正确')
                        else:
                            self.base_assert.except_error('单词已标星但标星按钮未被选中')

                self.copy_input().click()
                time.sleep(1)
                if x == 1:
                    random_str = random.sample(string.ascii_lowercase, 4)  # 随机输入错误单词，
                    for j, s in enumerate(random_str):
                        Keyboard().keyboard_operate(s, j)
                    print('输入单词：', ''.join(random_str))

                    if self.copy_word() != copy_word:  # 验证是否跳转到下一题
                        self.base_assert.except_error('输入错误单词可以进入下一题')

                    for y in range(4):  # 清除输入的单词
                        Keyboard().games_keyboard('backspace')
                    time.sleep(1)

                for j, s in enumerate(list(copy_word)):  # 输入抄写单词
                    Keyboard().keyboard_operate(s, j)
                time.sleep(3)
                print('-' * 30, '\n')
            return total_num, star_words, flash_type

    @teststeps
    def flash_card_result_operate(self, flash_result):
        """闪卡结果页面处理"""
        total, star_words, flash_type = flash_result

        # if self.wait_check_medal_page():
        #     print('获取勋章')
        #     self.click_back_up_button()

        if self.wait_check_flash_result_page():
            print('完成学习！')
            summary = self.study_sum()
            print(summary, '\n')
            full_count = int(re.findall(r'\d+', summary)[0])  # 页面统计总个数
            star_count = self.get_start_sum()

            if full_count != total:
                self.base_assert.except_error('页面统计个数与做题个数不一致')

            if len(star_words) != star_count:
                self.base_assert.except_error('标星个数与页面统计个数不一致')

            self.cancel_or_add_star(total, star_words, flash_type, cancel=True)
            if self.get_start_sum() != 0:
                self.base_assert.except_error('单词标星取消，页面标星统计数未发生变化，与实际标星数不一致')

            self.study_star_again().click()
            if Toast().find_toast('没有标记★的内容'):
                print('没有标记★的内容\n')
            else:
                self.base_assert.except_error('未提示没有标星单词')

            self.cancel_or_add_star(total, star_words, flash_type)
            self.study_star_again().click()


    @teststep
    def cancel_or_add_star(self, total, star_words, flash_type, cancel=False):
        """添加或取消标星"""
        word_list = []
        while True:
            words = self.result_words()
            for i, w in enumerate(words):
                if w.text in word_list:
                    continue
                else:
                    if i == len(words) - 1:
                        self.screen_swipe_up(0.5, 0.8, 0.72, 1000)
                    result_word = w.text
                    word_list.append(result_word)
                    if flash_type:
                        word_voice = self.word_voice(result_word)
                        word_explain = self.word_explain(result_word)
                        word_star = self.word_star(result_word)
                    else:
                        word_voice = self.sentence_voice(result_word)
                        word_explain = self.sentence_explain(result_word)
                        word_star = self.sentence_star(result_word)

                    word_voice.click()

                    if cancel:
                        print('单词：', result_word)
                        print('解释', word_explain)
                        if GetAttribute().get_selected(word_star) == 'true':
                            word_star.click()
                            print('取消标星')
                            star_words.remove(result_word)
                        print('-' * 20, '\n')
                    else:
                        if i == 2 or i == 4:
                            print('单词：', result_word, end='\t')
                            word_star.click()
                            print('添加标星')
                            star_words.append(result_word)
                            print('-' * 20, '\n')

            if len(word_list) != total:
                self.screen_swipe_up(0.5, 0.8, 0.3, 1000)
            else:
                break
        self.screen_swipe_down(0.5, 0.2, 0.8, 1000)

    @teststep
    def play_flash_game(self, half_exit):
        """闪卡的总体流程"""
        if self.wait_check_flash_study_page():
            first_result = self.flash_card_game_operate(fq=1, half_exit=half_exit)
            if not half_exit:
                self.flash_card_result_operate(first_result)
                self.flash_card_game_operate(fq=2, half_exit=half_exit, star_list=first_result[1],)
        elif self.wait_check_copy_page():
            first_result = self.flash_copy_game_operate(fq=1, half_exit=half_exit)
            if not half_exit:
                self.flash_card_result_operate(first_result)
                self.flash_copy_game_operate(fq=2, half_exit=half_exit, star_list=first_result[1])

        if not half_exit:
            if self.wait_check_flash_result_page():
                print(self.study_sum())
            self.click_back_up_button()

