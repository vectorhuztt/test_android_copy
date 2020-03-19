# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2018/12/17 10:59
# -------------------------------------------
from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_init import AllGameClass
from app.honor.student.library.object_page.game_result_page import ResultPage
from app.honor.student.listen_everyday.object_page.listen_home_page import ListenHomePage
from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps



class ListenGamePage(BasePage):

    def __init__(self):
        self.home = HomePage()
        self.listen = ListenHomePage()
        self.all_game = AllGameClass()

    @teststep
    def wait_check_gaming_page(self):
        """以游戏界面计时的id作为根据"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"待完成:")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_red_hint_page(self):
        """听后选择页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_hint')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_image_page(self):
        """听音选图 -- 以题号的id作为根据"""
        locator = (By.ID, self.id_type() + 'num')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_rich_page(self):
        """听音连句页面检查点"""
        locator = (By.ID, self.id_type() + 'rich_text')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_result_page(self):
        """结果检查点 以打卡的id作为依据"""
        locator = (By.ID, '{}today_minute'.format(self.id_type()))
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_error_hint_page(self):
        """不达标字样提示页面检查点"""
        locator = (By.ID, '{}error_hint'.format(self.id_type()))
        return self.get_wait_check_page_result(locator, timeout=5)


    @teststep
    def today_excise_time(self):
        """今日已练时间"""
        ele = self.driver.find_element_by_id("{}today_minute".format(self.id_type()))
        return ele.text

    @teststep
    def excise_date(self):
        """练习日期"""
        ele = self.driver.find_element_by_id('{}date'.format(self.id_type()))
        return ele.text

    @teststep
    def excise_correct_rate(self):
        """正确率"""
        ele = self.driver.find_element_by_id("{}right_rate".format(self.id_type()))
        return ele.text

    @teststep
    def error_hint(self):
        """正确率不足60%提示"""
        ele = self.driver.find_element_by_id('{}error_hint'.format(self.id_type()))
        return ele

    @teststep
    def punch_button(self):
        """打卡"""
        ele = self.driver.find_element_by_id("{}share".format(self.id_type()))
        return ele

    @teststep
    def check_answer_button(self):
        """查看答案"""
        ele = self.driver.find_element_by_id("{}detail".format(self.id_type()))
        return ele

    @teststep
    def redo_button(self):
        """重练此题"""
        ele = self.driver.find_element_by_id("{}again".format(self.id_type()))
        return ele

    @teststep
    def rank_button(self):
        """排行榜"""
        ele = self.driver.find_element_by_id('{}rank'.format(self.id_type()))
        return ele


    @teststep
    def audio_button(self):
        """声音按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'play_voice')
        return ele

    @teststep
    def split_sentence_word(self):
        """候选单词"""
        ele = self.driver.find_elements_by_id(self.id_type() + "text")
        word_list = [i for i in ele if i.text != '']
        return word_list

    @teststep
    def correct_answer(self):
        """正确答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'tv_right')
        return ele

    @teststep
    def play_listen_game_process(self):
        bank_info = 0
        bank_type = 0
        if self.wait_check_image_page():
            print('===== 听音选图 =====\n')
            bank_info = self.all_game.image_choice.image_choice_lib_hw_operate(fq=1, half_exit=False)
            bank_type = 1

        elif self.wait_check_rich_page():
            print('===== 听音连句 =====\n')
            bank_info = self.all_game.sentence_listen_link.sentence_listen_link_lib_hw_operate(fq=1, half_exit=False)
            bank_type = 2

        elif self.wait_check_red_hint_page():
            print('===== 听后选择 =====\n')
            bank_info = self.all_game.listen_choice.listen_choice_lib_hw_operate(fq=1, half_exit=False)
            bank_type = 3

        return bank_type, bank_info

    @teststeps
    def answer_page_operate(self, bank_type, bank_info):
        if self.wait_check_result_page():
            print('----- < 结果页 > -----\n')
            today_excise = self.today_excise_time()
            date = self.excise_date()
            rate = self.excise_correct_rate()
            print(today_excise, '\n', date, '\n', rate, '\n')
            if self.wait_check_error_hint_page():
                print(self.error_hint().text, '\n')
            self.punch_button().click()
            self.all_game.listen_choice.share_page_operate()
            if self.wait_check_result_page():
                self.check_answer_button().click()

            if ResultPage().wait_check_answer_page():
                if bank_type == 1:
                    print('----- < 听音选图答案详情页 > -----', '\n')
                    self.all_game.image_choice.image_choice_result_operate(bank_info)

                elif bank_type == 2:
                    print('----- < 听音连句答案详情页 > -----', '\n')
                    self.all_game.sentence_listen_link.sentence_listen_link_result_operate(bank_info)

                elif bank_type == 3:
                    print('----- < 听后选择答案详情页 > -----', '\n')
                    self.all_game.single_choice.single_choice_result_operate(bank_info, '听后选择')
                self.home.click_back_up_button()

