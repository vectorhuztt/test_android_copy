#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/3 9:19
# -----------------------------------------
import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from app.honor.student.games.word_spell import SpellWordGame
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast


class WordSpeakGame(SpellWordGame):

    @teststep
    def wait_check_word_speak_page(self):
        """单词跟读页面检查点"""
        locator = (By.ID, self.id_type() + 'game_record_button')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_max_time_tip_page(self):
        """五次过后文本提示"""
        locator = (By.ID, self.id_type() + 'result_hint')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_explain_page(self):
        """解释页面检查点"""
        locator = (By.ID, self.id_type() + 'hint')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def wait_check_speak_word_result_page(self):
        """单词跟读结果页页面检查点"""
        locator = (By.ID, self.id_type() + 'game_name')
        return self.get_wait_check_page_result(locator, timeout=3)

    @teststep
    def speak_button(self):
        """说话按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'game_record_button')
        return ele

    @teststep
    def audio_btn(self):
        """喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_play')
        return ele

    @teststep
    def speak_word(self):
        """跟读单词"""
        ele = self.driver.find_element_by_id(self.id_type() + 'english')
        return ele.text

    @teststep
    def word_explain(self):
        """单词解释"""
        ele = self.driver.find_element_by_id(self.id_type() + 'hint')
        return ele.text

    @teststep
    def max_time_hint(self):
        """次数限制后的文本提示"""
        ele = self.driver.find_element_by_id(self.id_type() + 'result_hint')
        return ele.text

    # 结果页
    @teststep
    def user_name(self):
        """用户"""
        ele = self.driver.find_element_by_id(self.id_type() + 'name')
        return ele.text

    @teststep
    def group_word_check(self, index):
        """结果页 单词对错标识"""
        ele = self.driver.find_element_by_xpath('//*[@content-desc="{}" and contains(@resource-id, "item_container")]/'
                                                'android.widget.CheckBox[contains(@resource-id, "check")]'.format(index))
        return ele

    @teststep
    def again_btn(self):
        """再练一遍按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'again')
        return ele

    @teststeps
    def word_speak_game_process(self, fq, half_exit, again_words=None):
        """单词跟读游戏处理过程"""
        mine_answer = []
        if self.wait_check_word_speak_page():
            total_num = self.rest_bank_num()
            timer = []
            for x in range(total_num):
                if self.wait_check_word_speak_page():
                    self.rate_judge(total_num, x)
                    self.next_btn_judge('false', self.audio_btn)
                    self.next_btn_judge('false', self.fab_next_btn)
                    print('解释：', self.word_explain())
                    word = self.speak_word()
                    mine_answer.append(word)
                    print('单词：', word)

                    if half_exit:
                        if x == 1:
                            self.click_back_up_button()
                            self.tips_operate()
                            break

                    if fq == 2:
                        if word not in again_words:
                            self.base_assert.except_error('该单词不在选择再练单词列表内 ' + word)
                    if x == 0 and fq == 1:
                        self.speak_button().click()
                        # 允许录音权限
                        if self.wait_check_permit_tab_page():
                            self.always_permit_allow_btn().click()
                        if self.wait_check_permit_tab_page():
                            self.always_permit_allow_btn().click()
                        if self.wait_check_permit_tab_page():
                            self.always_permit_allow_btn().click()

                    if self.wait_check_word_speak_page():
                        self.speak_button().click()
                        time.sleep(21)
                        if not Toast().find_toast('录音时长不得超过'):
                            self.base_assert.except_error('未发现录音超时提示 ' + word)
                        for i in range(4):
                            self.speak_button().click()
                            time.sleep(2)
                            self.speak_button().click()
                            time.sleep(1)
                        if not self.wait_check_max_time_tip_page():
                            self.base_assert.except_error('已成功录音五次， 未出现进入下一题提示')
                        else:
                            self.max_time_hint()

                        if self.speak_button().get_attribute('enabled') == 'true':
                            self.base_assert.except_error('已成功录音5次， 话筒按钮未置灰')
                    else:
                        self.speak_button().click()
                        time.sleep(3)
                        self.speak_button().click()
                    self.next_btn_judge('true', self.audio_btn)
                    timer.append(self.bank_time())
                    self.next_btn_operate('true', self.fab_next_btn)
                    print('-'*30, '\n')
        return mine_answer

    @teststeps
    def word_speak_result_operate(self, nickname, game_count, game_result):
        """单词跟读结果页处理"""
        print('======== 单词跟读查看结果页 ===========\n')
        if self.wait_check_speak_word_result_page():
            user_name = self.user_name()
            if user_name != nickname:
                self.base_assert.except_error('页面用户名与系统用户名不一致')
            for x in range(game_count):
                if x != game_count - 1:
                    index_num = x + 1
                else:
                    index_num = x
                    self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                while not self.wait_check_word_container_by_index_and_id(index_num):
                    self.screen_swipe_up(0.5, 0.9, 0.8, 500)

                word = self.group_word(x)
                explain = self.group_explain(x)
                self.group_word_voice(x).click()
                word_check = self.group_word_check(x)
                print('单词：', word)
                print('解释：', explain)
                if word in game_result:
                    if word_check.get_attribute('checked') != 'true':
                        self.base_assert.except_error('已练单词结果页选择按钮未被选中 ' + word)
                    else:
                        if x % 2 == 0:
                            word_check.click()
                            game_result.remove(word)
                print('-'*30, '\n')
            self.again_btn().click()

    @teststeps
    def word_speak_game_operate(self, nickname, half_exit):
        game_result = self.word_speak_game_process(fq=1, half_exit=half_exit)
        game_count = len(game_result)
        self.word_speak_result_operate(nickname, game_count, game_result)
        self.word_speak_game_process(fq=2, half_exit=half_exit, again_words=game_result)




