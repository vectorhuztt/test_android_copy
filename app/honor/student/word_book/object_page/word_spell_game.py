#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/26 17:14
# -----------------------------------------
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord


class WordSpellGamePage(SpellingWord):

    def word_spell_game_operate(self, stu_id, index, game_type):
        """单词拼写游戏"""
        if '单词拼写(复习)' not in game_type[-2]:
            print('===== 🌟🌟 单词默写 复习 🌟🌟 ===== \n')
        explain = self.word_explain()  # 解释
        print('解释：', explain.text)
        explain_id = explain.get_attribute('contentDescription')
        self.next_btn_judge('false', self.fab_commit_btn)  # 下一题 按钮 状态判断
        right_word = self.data.get_word_by_explain_id(stu_id, explain_id)
        self.spell_right_word_operate(right_word)
        self.next_btn_operate('true', self.fab_commit_btn)

        print('我输入的：', right_word)
        if not self.wait_check_play_voice_page():
            print('❌❌❌ 点击提交按钮后未发现喇叭按钮')
        self.next_btn_operate('true', self.fab_next_btn)
        index += 1
        print('-' * 30, '\n')
        return index

