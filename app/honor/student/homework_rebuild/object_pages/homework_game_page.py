#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2020/1/7 11:24
# -----------------------------------------
from app.honor.student.library.object_page.game_page import LibraryGamePage
from conf.base_page import BasePage
from conf.decorator import teststeps


class HomeworkGameOperate(BasePage):
    def __init__(self):
        self.library = LibraryGamePage()

    @teststeps
    def homework_game_operate(self, nickname, judge_score=True, has_medal=False, is_activity=False):
        """作业流程"""
        if self.library.wait_check_game_page():
            star_count, score_count, total_count = 0, 0, 0
            game_answer = {}
            for x in range(1):
                if self.library.wait_check_game_page():
                    game_name, game_result = self.library.play_book_games(x + 1, second_ans=game_answer, nickname=nickname,
                                                                          half_exit=False)
                    result_info = self.library.result.check_bank_result(game_name, game_result, has_medal=has_medal)
                    if self.library.result.wait_check_result_page():
                        if x == 0:
                            total_count = len(game_result)
                        if x == 1 and game_name in ['阅读理解', '听后选择', '听音选图']:
                            score_count = total_count - score_count
                            star_count += 0
                            if self.library.result.again_btn().text != '再练一遍':
                                self.base_assert.except_error('结果页【再练一遍/错题再练】按钮文本不是再练一遍')
                        else:
                            star_count += result_info[-1]
                            score_count += result_info[1]
                            if score_count > total_count:
                                score_count = total_count

                        self.library.result.result_multi_data_check(x + 1, result_info, star_count, score_count, judge_score=judge_score)
                        game_answer = result_info[0]
            if not is_activity:
                if not self.library.wait_check_bank_list_page():
                    self.library.click_back_up_button()
                    self.library.result.all_game.word_spell.tips_operate()