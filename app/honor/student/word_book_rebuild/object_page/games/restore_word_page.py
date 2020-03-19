import time
from app.honor.student.games.word_restore import RestoreWordGame
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from conf.decorator import teststeps, teststep


class WordRestore(RestoreWordGame):
    """还原单词"""

    @teststep
    def right_restore_word_operate(self, stu_id,  bank_count, new_explain_words):
        print('===== 🌟🌟 还原单词模式(新词) (一次做对) 🌟🌟 =====\n')
        for x in range(bank_count):
            self.sound_icon().click()  # 听力按钮
            self.next_btn_judge('false', self.fab_commit_btn)
            explain = self.word_explain()  # 展示的提示词
            explain_id = explain.get_attribute('contentDescription')
            right_answer = WordDataHandlePage().get_word_by_explain_id(stu_id, explain_id)
            if explain_id in new_explain_words:
                print('❌❌❌ 此单词为新释义，不应出现还原游戏')
            print("解释：%s" % explain.text)
            print("还原前单词为：", ''.join([x.text for x in self.word()]))
            self.restore_word_core(right_answer)
            print('还原后单词：', right_answer)
            self.next_btn_operate('true', self.fab_next_btn)
            time.sleep(3)
            print('-'*30, '\n')

    @teststeps
    def restore_word_operate(self, stu_id, bank_count, new_explain_words):
        print('===== 还原单词模式(新词) (做一遍错一遍对)=====\n')
        all_words, answer_word = [], []
        while len(all_words) < bank_count:
            self.sound_icon().click()  # 听力按钮
            explain = self.word_explain()  # 展示的提示词
            explain_id = explain.get_attribute('contentDescription')
            right_word = WordDataHandlePage().get_word_by_explain_id(stu_id, explain_id)
            self.next_btn_judge('false', self.fab_commit_btn)

            if explain_id in new_explain_words:
                print('❌❌❌ 此单词为新释义，不应出现还原游戏')

            print("英文解释：%s" % explain.text)
            print("还原前单词为：", ''.join([x.text for x in self.word()]))

            if not answer_word:
                self.drag_operate(self.word()[-1], self.word()[0])
                after_word = ''.join([x.text for x in self.word()])
                print('还原后单词为：%s' % after_word)
                if after_word == right_word:
                    print('还原正确')
                    all_words.append(explain)
                    self.next_btn_operate('true', self.fab_next_btn)
                else:
                    self.next_btn_operate('true', self.fab_commit_btn)
                    if self.wait_restore_answer_word_page():
                        right_answer = self.word(index=1)[0].text
                        print('正确答案：', right_answer)
                        answer_word.append(right_answer)
                    else:
                        print('❌❌❌ 未发现正确答案')
                    self.fab_next_btn().click()
            else:
                self.restore_word_core(answer_word[0])
                if len(all_words) != bank_count - 1:
                    print('还原后单词为：%s' % ''.join([x.text for x in self.word()]))
                self.next_btn_operate('true', self.fab_next_btn)
                answer_word.clear()
                all_words.append(explain)
            time.sleep(4)
            print('-'*30, '\n')
        time.sleep(5)


    @teststep
    def restore_word_core(self, english):
        """还原单词主要步骤"""
        index = 0
        count = 0
        sort_word = ''
        while True:
            alphas = self.word()
            for x in range(count, len(alphas)):
                alpha_len = len(alphas[x].text)
                if index + alpha_len >= len(english) - 1:
                    english += ' ' * alpha_len
                word_part = ''.join([english[x] for x in range(index, index + alpha_len)])

                if alphas[x].text == word_part.strip():
                    if count != x:
                        self.drag_operate(alphas[x], alphas[count])
                        sort_word = ''.join([k.text for k in self.word()])
                    index += alpha_len
                    count += 1
                    break
            if english.strip() == sort_word:
                break
