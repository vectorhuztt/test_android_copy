#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:48
# -----------------------------------------
import random
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep


class CompleteArticleGame(GameCommonEle):
    @teststep
    def wait_check_complete_article_page(self):
        """补全文章页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_opt_page(self, opt_text):
        """选项页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "{}")]'.format(opt_text))
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_opt_text_by_index(self, index):
        """判断当前索引下的选项是否在页面中"""
        locator = (By.XPATH, '//android.widget.LinearLayout[@index="{}"]/android.widget.LinearLayout'.format(index))
        return self.wait.wait_check_element(locator, timeout=3)

    @teststep
    def wait_check_select_opt_page(self, right_answer):
        locator = (By.XPATH, '//android.widget.TextView[@text="{}"]'.format(right_answer))
        return self.wait.wait_check_element(locator, timeout=3)


    @teststep
    def result_opt_char(self, opt_text):
        """结果页的选项"""
        locator = (By.XPATH, '//android.widget.TextView[@text="{}"]/preceding-sibling::android.widget.TextView'
                             '[contains(@resource-id, "tv_char")]'.format(opt_text))
        return self.wait.wait_find_element(locator)

    @teststep
    def complete_article_play_process(self, do_right=False, right_answer=None, timer=None):
        """补全文章对错操作"""
        select_answer = {}
        total_num = self.rest_bank_num()
        options = self.opt_options()
        if do_right:
            for i, y in enumerate(right_answer):
                has_swipe = False
                mine_selected_answer = right_answer[y]
                while True:
                    if not self.wait_check_select_opt_page(mine_selected_answer):
                        self.screen_swipe_up(0.5, 0.9, 0.8, 500)
                    else:
                        has_swipe = True
                        break
                self.rate_judge(total_num, i)
                select_answer[str(i)] = mine_selected_answer
                self.result_opt_char(mine_selected_answer).click()
                if timer is not None:
                    timer.append(self.bank_time())
                time.sleep(0.5)
                if has_swipe:
                    self.screen_swipe_down(0.5, 0.5, 0.9, 1000)
        else:
            for x in range(total_num):
                if x != total_num - 1:
                    index_num = x + 1
                else:
                    index_num = x
                    self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                while not self.wait_check_opt_text_by_index(index_num):
                    self.screen_swipe_up(0.5, 0.9, 0.8, 500)
                self.rate_judge(total_num, x)
                select_answer[str(x)] = options[x].text
                options[x].click()
                if timer is not None:
                    timer.append(self.bank_time())
                time.sleep(0.5)
        return select_answer

    @teststep
    def complete_article_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """补全文章游戏过程"""
        timer = []
        article = self.rich_text().text

        if fq == 1:
            print(article)
        self.drag_up_down(drag_down=False)
        self.next_btn_judge('false', self.fab_next_btn)
        if fq == 1:
            select_answer = self.complete_article_play_process(timer=timer)
        else:
            select_answer = self.complete_article_play_process(do_right=True, right_answer=sec_answer, timer=timer)
        self.judge_timer(timer)
        print('我的答案：', select_answer)
        if half_exit:
            self.click_back_up_button()
            self.tips_operate()
        else:
            self.drag_up_down(drag_down=True)
            self.screen_swipe_down(0.5, 0.2, 0.9, 1000)
            self.check_position_change()
            self.next_btn_operate('true', self.fab_next_btn)
        return select_answer

    @teststep
    def complete_article_result_operate(self, mine_answer):
        """补全文章结果页处理过程"""
        desc = self.rich_text().get_attribute('contentDescription')
        desc_right_answer = desc.split('## ')[1].split('  ')
        result_right_answer = [x for x in desc_right_answer if x and '(' not in x]
        self.drag_up_down(drag_down=False)
        right_answer = {}
        right_count = 0
        for i, x in enumerate(result_right_answer):
            is_swiped = False
            mine_done_answer = mine_answer[str(i)]
            print('正确答案：', x)
            print('我的答案：', mine_done_answer)
            while True:
                if not self.wait_check_select_opt_page(mine_done_answer):
                    self.screen_swipe_up(0.5, 0.9, 0.8, 500)
                else:
                    is_swiped = True
                    break
            mine_select_opt_char = self.result_opt_char(mine_done_answer)
            char_desc = mine_select_opt_char.get_attribute('contentDescription')
            if mine_done_answer != x:
                if char_desc == 'right':
                    self.base_assert.except_error('选择结果不正确，页面却显示正确')
                elif char_desc == 'error':
                    print('选项校验正确')
                right_answer[str(len(right_answer))] = x
            else:
                if char_desc == 'error':
                    self.base_assert.except_error('选择结果正确，页面却显示不正确')
                elif char_desc == 'right':
                    print('选项校验正确')
                right_count += 1

            if is_swiped:
                self.screen_swipe_down(0.5, 0.5, 0.9, 500)

            print('-'*30, '\n')
        print('错题再练答案：', right_answer)
        return right_answer, right_count, len(mine_answer)




