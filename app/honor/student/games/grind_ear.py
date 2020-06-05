import re
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from conf.decorator import teststep


class GrindingEarGame(GameCommonEle):
    @teststep
    def wait_check_grind_ear_game_page(self):
        """磨耳朵页面检查点"""
        locator = (By.ID, self.id_type() + "start")
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_en_change_btn_page(self):
        """磨耳朵解释隐藏显示切换按钮检查点"""
        locator = (By.ID, "status")
        return self.wait.wait_check_element(locator, timeout=3)

    @teststep
    def wait_check_grinding_ear_result_page(self):
        """磨耳朵结果页页面检查点"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text, '本次磨耳朵时长')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def audio_time_length(self):
        """音频总时长"""
        locator = (By.ID, self.id_type() + 'time')
        ele = self.wait.wait_find_element(locator)
        res = ele.text.split(':')
        return int(res[0]) * 60 + int(res[1])

    @teststep
    def start_audio(self):
        """播放按钮"""
        locator = (By.ID, self.id_type() + 'start')
        return self.wait.wait_find_element(locator)

    @teststep
    def en_change_btn(self):
        """英汉切换按钮"""
        locator = (By.ID, self.id_type() + 'status')
        return self.wait.wait_find_element(locator)

    @teststep
    def bg_imag(self):
        """背景图片"""
        locator = (By.ID, self.id_type() + 'subtitle')
        return self.wait.wait_find_element(locator)

    @teststep
    def sentence(self):
        """听读的句子"""
        locator = (By.ID, self.id_type() + 'sentence')
        return self.wait.wait_find_element(locator)

    def wait_check_tips_operate(self):
        if self.wait_check_tips_page():
            return False
        else:
            time.sleep(3)
            return self.wait_check_tips_operate()

    @teststep
    def grinding_ear_game_operate(self):
        """磨耳朵游戏处理"""
        if self.wait_check_grind_ear_game_page():
            audio_length = self.audio_time_length()
            print("音频时长：", audio_length)
            if self.wait_check_en_change_btn_page():
                self.en_change_btn().click()
                sentences = self.sentence()
                zhPattern = re.compile(u'[\u4e00-\u9fa5]')
                if not zhPattern.search(sentences[0].text):
                    self.base_assert.except_error(
                        '存在显示解释按钮， 点击显示解释，下方句子未出现中文字样')
                self.en_change_btn().click()

            self.start_audio().click()

            time.sleep(audio_length + 3)
            self.wait_check_tips_operate()
            self.tips_operate()
            self.next_btn_operate('true', self.commit_without_fab_btn)
        if self.wait_check_grinding_ear_result_page():
            self.click_back_up_button()
