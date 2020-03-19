#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/3 10:59
# -----------------------------------------
import json
import time

import numpy as np
from math import floor

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.games.listen_spell_page import ListenSpellWordPage
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from app.honor.student.word_book_rebuild.object_page.games.restore_word_page import WordRestore
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord
from app.honor.student.word_book_rebuild.object_page.games.vocabulary_choose_page import VocabularyChoose
from app.honor.student.word_book_rebuild.object_page.games.word_match_page import MatchingWord
from conf.base_page import BasePage
from conf.decorator import teststep


class WordBookRebuildPage(BasePage):

    def __init__(self):
        super().__init__()
        self.data = WordDataHandlePage()
        self.public = WorldBookPublicPage()
        self.data_dir = 'app/honor/student/word_book_rebuild/test_data/'

    @teststep
    def wait_check_start_page(self):
        """将'你准备好了吗?'作为 单词本首页 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '你准备好了吗?')]")
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_continue_page(self):
        """单词继续学习页面检查点"""
        locator = (By.ID, self.id_type() + "word_continue")
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_start_wrong_again_page(self):
        """错题题再练页面"""
        locator = (By.ID, self.id_type() + "word_continue")
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_game_title_page(self):
        """游戏标题页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_title')
        return self.get_wait_check_page_result(locator)

    @teststep
    def word_start_button(self):  # Go标志按钮
        self.driver \
            .find_element_by_id(self.id_type() + "word_start")\
            .click()
        time.sleep(3)

    @teststep
    def word_continue_button(self):
        """继续练习按钮"""
        self.driver.\
            find_element_by_id(self.id_type() + 'word_continue')\
            .click()
        time.sleep(3)

    @teststep
    def total_word(self):
        """已背单词 数"""
        word = self.driver \
            .find_element_by_id(self.id_type() + "total").text
        return int(word)

    @teststep
    def confirm_btn(self):
        """错题再练开始练习按钮"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "confirm")
        return ele

    @teststep
    def write_words_to_file(self, file_name, file_value):
        """将数据存入文件"""
        with open(self.data_dir + file_name, 'w', encoding='utf-8') as f:
            if '.json' in file_name:
                json.dump(file_value, f, ensure_ascii=False)
            elif '.txt' in file_name:
                f.write(','.join(file_value))

    @teststep
    def read_words_info_from_file(self, file_name):
        """从json文件中读取数据"""
        file_value = 0
        with open(self.data_dir + file_name, 'r', encoding='utf-8') as f:
            if '.json' in file_name:
                file_value = json.load(f)
            elif '.txt' in file_name:
                file_value = [x for x in f.read().split(',') if x]

        return file_value


    @teststep
    def set_do_right_by_familiar_type(self, familiar_type, group_count):
        """根据标熟类型设置是否做对"""
        do_right = 0
        if familiar_type in [1, 2, 3]:
            do_right = False
        elif familiar_type in [4, 5]:
            if group_count == 0:
                do_right = True
            else:
                do_right = False
        return do_right

    @teststep
    def group_operate(self, need_recite_count):
        """分组操作"""
        if need_recite_count <= 10:      # 个数小于10 分为一组
            group = [need_recite_count]
        elif 10 < need_recite_count < 21:   # 个数为11-20 分为两组
            group = [floor(need_recite_count/2), need_recite_count-floor(need_recite_count/2)]

        else:
            if need_recite_count > 30:     # 个数为 20 -30 或者 >30(做30处理) 分三组
                need_recite_count = 30
            third_division = floor(need_recite_count / 3)
            second_division = floor((need_recite_count - third_division)/2)
            reset_part = need_recite_count - third_division - second_division
            group = [third_division, second_division, reset_part]
        return group

    @teststep
    def check_new_word_after_recite_process(self, flash_result, group_recite_count, group_count, study_model=1):
        """校验新词奖励个数"""
        boundary_value = 28 if study_model == 1 else 17       # 根据学习类型设置边界值
        if flash_result:
            if group_count == 0:
                if group_recite_count < boundary_value:
                    if len(flash_result[0]) > 10:
                        print('❌❌❌ 新词奖励个数大于10个')
            else:
                if len(flash_result[0]) not in range(3, 11):
                    print('❌❌❌ 复习的新词奖励个数不在3-10之间', len(flash_result[0]))
        else:
            if group_recite_count < boundary_value:
                print('❌❌❌ 复习个数小于“{}”, 未有新词奖励'.format(boundary_value))

    @teststep
    def from_wordbook_back_to_home(self):
        """从单词本中退回主页面"""
        self.click_back_up_button()
        GameCommonEle().tips_operate()
        if self.wait_check_continue_page():
            self.click_back_up_button()


    @teststep
    def normal_study_new_word_operate(self, stu_id, flash_result, do_right):
        """单词学习过程"""
        group_word_answers = flash_result[-1]
        group_word_explains = list(flash_result[0].values())
        star_words = flash_result[2]
        familiar_explain_ids = list(flash_result[1].keys())
        group_new_explain_words = flash_result[3]
        remove_familiar = list(np.setdiff1d(group_word_explains, familiar_explain_ids))
        remove_repeat_words = list(np.setdiff1d(remove_familiar, group_new_explain_words))
        remove_repeat_count = len(remove_repeat_words)
        print('本组所有单词：', group_word_explains)
        print('本组标星单词：', star_words)
        print('本组标熟单词：', familiar_explain_ids)
        print('本组不去新释义做题数：', remove_familiar)
        print('本组新释义单词：', group_new_explain_words)
        print('本组去除重复单词数：', remove_repeat_count, '\n')

        while self.wait_check_game_title_page():
            title_ele = self.public.game_title()
            game_title = title_ele.text
            mode_id = int(title_ele.get_attribute('contentDescription').split('  ')[1])

            if '闪卡练习' in game_title and mode_id == 2:
                copy_count = FlashCard().flash_copy_model(star_words, group_new_explain_words)
                if self.wait_check_game_title_page():
                    if copy_count != len(star_words):
                        self.base_assert.except_error('标星个数与抄写个数不一致')

            elif '单词拼写(新词)' in game_title or '单词拼写(新释义)' in game_title:
                spell_count = SpellingWord().new_word_spell_operate(flash_result[1], group_new_explain_words)
                print('单词拼写个数', spell_count)
                if self.wait_check_game_title_page():
                    if spell_count != len(familiar_explain_ids):
                        self.base_assert.except_error('标熟个数与拼写个数不一致')

            elif '词汇选择(新词)' in game_title:
                if do_right:   # 词汇选择做对操作
                    VocabularyChoose().right_listen_select_operate(stu_id, remove_repeat_count, group_new_explain_words)
                else:          # 词汇选择随机选择操作
                    VocabularyChoose().normal_listen_select_operate(remove_repeat_count, group_new_explain_words)

            elif '连连看' in game_title:
                MatchingWord().link_link_game_operate(len(remove_familiar), group_word_answers)

            elif '还原单词' in game_title:
                if do_right:    # 还原单词做对操作
                    WordRestore().right_restore_word_operate(stu_id, remove_repeat_count, group_new_explain_words)
                else:           # 还原单词做错后做对操作
                    WordRestore().restore_word_operate(stu_id, remove_repeat_count, group_new_explain_words)

            elif '单词听写' in game_title:
                if do_right:   # 单词听写做对操作
                    ListenSpellWordPage().right_listen_spell_operate(stu_id, remove_repeat_count, group_new_explain_words)
                else:          # 单词听写做错后做对操作
                    ListenSpellWordPage().normal_listen_spell_operate(remove_repeat_count, group_new_explain_words)
            else:
                break
        return remove_repeat_words

    @teststep
    def recite_word_operate(self, stu_id, level, wrong_again_words, right_explains):
        """单词复习过程"""
        recite_new_explains = self.data.get_recite_new_explains(stu_id, level)  # 已学新释义单词，需跳过单词拼写游戏
        recite_new_words = self.data.get_word_list_by_explains(stu_id, recite_new_explains)
        print('新释义解释：', recite_new_explains)
        print('新释义单词：', recite_new_words)
        print('新释义单词个数：', len(recite_new_words), '\n')

        right_words = self.data.get_word_list_by_explains(stu_id, right_explains)
        print('新词非标熟且全对单词：', right_words)
        print('新词非标熟且全对个数', len(right_words), '\n')

        recite_b_explains = self.data.get_recite_level_one_explains(stu_id)  # 获取一轮复习单词的个数
        recite_b_words = self.data.get_word_list_by_explains(stu_id, recite_b_explains)  # 根据解释id获取单词
        print('B轮需要复习的解释：', recite_b_explains)
        print('B轮需要复习的单词：', recite_b_words)
        print('B轮需要复习的个数：', len(recite_b_words), '\n')


        vocab_select_words = list(np.setdiff1d(recite_b_words, right_words))
        vocab_select_count = len(vocab_select_words)  # 词汇选择或者词汇运用的个数
        print('B轮词汇选择单词：', vocab_select_words)
        print('B轮词汇选择个数：', vocab_select_count, '\n')

        only_apply_explains = list(np.intersect1d(recite_new_explains, right_explains))  # 只有词汇运用的单词
        only_apply_words = list(np.intersect1d(recite_new_words, right_words))
        print('B轮单独复习词汇运用的解释：', only_apply_explains)
        print('B轮单独复习词汇运用的单词:', only_apply_words)
        print('B轮单独复习词汇运用个数：', len(only_apply_words), '\n')

        recite_b_vocab_apply_words = list(np.hstack((vocab_select_words, only_apply_words)))
        recite_b_vocab_apply_count = len(recite_b_vocab_apply_words)
        print('B轮复习词汇运用单词：', recite_b_vocab_apply_words)
        print('B轮复习词汇运用个数：', recite_b_vocab_apply_count, '\n')

        recite_b_spell_explains = list(np.setdiff1d(recite_b_explains, recite_new_explains))  # 需要复习单词拼写的单词
        recite_b_spell_words = self.data.get_word_list_by_explains(stu_id, recite_b_spell_explains)
        print('B轮单词拼写解释：', recite_b_spell_explains)
        print('B轮单词拼写单词：', recite_b_spell_words)
        print('B轮单词拼写单词个数：', len(recite_b_spell_words), '\n')


        recite_cde_vocab_apply_explains = self.data.get_recite_level_more_than_one_explains(stu_id, level)    # 获取F值=level的解释id
        recite_cde_vocab_apply_words = self.data.get_word_list_by_explains(stu_id, recite_cde_vocab_apply_explains)  # 根据解释id获取单词
        print('C/D/E轮词汇运用的解释：', recite_cde_vocab_apply_explains)
        print('C/D/E轮词汇运用的单词：', recite_cde_vocab_apply_words)
        print('C/D/E轮词汇运用的个数：', len(recite_cde_vocab_apply_words), '\n')


        recite_cde_spell_explains = list(np.setdiff1d(recite_cde_vocab_apply_explains, recite_new_explains))  # 需要复习单词拼写的单词
        recite_cde_spell_words = self.data.get_word_list_by_explains(stu_id, recite_cde_spell_explains)
        print('C/D/E轮单词拼写解释：', recite_cde_spell_explains)
        print('C/D/E轮单词拼写单词：', recite_cde_spell_words)
        print('C/D/E轮单词拼写单词个数：', len(recite_cde_spell_words), '\n')

        all_vocab_select_words = vocab_select_words
        all_vocab_apply_words = list(set(list(np.hstack((recite_b_vocab_apply_words, recite_cde_vocab_apply_words)))))
        all_spell_words = list(set(list(np.hstack((recite_b_spell_words, recite_cde_spell_words)))))
        print('词汇选择总数：', len(all_vocab_select_words))
        print('词汇运用总数：', len(all_vocab_apply_words))
        print('单词拼写总数：', len(all_spell_words), '\n')

        vocab_select_group = self.group_operate(len(all_vocab_select_words))
        vocab_apply_group = self.group_operate(len(all_vocab_apply_words))
        word_spell_group = self.group_operate(len(all_spell_words))
        all_group = [vocab_select_group, vocab_apply_group, word_spell_group]
        max_length = max((len(l) for l in all_group))
        reform_group = list(map(lambda x: x + [0]*(max_length - len(x)), all_group))

        vocab_select_group = reform_group[0]
        vocab_apply_group = reform_group[1]
        word_spell_group = reform_group[2]

        print('词汇选择分组：', vocab_select_group)
        print('词汇运用分组：', vocab_apply_group)
        print('单词拼写分组：', word_spell_group, '\n')

        for x in range(len(vocab_select_group)):
            while self.wait_check_game_title_page():
                title_ele = self.public.game_title()
                game_title = title_ele.text
                print(game_title)
                mode_id = int(title_ele.get_attribute('contentDescription').split()[1])

                if '词汇选择(复习)' in game_title:
                    if len(recite_b_words) < 3:             # 若F=1的单词个数小于3 ，则不应出现词汇选择
                        self.base_assert.except_error('一轮复习单词不足3个，不应出现词汇选择游戏')

                    if not vocab_select_group[x]:
                        self.base_assert.except_error('词汇选择分组为0， 不应出现词汇选择游戏')

                    if mode_id == 1:                       # mode=1 , 根据单词选解释游戏
                        VocabularyChoose().vocab_select_choice_explain(vocab_select_group[x], wrong_again_words)
                    else:                                  # mode=2， 根据解释选单词
                        VocabularyChoose().vocab_select_choice_word(stu_id, vocab_select_group[x], wrong_again_words)

                    if '词汇选择(复习)' in self.public.game_title().text:  # 判断一组结束后是否还会出现词汇选择游戏
                        self.base_assert.except_error('词汇选择个数与计算个数不一致！')
                        break

                elif '词汇运用(复习)' in game_title:
                    if not vocab_apply_group[x]:
                        self.base_assert.except_error('词汇运用分组为0， 不应出现词汇运用游戏')


                    VocabularyChoose().vocab_apply(stu_id, vocab_apply_group[x], right_words, recite_new_explains)   # 词汇运用游戏过程
                    if self.wait_check_game_title_page():
                        if '词汇运用(复习)' in self.public.game_title().text:  # 判断一组结束后是否还会出现词汇选择游戏
                            self.base_assert.except_error('词汇运用组数与计算个数不一致！')
                            break

                elif '单词拼写(复习)' in game_title:          # 单词拼写游戏
                    if not word_spell_group[0]:
                        self.base_assert.except_error('单词拼写分组为0， 不应出现单词拼写戏')
                    SpellingWord().recite_word_spell_operate(stu_id, word_spell_group[x], recite_new_explains, only_apply_explains)
                    if self.wait_check_game_title_page():
                        if '单词拼写(复习)' in self.public.game_title().text:
                            self.base_assert.except_error('单词拼写（复习）个数与计算个数不一致')
                            break
                else:
                    break

        return len(recite_b_words) + len(recite_cde_vocab_apply_words)