#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/18 16:19
# -----------------------------------------
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.games.listen_spell_page import ListenSpellWordPage
from app.honor.student.word_book_rebuild.object_page.games.restore_word_page import WordRestore
from app.honor.student.word_book_rebuild.object_page.games.vocabulary_choose_page import VocabularyChoose
from app.honor.student.word_book_rebuild.object_page.games.word_match_page import MatchingWord
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.decorator import teststep


class GameOperate(WordBookRebuildPage):


    @teststep
    def new_word_other_game_operate(self, flash_result, word_info, stu_id):

        star_words = flash_result[0]
        familiar_words = flash_result[1]
        bank_count = flash_result[2] - len(familiar_words)

        while self.wait_check_game_title_page():
            title_ele = self.public.game_title()
            game_title = title_ele.text
            mode_id = int(title_ele.get_attribute('contentDescription').split('  ')[1])

            if '闪卡练习' in game_title and mode_id == 2:
                copy_count = FlashCard().flash_copy_model(star_words, new_explain_words=[])
                if self.wait_check_game_title_page():
                    if copy_count != len(star_words):
                        print('❌❌❌ 标星个数与抄写个数不一致')
                        break

            elif '单词拼写(新词)' in game_title:
                SpellingWord().new_word_spell_operate(familiar_words, new_explain_words=[])
                if self.wait_check_game_title_page():
                    if '单词拼写(新词)' in self.public.game_title().text:
                        print('❌❌❌ 标熟单词与单词拼写个数不一致')
                        break

            elif '词汇选择(新词)' in game_title:
                VocabularyChoose().normal_listen_select_operate(bank_count, new_explain_words=[])

            elif '连连看' in game_title:
                MatchingWord().link_link_game_operate(bank_count, word_info)

            elif '还原单词' in game_title:
                WordRestore().restore_word_operate(stu_id, bank_count, new_explain_words=[])

            elif '单词听写' in game_title:
                ListenSpellWordPage().normal_listen_spell_operate(bank_count, new_explain_words=[])
            else:
                break

