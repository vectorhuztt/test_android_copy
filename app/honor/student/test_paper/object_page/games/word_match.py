
import time
from app.honor.student.games.word_match_new import LinkWordGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class WordMatch(LinkWordGame):

    @teststeps
    def play_word_match_game(self, num, exam_json):
        """连连看 """
        exam_json['连连看'] = bank_json = {}
        text_mode = False if self.is_image_text_mode() else True
        tips = []
        while len(tips) < num:
            hans_card_list = self.get_ch_or_en_cards(text_mode=text_mode, hans=True)
            english_card_list = self.get_ch_or_en_cards(text_mode=text_mode, hans=False)
            if len(hans_card_list) != 0:
                hans_card = hans_card_list[0]
                hans_text = hans_card.text
                for en in english_card_list:
                    english_word = en.text
                    hans_card.click()
                    en.click()
                    time.sleep(1)
                    if len(self.get_ch_or_en_cards(text_mode=text_mode, hans=True)) < len(hans_card_list):
                        tips.append(english_card_list)
                        bank_json[len(tips) - 1] = english_word
                        print('单词解释：', hans_text)
                        print('英文：', english_word)
                        break
                AnswerPage().skip_operator(len(tips) - 1, num, '连连看', self.wait_check_word_match_page, self.judge_tip_status, hans_text)
            else:
                self.screen_swipe_left(0.9, 0.5, 0.2, 1000)
        print('本次做题答案：', bank_json)

    @teststep
    def judge_tip_status(self, opt_text):
        img_select_status = self.get_img_status_by_text(opt_text)
        if img_select_status != 'true':
            self.base_assert.except_error('Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')
