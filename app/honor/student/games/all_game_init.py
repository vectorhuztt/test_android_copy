#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/11/11 13:44
# -----------------------------------------
from app.honor.student.games.article_cloze import ClozeGame
from app.honor.student.games.article_complete import CompleteArticleGame
from app.honor.student.games.article_read_understand import ReadUnderstandGame
from app.honor.student.games.article_select_blank import SelectBlankGame
from app.honor.student.games.choice_images import ListenSelectImageGame
from app.honor.student.games.choice_listen import ListenChoiceGame
from app.honor.student.games.choice_single import SingleChoiceGame
from app.honor.student.games.choice_vocab import VocabChoiceGame
from app.honor.student.games.grind_ear import GrindingEarGame
from app.honor.student.games.sentence_change import SentenceChangeGame
from app.honor.student.games.sentence_link import SentenceLinkGame
from app.honor.student.games.sentence_listen_link import ListenLinkSentenceGame
from app.honor.student.games.sentence_strengthen import SentenceStrengthenGame
from app.honor.student.games.word_flash_card import FlashCardGame
from app.honor.student.games.word_guess import GuessWordGame
from app.honor.student.games.word_listen_spell import ListenSpellGame
from app.honor.student.games.word_match_new import LinkWordGame
from app.honor.student.games.word_restore import RestoreWordGame
from app.honor.student.games.word_speak import WordSpeakGame
from app.honor.student.games.word_spell import SpellWordGame


class AllGameClass:

    def __init__(self):
        self.word_spell = SpellWordGame()
        self.word_restore = RestoreWordGame()
        self.word_match = LinkWordGame()
        self.word_speak = WordSpeakGame()
        self.listen_spell = ListenSpellGame()
        self.word_guess = GuessWordGame()
        self.word_flash = FlashCardGame()
        self.sentence_strengthen = SentenceStrengthenGame()
        self.sentence_listen_link = ListenLinkSentenceGame()
        self.sentence_link = SentenceLinkGame()
        self.sentence_change = SentenceChangeGame()
        self.vocab_choice = VocabChoiceGame()
        self.single_choice = SingleChoiceGame()
        self.listen_choice = ListenChoiceGame()
        self.image_choice = ListenSelectImageGame()
        self.select_blank = SelectBlankGame()
        self.read_understand = ReadUnderstandGame()
        self.complete_article = CompleteArticleGame()
        self.cloze = ClozeGame()
        self.grind_ear = GrindingEarGame()