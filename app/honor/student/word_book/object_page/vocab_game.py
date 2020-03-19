#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/26 17:18
# -----------------------------------------
import time

from app.honor.student.word_book_rebuild.object_page.games.vocabulary_choose_page import VocabularyChoose
from conf.decorator import teststep


class VocabGamePage(VocabularyChoose):

    @teststep
    def select_explain_by_word(self, index, wrong_again_words, game_type):
        """根据解释选单词"""
        if '词汇选择(复习)' not in game_type[-2]:
            print('====== 🌟🌟 词汇选择 - 根据单词选解释模式（复习）🌟🌟 =====\n')
        self.next_btn_operate('false', self.fab_next_btn)  # 下一题 按钮 判断加 点击操作
        word = self.question_content()  # 题目
        print('题目:', word.text)

        explain_id = word.get_attribute('contentDescription')  # 获取正确解释id
        right_explain = self.data.get_explain_by_id(explain_id)  # 根据id获取正确解释文本
        options = self.option_button()  # 遍历选项，点击和正确答案一样的解释
        for y in options:
            if index in [2, 3]:  # 次序为【2,3】连续选择错误
                if right_explain not in y.text:
                    if index == 2:
                        wrong_again_words.append(explain_id)
                    print('选择错误答案：', y.text)
                    print('正确答案为:', right_explain)
                    y.click()
                    break
            elif right_explain in y.text:
                print('选择答案：', y.text)
                y.click()
                break

        print('正确答案：', right_explain)
        self.next_btn_operate('true', self.fab_next_btn)  # 下一题 按钮 状态判断 加点击
        print('-' * 30, '\n')
        index += 1
        return index


    @teststep
    def select_word_by_explain(self, stu_id, index, wrong_again_words, game_type):
        """根据解释选单词"""
        if '词汇选择(复习)' not in game_type[-2]:
            print('===== 🌟🌟 词汇选择-根据解释选单词模式（复习）🌟🌟 =====\n')
        self.next_btn_judge('false', self.fab_next_btn)  # 下一题 按钮 判断加 点击操作
        item = self.question_content()  # 题目
        print('题目:', item.text)
        explain_id = item.get_attribute('contentDescription')
        right_word = self.data.get_word_by_explain_id(stu_id, explain_id)  # 根据解释id获取正确单词
        options = self.option_button()  # 遍历选项，点击和word一样的单词
        for y in options:
            if index in [2, 3]:  # 次序为【2,3】连续选择错误
                if y.text != right_word:
                    if index == 2:
                        wrong_again_words.append(explain_id)
                    print('选择错误答案：', y.text)
                    print('正确答案为:', right_word)
                    y.click()
                    break
            elif y.text == right_word:
                print('选择答案：', y.text)
                y.click()
                break
        self.next_btn_operate('true', self.fab_next_btn)  # 下一题 按钮 状态判断 加点击
        index += 1
        print('-' * 30, '\n')
        return index

    @teststep
    def vocab_apply_game_operate(self, stu_id, index, game_type):
        """词汇运用游戏"""
        if '词汇运用(复习)' not in game_type[-2]:
            print('===== 🌟🌟 词汇运用 --句子选单词模式(复习) 🌟🌟 =====\n')
        self.next_btn_judge('false', self.fab_next_btn)
        item = self.question_content()  # 题目
        print('题目：%s' % item.text)
        explain_id = item.get_attribute('contentDescription')                # 根据题目获取explain——id
        right_answer = self.data.get_word_by_explain_id(stu_id, explain_id)  # 根据解释id获取正确单词
        self.click_hint_button()  # 点击提示按钮
        self.hint_button_judge('false')  # 提示按钮 状态判断
        if not self.wait_vocab_apply_explain_page():
            print('❌❌❌ 点击提示后未发现句子解释文本')
        else:
            sentence_explain = self.sentence_explain()
            print('句子解释：', sentence_explain)

        for y in self.option_button():
            if y.text == right_answer:
                print('选择答案：', y.text)
                y.click()
                time.sleep(1)
                break
        self.next_btn_operate('true', self.fab_next_btn)  # 下一题 按钮 状态判断 加点击
        index += 1
        print('-' * 30, '\n')
        return index