import re
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep


class GrindingEarGame(GameCommonEle):
    @teststep
    def wait_check_grind_ear_game_page(self):
        """磨耳朵页面检查点"""
        locator = (By.ID, "start")
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_en_change_btn_page(self):
        """磨耳朵解释隐藏显示切换按钮检查点"""
        locator = (By.ID, "status")
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_grinding_ear_result_page(self):
        """磨耳朵结果页页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '本次磨耳朵时长')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def start_audio(self):
        """播放按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'start')
        return ele

    @teststep
    def en_change_btn(self):
        """英汉切换按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'status')
        return ele

    @teststep
    def bg_imag(self):
        """背景图片"""
        ele = self.driver.find_element_by_id(self.id_type() + 'subtitle')
        return ele

    @teststep
    def sentence(self):
        """听读的句子"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'sentence')
        return ele

    @teststep
    def grinding_ear_game_operate(self):
        """磨耳朵游戏处理"""
        if self.wait_check_grind_ear_game_page():
            if self.wait_check_en_change_btn_page():
                self.en_change_btn().click()
                sentences = self.sentence()
                zhPattern = re.compile(u'[\u4e00-\u9fa5]')
                if not zhPattern.search(sentences[0].text):
                    self.base_assert.except_error(
                        '存在显示解释按钮， 点击显示解释，下方句子未出现中文字样')
                self.en_change_btn().click()

            self.start_audio().click()
            while not self.wait_check_tips_page():
                time.sleep(3)
            self.tips_operate()
            self.next_btn_operate('true', self.commit_without_fab_btn)
        if self.wait_check_grinding_ear_result_page():
            self.click_back_up_button()