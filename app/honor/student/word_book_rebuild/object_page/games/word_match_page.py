
import time
from app.honor.student.games.word_match_new import LinkWordGame
from conf.decorator import teststeps



class MatchingWord(LinkWordGame):
    """连连看"""
    @teststeps
    def link_link_game_operate(self, bank_count, group_word_answers):
        """连连看游戏过程"""
        print('====== 🌟🌟 连连看  新词 🌟🌟======= \n')
        print('本组单词信息：', group_word_answers)
        tips = []
        while self.wait_check_word_match_page():
            hans_card_list = self.get_ch_or_en_cards(text_mode=True, hans=True)
            english_card_list = self.get_ch_or_en_cards(text_mode=True, hans=False)
            if len(hans_card_list) != 0:
                hans_card = hans_card_list[0]
                hans_text = hans_card.text
                for en in english_card_list:
                    english_word = en.text
                    hans_card.click()
                    en.click()
                    time.sleep(3)
                    if self.wait_check_word_match_page():
                        if len(self.get_ch_or_en_cards(text_mode=True, hans=True)) < len(hans_card_list):
                            tips.append(hans_text)
                            print('单词解释：', hans_text)
                            print('英文：', english_word)
                            break
                    else:
                        print('单词解释：', hans_text)
                        print('英文：', english_word)
                        tips.append(hans_text)
                        break
        if len(tips) != bank_count:
            self.base_assert.except_error('❌❌❌  连连看个数与计算个数不一致， 应为{}题， 实际为{}题'.format(bank_count, len(tips)))

        time.sleep(3)

