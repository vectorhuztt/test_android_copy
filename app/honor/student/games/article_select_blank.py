#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:49
# -----------------------------------------
import random
import re
import string

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.login.object_page.home_page import HomePage
from conf.decorator import teststep


class SelectBlankGame(GameCommonEle):
    """选词填空"""
    @teststep
    def wait_check_select_blank_page(self):
        """选词填空页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        return self.wait.wait_check_element(locator)

    def wait_check_hint_btn_page(self):
        """检测是否存在提示按钮"""
        locator = (By.ID, '{}prompt'.format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_hint_content_page(self):
        """提示词页面检查点"""
        locator = (By.ID, '{}md_titleFrame'.format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def hint_answer(self):
        """提示答案"""
        locator = (By.XPATH, '//android.widget.FrameLayout[contains(@resource-id ,"md_customViewFrame")]/'
                             'android.widget.ScrollView/android.widget.TextView')
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def hint_btn(self):
        """提示词"""
        locator = (By.ID, self.id_type() + 'prompt')
        return self.wait.wait_find_element(locator)

    @teststep
    def select_blank_play_process(self, do_right=False, right_answer=None):
        """选词填空对错操作"""
        if do_right:
            for x in right_answer:
                if x == ' ':
                    self.keyboard.games_keyboard('blank')
                self.keyboard.games_keyboard(x)
            self.keyboard.games_keyboard('enter')
            input_answer = right_answer
        else:
            random_str = ''.join(random.sample(string.ascii_letters, random.randint(2,5)))
            for x in random_str:
                self.keyboard.games_keyboard(x)
            input_answer = random_str
            self.keyboard.games_keyboard('enter')
        return input_answer


    @teststep
    def select_blank_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """选词填空操作"""
        mine_answer = {}
        timer = []
        if self.wait_check_hint_btn_page():
            self.hint_btn().click()  # 点击提示词，检验提示页面是否出现
            if not self.wait_check_hint_content_page():
                self.base_assert.except_error('点击提示词按钮未出现提示词')
            else:
                print('提示词：', self.hint_answer())
            HomePage().click_blank()

        if fq == 1:
            content = self.rich_text()
            print(content.text)
        total_count = self.rest_bank_num()
        for x in range(total_count):
            self.rate_judge(total_count, x)
            self.next_btn_judge('false', self.fab_commit_btn)  # 判断下一步状态
            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                input_answer = self.select_blank_play_process()
            else:
                right_answer = sec_answer[str(x)]
                input_answer = self.select_blank_play_process(do_right=True, right_answer=right_answer)
            mine_answer[str(x)] = input_answer
            timer.append(self.bank_time())
        if not half_exit:
            self.judge_timer(timer)
            print('本次做题答案：', mine_answer)
            self.check_position_change()
            self.next_btn_operate('true', self.fab_commit_btn)  # 判断下一步状态
        return mine_answer

    @teststep
    def select_bank_result_operate(self, mine_answer):
        """选词填空结果页处理"""
        again_right_answer = {}
        right_count = 0
        if self.wait_check_hint_btn_page():
            self.hint_btn().click()  # 点击提示词，校验是否出现提示答案页面
            if not self.wait_check_hint_content_page():
                self.base_assert.except_error('点击提示词按钮未出现提示词')
            else:
                print('提示词：', self.hint_answer())
            HomePage().click_blank()

        content = self.rich_text()   # 从desc中获取正确答案
        content_desc = content.get_attribute('contentDescription')
        answers = [x for x in content_desc.split('## ')[1].split('  ') if x and '(' not in x]
        mine_input_answer = re.findall(r'\d+[.](.*?)[.,?!].*?', content.text)
        print(mine_input_answer)
        for i, mine in enumerate(mine_input_answer):
            print('我的答案：', mine_answer[str(i)].lower())
            if '(' in mine:
                again_right_answer[str(len(again_right_answer))] = answers[i]
            else:
                if mine_answer[str(i)].lower() not in mine.lower():
                    self.base_assert.except_error('填入单词与结果页不一致')
                right_count += 1
        print('错题再练答案：', again_right_answer)
        return again_right_answer, right_count, len(mine_answer)






