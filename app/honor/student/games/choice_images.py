#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:44
# -----------------------------------------
import random
import time

from selenium.webdriver.common.by import By
from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class ListenSelectImageGame(GameCommonEle):
    @teststep
    def wait_check_listen_image_page(self):
        """听音选图页面检查点 以题目索引id作为依据"""
        locator = (By.ID, self.id_type() + "img")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_ques_text_by_index(self, index):
        """听音题目选图页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '{}.')]".format(index))
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def get_ques_text_by_index(self, index):
        """根据索引值获取问题内容"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text, '{}.')]".format(index))
        return ele.text

    @teststep
    def get_images_by_index(self, index):
        """根据index 获取结果页图片信息"""
        ele = self.driver.find_elements_by_xpath("//android.widget.ImageView[contains(@content-desc, '## {} ##')]".format(index))
        return ele

    @teststep
    def ques_index(self):
        """问题索引"""
        ele = self.driver.find_element_by_id(self.id_type() + 'num')
        return ele.text

    @teststep
    def listen_question(self):
        """问题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sentence')
        return ele.text

    @teststep
    def image_options(self):
        """图片"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'img')
        return ele

    @teststep
    def voice_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'exo_play')
        return ele


    @teststep
    def image_choice_play_process(self, do_right=False, right_answer=None):
        """听音选图对错操作"""
        select_answer = ''
        image_options = self.image_options()
        if do_right:
            for x in image_options:
                if right_answer in x.get_attribute('contentDescription'):
                    select_answer = right_answer
                    x.click()
                    time.sleep(1)
                    break
        else:
            random_index = random.randint(0, len(image_options) - 1)
            random_choice = image_options[random_index]
            choice_desc = random_choice.get_attribute('contentDescription')
            select_answer = choice_desc
            random_choice.click()
        return select_answer

    @teststep
    def image_choice_lib_hw_operate(self, fq, half_exit, sec_answer=None):
        """听音选图作业 图书馆操作"""
        mine_answer = {}
        timer = []
        total_count = self.rest_bank_num()
        for x in range(total_count):
            ques_index = self.ques_index()
            question = ques_index + '.' + self.listen_question()
            print('问题：', question)

            if half_exit:
                if x == 1:
                    self.click_back_up_button()
                    self.tips_operate()
                    break

            if fq == 1:
                select_answer = self.image_choice_play_process()
            else:
                right_answer = sec_answer[str(x)]
                select_answer = self.image_choice_play_process(do_right=True, right_answer=right_answer)

            mine_answer[str(x)] = select_answer
            print('选择答案：', select_answer)
            timer.append(self.bank_time())
            time.sleep(3)
            print('-' * 30, '\n')
        self.judge_timer(timer)
        self.next_btn_judge('true', self.fab_commit_btn)
        while True:
            self.fab_commit_btn().click()
            if Toast().find_toast('请听完音频，再提交答案'):
                time.sleep(3)
            else:
                break
        print(mine_answer)
        return mine_answer

    @teststep
    def image_choice_result_operate(self, mine_answer=None):
        """听音选图结果页面处理"""
        right_answer = {}
        right_count = 0
        # self.voice_button().click()
        for x in range(len(mine_answer)):
            if x == len(mine_answer) - 1:
                index_num = x+1
                self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
            else:
                index_num = x+2

            while not self.wait_check_ques_text_by_index(index_num):
                self.screen_swipe_up(0.5, 0.9, 0.8, 500)
            question = self.get_ques_text_by_index(str(x+1))
            print('问题：', question)
            images = self.get_images_by_index(x)
            mine_done_answer = mine_answer[str(x)]
            print('我的答案：', mine_done_answer)
            for img in images:
                img_content = img.get_attribute('contentDescription')
                if mine_done_answer in img_content:
                    if GetAttribute().get_selected(img) == 'false':
                        self.base_assert.except_error('选择答案后，结果页显示未选中')
                    if 'true' in img_content:
                        print('正确答案：', img_content)
                        right_answer[str(len(right_answer))] = img_content.split('##')[0].strip()
                        right_count += 1
                else:
                    if GetAttribute().get_selected(img) == 'true':
                        self.base_assert.except_error('未选此选项，结果页显示被选中')

                    if 'true' in img_content:
                        print('正确答案：', img_content)
                        right_answer[str(len(right_answer))] = img_content.split('##')[0].strip()
            print('-'*30, '\n')
        print('再练一遍答案：', right_answer)
        return right_answer, right_count, len(mine_answer)

