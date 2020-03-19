import re
from app.honor.student.games.article_complete import CompleteArticleGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststep, teststeps


class CompleteText(CompleteArticleGame):

    @teststeps
    def play_complete_article_game(self, num, exam_json):
        """补全文章 答卷过程"""
        exam_json['补全文章'] = bank_json = {}
        if self.wait_check_complete_article_page():
            article = self.rich_text()
            print(article.text)
            self.drag_up_down(drag_down=False)
            for i in range(num):  # 依次点击选项
                if self.wait_check_complete_article_page():
                    select_text = self.opt_options()[i].text
                    self.opt_char()[i].click()
                    print("选择选项：", select_text)
                    bank_json[i] = select_text
                    AnswerPage().skip_operator(i, num, '补全文章', self.wait_check_complete_article_page,
                                               self.judge_tip_status, i, next_page=1)

    @teststep
    def judge_tip_status(self, i):
        if self.opt_char()[i].get_attribute("selected") == "true":
            print('跳转后选中状态未发生改变')
        else:
            self.base_assert.except_error('Error-- 跳转后选中状态发生改变！')
