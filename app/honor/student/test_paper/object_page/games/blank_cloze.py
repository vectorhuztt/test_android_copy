import random
import re
import string
import time
from app.honor.student.games.article_select_blank import SelectBlankGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps
from utils.games_keyboard import Keyboard


class BlankCloze(SelectBlankGame):
    """选词填空"""

    @teststeps
    def play_bank_cloze_game(self, num, exam_json):
        """选词填空 答卷过程 """
        exam_json['选词填空'] = bank_json = {}
        article = self.rich_text()  # 获取文章
        print(article.text)
        self.hint_btn().click()
        if self.wait_check_hint_content_page():
            print("提示词：", self.hint_answer())
            HomePage().click_blank()
        for i in range(num):   # 其他点击回车键顺序填空，填空的文本为26个字母随机填写3-6个
            input_answer = self.select_blank_play_process()
            print('我输入的：', input_answer)
            bank_json[i] = input_answer
            AnswerPage().skip_operator(i, num, '选词填空', self.wait_check_select_blank_page,
                                       self.judge_tip_status, input_answer.lower())

    @teststeps
    def judge_tip_status(self, input_word):
        desc = self.rich_text().get_attribute('contentDescription')
        if input_word in desc.split('## ')[1].split():
            print('跳转后填空内容未发生变化')
        else:
            self.base_assert.except_error('Error-- 跳转回来填空内容发生改变')



