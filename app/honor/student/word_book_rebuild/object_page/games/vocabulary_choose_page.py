import random
import time

from app.honor.student.games.choice_vocab import VocabChoiceGame
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from conf.decorator import teststeps


class VocabularyChoose(VocabChoiceGame):
    """词汇选择"""
    def __init__(self):
        self.data = WordDataHandlePage()

    @teststeps
    def normal_listen_select_operate(self, bank_count, new_explain_words):
        """《词汇选择》 - 听音选词模式 具体操作"""
        print('===== 🌟🌟 词汇选择(新词) 听音选词模式(第一遍选错，第二遍选择正确) 🌟🌟=====\n')
        print('题目个数：', bank_count)
        answer_word, all_words = [], []

        while len(all_words) < bank_count:
            self.next_btn_judge('false', self.fab_next_btn)
            self.listen_choice_speak_icon().click()  # 点击发音按钮
            options = self.vocab_options()  # 获取当前页面所有选项
            if not answer_word:  # 正确答案列表为空
                opt_index = random.randint(0, len(options) - 1)  # 随机选择一个选项
                opt_text = options[opt_index].text
                options[opt_index].click()
                self.next_btn_judge('true', self.fab_next_btn)  # 检查下一步按钮的状态

                print('选择答案为：', opt_text)
                if self.wait_check_explain_page():  # 检验是否出现解释页面
                    explain = self.vocab_word_explain()
                    explain_id = explain.get_attribute('contentDescription')

                    if explain_id in new_explain_words:
                        self.base_assert.except_error('此单词为新释义，不应出现词汇选择游戏')
                    print('解释:', explain.text)
                else:
                    self.base_assert.except_error('解释文本未出现')

                right_answer = self.vocab_right_answer()  # 正确答案
                if right_answer == opt_text:
                    print('选择正确')
                    all_words.append(right_answer)
                else:
                    print('选择错误，正确答案为', right_answer)
                    answer_word.append(right_answer)
            else:  # 正确答案列表不为空-- 上一题选择错误
                for y in options:
                    if y.text == answer_word[0]:  # 点击正确答案
                        y.click()
                        self.next_btn_judge('true', self.fab_next_btn)  # 检查下一步按钮的状态
                        if self.wait_check_explain_page():
                            explain = self.vocab_word_explain()
                            explain_id = explain.get_attribute('contentDescription')
                            if explain_id in new_explain_words:
                                self.base_assert.except_error('此单词为新释义，不应出现词汇选择游戏')
                            all_words.append(y.text)
                            print('答案正确：%s' % answer_word[0])
                            print('解释：%s' % explain.text)
                        else:
                            self.base_assert.except_error('Error-- 解释文本未出现')
                        break
                answer_word.clear()
            self.sound_icon().click()
            self.fab_next_btn().click()   # 下一题 按钮 状态判断 加点击
            time.sleep(2)
            print('-' * 30, '\n')

    @teststeps
    def right_listen_select_operate(self, stu_id, bank_count, new_explain_words):
        print('===== 🌟🌟 词汇选择(新词) 听音选词模式(一次做对模式) 🌟🌟 =====\n')
        for x in range(bank_count):
            self.next_btn_judge("false", self.fab_next_btn)  # 下一题 按钮 状态判断 加点击
            voice_btn = self.listen_choice_speak_icon()
            explain_id = voice_btn.get_attribute('contentDescription')
            if explain_id in new_explain_words:
                self.base_assert.except_error('此单词为新释义，不应出现词汇选择游戏')
            right_word = self.data.get_word_by_explain_id(stu_id, explain_id)
            for y in self.vocab_options():
                if y.text == right_word:
                    print('选择选项：', y.text)
                    y.click()
                    if not self.wait_check_explain_page():
                        self.base_assert.except_error('点击选项未出现解释文本！')
                    else:
                        print("解释：", self.vocab_word_explain().text)
                    break
            self.sound_icon().click()
            self.fab_next_btn().click()   # 下一题 按钮 状态判断 加点击
            time.sleep(2)
            print('-' * 30, '\n')


    @teststeps
    def vocab_select_choice_explain(self, bank_count, wrong_again_words):
        """《词汇选择》 - 选解释模式
        :param bank_count: 题目个数
        :param wrong_again_words: 错题再练单词
        """
        print('====== 🌟🌟 词汇选择 - 根据单词选解释模式（复习）🌟🌟 =====\n')
        recite_words = []
        for x in range(bank_count + 2):
            self.next_btn_operate('false', self.fab_next_btn)  # 下一题 按钮 判断加 点击操作
            self.sound_icon().click()  # 点击发音按钮
            word = self.vocab_question()  # 题目
            print('题目:', word.text)

            explain_id = word.get_attribute('contentDescription')     # 获取正确解释id

            if explain_id in recite_words:
                self.base_assert.except_error('单词已选过， 再次出现')

            right_explain = self.data.get_explain_by_id(explain_id)      # 根据id获取正确解释文本
            options = self.vocab_options()      # 遍历选项，点击和正确答案一样的解释
            for y in options:
                if x in [2, 3]:                 # 次序为【2,3】连续选择错误
                    if right_explain not in y.text:
                        if x == 2:
                            wrong_again_words.append(explain_id)
                        print('选择错误答案：', y.text)
                        print('正确答案为:', right_explain)
                        y.click()
                        break
                elif right_explain in y.text:
                    print('选择答案：', y.text)
                    recite_words.append(explain_id)
                    y.click()
                    break

            print('正确答案：', right_explain)
            self.fab_next_btn().click()  # 下一题 按钮 状态判断 加点击
            time.sleep(2)
            print('-'*30, '\n')

    @teststeps
    def vocab_select_choice_word(self, stu_id, bank_count, wrong_again_words):
        """《词汇选择》 - 根据解释选单词"""
        recite_words = []
        print('===== 🌟🌟 词汇选择-选单词模式（复习）🌟🌟 =====\n')
        for x in range(bank_count + 2):
            self.next_btn_judge('false', self.fab_next_btn)  # 下一题 按钮 判断加 点击操作
            item = self.vocab_question()  # 题目
            print('题目:', item.text)
            explain_id = item.get_attribute('contentDescription')

            if explain_id in recite_words:
                self.base_assert.except_error('单词已选过， 再次出现')

            right_word = self.data.get_word_by_explain_id(stu_id, explain_id)   # 根据解释id获取正确单词
            options = self.vocab_options()  # 遍历选项，点击和word一样的单词
            for y in options:
                if x in [2, 3]:                 # 次序为【2,3】连续选择错误
                    if y.text != right_word:
                        if x == 2:
                            wrong_again_words.append(explain_id)
                        print('选择错误答案：', y.text)
                        print('正确答案为:', right_word)
                        y.click()
                        break
                elif y.text == right_word:
                    print('选择答案：', y.text)
                    recite_words.append(explain_id)
                    y.click()
                    break
            if self.wait_check_voice_page():
                self.sound_icon().click()
            else:
                self.base_assert.except_error(' Error-- 声音按钮未出现')
            self.fab_next_btn().click()  # 下一题 按钮 状态判断 加点击
            time.sleep(2)
            print('-'*30, '\n')

    @teststeps
    def vocab_apply(self, stu_id,  bank_count, right_words, recite_new_explain_words):
        """词汇运用"""
        print('===== 🌟🌟 词汇运用 --句子选单词模式(复习) 🌟🌟 =====\n')
        recite_words = []
        for x in range(bank_count):
            self.next_btn_judge('false', self.fab_next_btn)
            item = self.vocab_question()  # 题目
            print('题目：%s' % item.text)
            explain_id = item.get_attribute('contentDescription')           # 根据题目获取explain——id
            if explain_id in recite_words:
                self.base_assert.except_error('单词已复习过， 单词未去重!')

            if explain_id in right_words and explain_id not in recite_new_explain_words:
                self.base_assert.except_error('单词新词时做全对， 复习时不为新释义单词， 不应出现词汇运用游戏')

            right_answer = self.data.get_word_by_explain_id(stu_id, explain_id)     # 根据解释id获取正确单词
            self.apply_hint_button().click()  # 点击提示按钮
            self.next_btn_judge('false', self.apply_hint_button)  # 提示按钮 状态判断
            if not self.wait_vocab_apply_explain_page():
                self.base_assert.except_error('点击提示后未发现句子解释文本')
            else:
                sentence_explain = self.apply_sentence_explain()
                self.base_assert.except_error('句子解释：' + sentence_explain)

            for y in self.vocab_options():
                if y.text == right_answer:
                    recite_words.append(explain_id)
                    print('选择答案：', y.text)
                    y.click()
                    break

            if self.wait_check_voice_page():
                self.sound_icon().click()
            else:
                self.base_assert.except_error('Error-- 声音按钮未出现')
            self.fab_next_btn().click()   # 下一题 按钮 状态判断 加点击
            time.sleep(2)
            print('-'*30, '\n')



