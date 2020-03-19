#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/18 15:45
# -----------------------------------------
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from conf.decorator import teststep


class FlashCardProcess(FlashCard):

    @teststep
    def flash_card_operate(self, word_info):
        """闪卡操作流程"""
        index = 0
        star_words = []
        familiar_words = {}

        while '闪卡练习(新词)' in self.game_title().text:
            if index == 0:
                print('===== 🌟🌟 闪卡练习 学习模式 🌟🌟 =====\n')
            word = self.english_study()

            if self.wait_check_explain_page():
                explain = self.study_word_explain()  # 解释
                explain_id = explain.get_attribute('contentDescription')  # 解释id
                if word in list(word_info.keys()):
                    print('❌❌❌ 单词未去重')
                else:
                    word_info[word] = explain.text

                print('单词：', word, '\n',
                      '解释：', explain.text, '\n',
                      '句子：', self.study_sentence_explain(), '\n',
                      '句子解释：', self.study_sentence_explain(), '\n',
                      '推荐老师：', self.author(), '\n'
                      )
                self.pattern_switch()  # 切换到 全英模式
                if self.wait_check_explain_page():  # 校验是否成功切换
                    print('❌❌❌ 切换全英模式， 依然存在解释')

                self.pattern_switch()  # 切换回 英汉模式

                if index in [0, 2, 3, 4]:
                    if index == 0:
                        self.familiar_button().click()
                        self.tips_operate()
                        if self.familiar_button().text != '取消熟词':
                            print('❌❌❌ 点击熟词后内容未发生变化')
                        self.familiar_button().click()
                        if self.familiar_button().text != '设置熟词':
                            print('❌❌❌ 点击熟词后内容未发生变化')
                    self.familiar_button().click()
                    familiar_words[explain_id] = word

                if index in [0, 1]:
                    if index == 0:
                        self.star_button().click()  # 标星
                        self.tips_operate()
                        if self.star_button().get_attribute('selected') != 'true':
                            print('❌❌❌ 点击标星按钮后，按钮未点亮')
                        self.star_button().click()
                        if self.star_button().get_attribute('selected') != 'false':
                            print('❌❌❌ 取消标星后，按钮未置灰')
                    self.star_button().click()  # 标星
                    star_words.append(explain_id)
            else:
                print('❌❌❌ 默认不为英汉模式')

            self.next_btn_operate('true', self.fab_next_btn)
            index += 1
            print('-' * 30, '\n')

        return star_words, familiar_words

