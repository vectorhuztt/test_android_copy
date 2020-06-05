#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:49
# -----------------------------------------
import random

from selenium.webdriver.common.by import By

from app.honor.student.games.choice_single import SingleChoiceGame
from conf.decorator import teststep, teststeps


class ClozeGame(SingleChoiceGame):
    """完型填空游戏"""
    @teststep
    def wait_check_cloze_page(self):
        """完形填空页面检查点"""
        locator = (By.ID, self.id_type() + "rich_text")
        return self.wait.wait_check_element(locator)

    @teststeps
    def cloze_game_play_process(self, game_type=1, index=0, do_right=False, right_answer=None):
        """完形填空对错操作"""
        select_answer = ''
        if do_right:
            for x in self.get_opt_text_by_index(index):
                if x.text == right_answer:
                    select_answer = right_answer
                    x.click()
                    break
        else:
            if game_type:
                opt_chars = self.get_opt_char_by_index(index)
                opt_text = self.get_opt_text_by_index(index)
            else:
                opt_chars = self.opt_char()
                opt_text = self.opt_options()
            for j, char in enumerate(opt_chars):
                print(char.text, ' ', opt_text[j].text)
            random_index = random.randint(0, len(opt_chars) - 1)
            random_opt = opt_text[random_index]
            select_answer = random_opt.text
            random_opt.click()
        return select_answer

    @teststeps
    def cloze_game_lib_hw_operate(self, fq, half_exit, sec_answer):
        """完形填空主要步骤"""
        mine_answer = {}
        timer = []
        if fq == 1:
            article = self.rich_text()
            print(article.text)

        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.rate_judge(total_count, x)  # 剩余题数校验
            question = self.question().text.strip()
            print('问题：', question)
            self.next_btn_judge('false', self.fab_next_btn)  # 判断下一题状态
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                select_answer = self.cloze_game_play_process(game_type=0)
            else:
                right_answer = sec_answer[str(x)]
                select_answer = self.cloze_game_play_process(game_type=0, do_right=True, right_answer=right_answer)
            print('选择答案：', select_answer)
            mine_answer[str(x)] = select_answer
            timer.append(self.bank_time())
            print('-'*30, '\n')

        if not half_exit:
            self.judge_timer(timer)
            self.drag_up_down(drag_down=True)
            self.check_position_change()
            self.next_btn_operate("true", self.fab_next_btn)
            print('我的答案：', mine_answer)
        return mine_answer







