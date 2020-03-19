import time

from app.honor.student.games.word_spell import SpellWordGame
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class SpellingWord(SpellWordGame):
    """单词拼写"""
    def __init__(self):
        super().__init__()
        self.data = WordDataHandlePage()
        self.key = Keyboard()
        self.word_public = WorldBookPublicPage()


    @teststep
    def spell_right_word_operate(self, word):
        """单词拼写做对操作"""
        self.hint_ele_operate(word)
        self.key.games_keyboard('backspace')
        print('单词:', word)
        for j in range(0, len(word)):
            self.keyboard_operate(j, word[j])  # 点击键盘 具体操作


    @teststeps
    def new_word_spell_operate(self, familiar_word, new_explain_words):
        """单词拼写 - 《默写模式》游戏过程"""
        print('===== 🌟🌟 单词拼写 新词 🌟🌟 ======\n')
        print('标熟单词：', familiar_word, '\n')
        all_words = []
        value = 0
        index = 0
        while self.wait_check_normal_spell_page():
            explain_ele = self.word_explain()        # 解释
            explain = explain_ele.text
            explain_id = self.word_public.get_explain_id(explain_ele)
            self.next_btn_judge('false', self.fab_commit_btn)  # 下一题 按钮 状态判断

            if explain_id in new_explain_words:
                if '新释义' not in self.game_title().text:
                    print('❌❌❌ 该单词为新释义，但是标题没有显示新释义字样')

            print('解释：', explain)
            if explain in all_words:
                print('❌❌❌ 该单词在拼写单词中已经出现过！')
            else:
                all_words.append(explain)

            if explain_id not in list(familiar_word.keys()):
                print('❌❌❌ 单词未标熟，但是出现拼写', explain)
            else:
                value = familiar_word[explain_id]
                self.spell_right_word_operate(value)

            self.next_btn_operate('true', self.fab_commit_btn)         # 下一题 按钮 状态判断 加点击
            answer = self.spell_word().text[::2]  # 最终答案
            if answer != value.lower():
                print('❌❌❌ 大写字母未自动变为小写字母')
            # self.result_operate(answer, self.mine_answer())   # 下一步按钮后的答案页面 测试
            self.click_voice()
            self.next_btn_operate('true', self.fab_next_btn)
            time.sleep(2)
            index += 1
            print('-'*30, '\n')
        return index


    @teststeps
    def recite_word_spell_operate(self, stu_id, bank_count, recite_new_explain_words, only_apply_explains):
        """单词拼写 复习"""
        print('===== 🌟🌟 单词默写 复习 🌟🌟 ===== \n')
        for x in range(bank_count):
            explain = self.word_explain()  # 解释
            print('解释：', explain.text)
            explain_id = explain.get_attribute('contentDescription')
            if explain_id in recite_new_explain_words:
                print('❌❌❌ 此单词为新释义单词，不应出现单词拼写游戏')

            if explain_id in only_apply_explains:
                print('❌❌❌ 此单词为只有词汇运用单词， 不应出现在单词拼写中')

            self.next_btn_judge('false', self.fab_commit_btn)  # 下一题 按钮 状态判断
            right_word = self.data.get_word_by_explain_id(stu_id, explain_id)
            self.spell_right_word_operate(right_word)
            self.next_btn_operate('true', self.fab_commit_btn)
            print('我输入的：', right_word)

            if not self.wait_check_play_voice_page():
                print('❌❌❌ 点击提交按钮后未发现喇叭按钮')
            self.next_btn_operate('true', self.fab_next_btn)
            print('-'*30, '\n')


    # @teststeps
    # def dictation_pattern_mine(self, i, familiar_add, spell_word):
    #     """单词默写 我的单词"""
    #     if i == 0:
    #         print("\n单词拼写 - 默写模式(单词详情)\n")
    #     explain = self.word_explain()  # 题目
    #     value = self.data.get_word_by_explain(explain)
    #     familiars = self.data.get_familiar_words() + familiar_add
    #     intersect_list = list(set(value).intersection(set(familiars)))  # 取获取单词数组与标星单词数组的交集
    #     if i in range(0, 5):
    #         self.dictation_pattern_core(spell_word, word_type=1)
    #         if len(intersect_list) == 0:
    #             print('❌❌❌ Error-- 单词未被标熟却出现默写模式')
    #     else:
    #         FlashCard().tips_operate()
    #         for i in familiar_add:
    #             level = self.data.get_word_level(i)
    #             if level < 3:
    #                 print("❌❌❌ Error--提交未成功，单词熟练度未更改")

    @teststeps
    def hint_ele_operate(self, value):
        self.next_btn_judge('false', self.fab_commit_btn)  # 下一题 按钮 判断加 点击操作
        if self.wait_check_tv_word_or_random_page():  # 默写模式 - 字母未全部消除
            print('❌❌❌ Error - 单词拼写 默写模式 - 字母未全部消除')

        hint = self.hint_btn()  # 提示按钮
        if GetAttribute().get_enabled(hint) == 'true':
            hint.click()  # 点击 提示按钮
            if GetAttribute().get_enabled(self.hint_btn()) != 'false':
                print('❌❌❌ Error - 点击后提示按钮enabled属性错误')

            if self.wait_check_tv_word_or_random_page():  # 出现首字母提示
                first_word = self.spell_word().text[::2]
                if first_word == value[0]:
                    print('点击提示出现首字母提示', first_word)
                else:
                    print('点击提示出现首字母提示', first_word)
            else:
                print("❌❌❌ Error - 首字母提示未出现")
        else:
            print('❌❌❌ Error - 提示按钮enabled属性错误')

    @teststeps
    def result_operate(self, answer, mine):
        """下一步按钮后的答案页面"""
        print('我的答案:', answer)
        print('去除大小写结果:', mine)
        if self.wait_check_right_answer_page():
            correct = self.right_answer_word()  # 正确答案
            print('填写错误，正确答案:', correct)
            if len(mine) <= len(correct):  # 输入少于或等于单词字母数的字符
                if mine.lower() != answer.lower():  # 展示的 我的答题结果 是否与我填入的一致
                    print('❌❌❌ Error - 字符数少于或等于时:', mine.lower(), answer.lower())
            else:  # 输入过多的字符
                if correct + mine[len(correct):].lower() != correct + answer[len(correct):].lower():
                    # 展示的 我的答题结果 是否与我填入的一致
                    print('❌❌❌ Error - 字符输入过多时:', correct + mine[len(correct):].lower(), correct + answer[len(
                        correct):].lower())
        else:  # 回答正确
            if mine.lower() != answer.lower():  # 展示的 我的答题结果 是否与我填入的一致
                print('❌❌❌ Error - 展示的答题结果 与我填入的不一致:', mine.lower(), answer.lower())
            else:
                print('回答正确!')
        print('-'*30, '\n')

    @teststeps
    def keyboard_operate(self, j, value):
        """点击键盘 具体操作"""
        if j == 4:
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.key.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.key.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.key.games_keyboard(value)  # 点击键盘对应字母

    @teststeps
    def dictation_random_pattern_recite(self, stu_id, wrong_words):
        """错题再练 单词拼写 随机模式"""
        for x in range(len(wrong_words)):
            self.next_btn_judge('false', self.fab_commit_btn)
            explain = self.word_explain()
            print('解释：', explain.text)
            explain_id = explain.get_attribute('contentDescription')
            word = self.data.get_word_by_explain_id(stu_id, explain_id)
            print("正确单词：", word)
            tip_word = self.spell_word().text[1::2]
            print('提示词：', tip_word)

            right_word = [x for x in word if len(x) == len(tip_word)]
            alphas = [right_word[0][x] for x in range(len(right_word[0])) if tip_word[x] == '_']
            print(alphas)
            for k in range(len(alphas)):
                self.keyboard_operate(k, alphas[k])  # 点击键盘 具体操作
            print('填充后单词为：', self.spell_word().text[1::2])
            self.next_btn_operate('true', self.fab_commit_btn)
            if self.wait_check_play_voice_page():
                self.sound_icon().click()
            else:
                print('❌❌❌ 未发现声音按钮')
            self.next_btn_operate('true', self.fab_next_btn)  # 下一题 按钮 判断加 点击操作
            time.sleep(2)





