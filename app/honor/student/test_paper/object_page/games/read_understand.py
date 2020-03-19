from app.honor.student.games.article_read_understand import ReadUnderstandGame
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from conf.decorator import teststeps, teststep


class ReadUnderstand(ReadUnderstandGame):

    @teststeps
    def play_read_understand_game(self, num, exam_json):
        exam_json['阅读理解'] = bank_json = {}
        text = self.rich_text().text
        print(text)
        self.drag_up_down(drag_down=False)
        for x in range(num):
            if x != num - 1:
                index_num = x+1
            else:
                index_num = x
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            while not self.wait_check_article_container_by_index(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.8, 500)
            question = self.get_question_by_bank_index(x).text
            print('问题：', question)
            select_answer = self.cloze_game_play_process(x)
            print('选择答案：', select_answer)
            bank_json[x] = select_answer
            AnswerPage().skip_operator(x, num, '阅读理解', self.wait_check_read_understand_page,
                                       self.judge_tip_status, x, select_answer)


    @teststep
    def judge_tip_status(self, opt_index, opt_text):
        options = self.get_opt_text_by_index(opt_index)
        selected_text = [x for x in options if x.text == opt_text]
        if selected_text[0].get_attribute('selected') != 'true':
            self.base_assert.except_error('Error-- 跳转回来后题目完成状态发生变化')
        else:
            print('题目跳转后题目状态未改变：已完成')