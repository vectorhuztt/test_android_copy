#!/usr/bin/env python
# code:UTF-8
import random
import string
import time

from app.honor.student.games.word_listen_spell import ListenSpellGame
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard


class ListenSpellWordPage(ListenSpellGame):
    """单词听写"""
    def __init__(self):
        self.key = Keyboard()
        self.word_public = WorldBookPublicPage()

    @teststep
    def right_listen_spell_operate(self, stu_id, bank_count, new_explain_words):
        """单词听写做对操作"""
        print('===== 🌟🌟 单词听写模式(新词)(一次做对) 🌟🌟 =====\n')
        for x in range(bank_count):
            self.next_btn_judge('false', self.fab_commit_btn)  # 下一题 按钮 判断加 点击操作
            explain_id = self.word_public.get_explain_id(self.input_wrap_side())
            right_answer = WordDataHandlePage().get_word_by_explain_id(stu_id, explain_id)
            for alpha in list(right_answer):
                self.key.games_keyboard(alpha)  # 输入单词的大写字母

            self.next_btn_operate('true', self.fab_commit_btn)  # 下一题 按钮 判断加 点击操作
            explain = self.word_explain()
            if explain_id in new_explain_words:
                print('❌❌❌ 此单词为新释义，不应出现单词听写游戏')
            print('解释：', explain.text)
            print('我输入的：', right_answer)
            self.next_btn_operate('true', self.fab_next_btn)  # 下一题
            time.sleep(2)
            print('-' * 30, '\n')
        time.sleep(5)
    
    @teststeps
    def normal_listen_spell_operate(self, bank_count, new_explain_words):
        """《单词听写》 正常游戏过程"""
        print('===== 🌟🌟 单词听写模式(新词)(输错一次，输对一次) 🌟🌟 =====\n')
        answer_word = []
        for x in range(bank_count*2):
            if self.wait_check_listen_spell_word_page():
                self.click_voice()  # 点击播放按钮
                self.next_btn_judge('false', self.fab_commit_btn)  # 下一题 按钮 判断加 点击操作
                explain_id = self.word_public.get_explain_id(self.input_wrap_side())
                if explain_id in new_explain_words:
                    print('❌❌❌ 此单词为新释义，不应出现单词听写游戏')

                if not answer_word:    # 数组为空，说明上一题已回答正确，本题需随机填入字母以获取正确答案
                    self.key.games_keyboard(random.choice(string.ascii_lowercase))  # 随机输入一个小写字母
                    mine_input = self.input_word()  # 输入的答案
                    self.next_btn_operate('true', self.fab_commit_btn)
                    if self.wait_check_answer_word_page():  # 判断正确答案是否存在
                        correct_ans = self.right_answer()  # 获取正确答案
                        answer_word.append(correct_ans)
                        explain = self.word_explain()
                        print('解释：', explain.text)
                        print('我输入的答案：', mine_input)
                        print('正确答案为:', correct_ans)
                    else:
                        print("❌❌❌ Error - 未显示正确答案")

                else:   # 数组长度为1，说明已获取正确答案，直接输入正确答案即可
                    for alpha in list(answer_word[0]):
                        self.key.games_keyboard(alpha.upper())   # 输入单词的大写字母

                    print('我输入的单词：', answer_word[0].upper())
                    self.next_btn_operate('true', self.fab_commit_btn)      # 提交 判断加 点击操作
                    if self.input_word() != answer_word[0].lower():
                        print('❌❌❌ 输入单词大写后，点击确定，单词未变为小写字母')

                    if self.wait_check_answer_word_page():  # 判断正确答案是否出现
                        print("❌❌❌ Error -听写正确却显示正确答案")
                    explain = self.word_explain()
                    print('解释：', explain.text)
                    print('回答正确！')
                    answer_word.clear()
                self.next_btn_operate('true', self.fab_next_btn)  # 下一题
                time.sleep(2)
                print('-'*30, '\n')
        time.sleep(5)


