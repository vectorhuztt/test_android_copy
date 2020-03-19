#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/26 13:34
# -----------------------------------------
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from app.honor.student.word_book.object_page.vocab_game import VocabGamePage
from app.honor.student.word_book.object_page.word_spell_game import WordSpellGamePage
from conf.decorator import teststep


class ReciteWordPage(WordBookRebuildPage):
    @teststep
    def word_book_recite_operate(self, stu_id, wrong_again_words):
        """单词复习操作"""
        vocab_select_index, vocab_apply_index, word_spell_index = 0, 0, 0
        game_type = [' ']
        while self.wait_check_game_title_page():
            title_ele = self.public.game_title()
            game_title = title_ele.text
            game_type.append(game_title)
            mode_id = int(title_ele.get_attribute('contentDescription').split('  ')[1])

            if '词汇选择(复习)' in game_title:
                if mode_id == 2:  # mode=2 , 根据解释选单词
                    vocab_select_index = VocabGamePage().select_word_by_explain(stu_id, vocab_select_index, wrong_again_words, game_type)
                else:            # mode=1， 根据单词选解释
                    vocab_select_index = VocabGamePage().select_explain_by_word(vocab_select_index, wrong_again_words, game_type)

            elif '词汇运用(复习)' in game_title:
                vocab_apply_index = VocabGamePage().vocab_apply_game_operate(stu_id, vocab_apply_index, game_type)  # 词汇运用游戏过程

            elif '单词拼写(复习)' in game_title:  # 单词拼写游戏
                word_spell_index = WordSpellGamePage().word_spell_game_operate(stu_id, word_spell_index, game_type)

            else:
                break
        return word_spell_index