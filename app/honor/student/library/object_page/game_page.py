# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/27 13:12
# -------------------------------------------
from selenium.webdriver.common.by import By
from app.honor.student.library.object_page.game_result_page import ResultPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class LibraryGamePage(BasePage):
    def __init__(self):
        self.result = ResultPage()

    @teststep
    def wait_check_top_name_page(self, name):
        locator = (By.XPATH, '//android.view.ViewGroup[contains(@resource-id, "common_toolbar")]/'
                             'android.widget.TextView[contains(@text,"{}")]'.format(name))
        return self.get_wait_check_page_result(locator, timeout=10)

    @teststep
    def wait_check_share_page(self):
        """分享页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"图书分享")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_bank_list_page(self):
        """大题列表页面检查点"""
        locator = (By.ID, '{}tv_testbank_name'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_game_page(self):
        """游戏页面检查点"""
        locator = (By.ID, '{}progress'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_share_area_page(self):
        """分享页面检查点"""
        locator = (By.ID, '{}share_area'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststeps
    def wait_check_game_list_page(self, var):
        """以 小游戏的class_name为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, %s)]" % var)
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_homework_list_page(self):
        """作业页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}tv_homework_name')]".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def homework_list(self):
        """作业列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_homework_name')
        return ele

    @teststep
    def share_btn(self):
        """分享"""
        ele = self.driver.find_element_by_id(self.id_type() + 'share')
        return ele

    @teststep
    def share_page_menu_share_btn(self):
        """分享页面的分享按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'menu_share')
        return ele

    @teststep
    def punch_share_btn(self):
        """立即打卡 -分享页面"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sign')
        return ele

    @teststep
    def start_game_btn(self):
        """开始阅读 -做题页面"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sign_bottom')
        return ele


    @teststep
    def bank_name_list(self):
        """大题列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_testbank_name')
        return ele

    @teststep
    def bank_type(self):
        """大题类型"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_testbank_type')
        return ele

    @teststep
    def bank_name_by_type(self, bank_type):
        """根据大题题型获取题目名称"""
        ele = self.driver.find_elements_by_xpath('//android.widget.TextView[@text="{}"]/../preceding-sibling::'
                                                 'android.widget.RelativeLayout/android.widget.TextView[contains'
                                                 '(@resource-id, "tv_testbank_name")]'.format(bank_type))
        return ele

    @teststep
    def bank_name(self):
        """大题名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_testbank_name')
        return ele

    @teststep
    def bank_progress_by_name(self, bank_name):
        """根据大题名称获取"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling::android.widget.RelativeLayout/'
                                                'android.widget.TextView[contains(@resource-id, "tv_testbank_status")]'.format(bank_name))
        return ele.text

    @teststep
    def click_bank_by_name(self, bank_name):
        """通过名称定为大题并点击"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]'.format(bank_name))
        ele.click()

    @teststep
    def game_name(self):
        """游戏名称"""
        ele = self.driver.find_element_by_xpath('//*[@resource-id="{}common_toolbar"]/'
                                                'android.widget.TextView'.format(self.id_type()))
        return ele.text


    @teststep
    def check_process_change(self, bank_name, bank_progress):
        """检查大题进度变化"""
        print(self.wait_check_bank_list_page())
        if self.wait_check_bank_list_page():
            print(bank_name)
            if self.bank_progress_by_name(bank_name) != bank_progress:
                self.base_assert.except_error('中途返回进度却发生变化！')
            self.click_bank_by_name(bank_name)
            if self.wait_check_game_page():
                pass

    @teststep
    def enter_into_game(self, hw_name, bank_type):
        """进入游戏过程"""
        hw_name_list = 0
        if self.wait_check_homework_list_page():  # 页面检查点
            homework_name = []
            while True:
                for hw in self.homework_list():
                    if hw.text in homework_name:
                        continue
                    else:
                        homework_name.append(hw.text)
                        if hw_name == hw.text:
                            hw.click()
                            break
                if hw_name not in homework_name:
                    self.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                else:
                    break
            if self.wait_check_game_list_page(hw_name):
                while True:
                    game_list = self.bank_type()
                    if bank_type not in [x.text for x in game_list]:
                        self.screen_swipe_up(0.5, 0.9, 0.5, 1000)
                    else:
                        if game_list[-1].text == bank_type:
                            self.screen_swipe_up(0.5, 0.9, 0.85, 1000)
                        break
            else:
                print('❌❌❌ 未进入大题列表')
        return hw_name_list

    @teststep
    def play_book_games(self, fq, second_ans=None, nickname=None, half_exit=False):
        """各种游戏过程
           fq:: 大题练习次数
           sec_answer :: 第二次练习的正确答案
           half_exit :: 是否中途退出 针对第三个脚本
           total_num :: 记录每道大题的总数
           bank_name :: 大题名称
           nickname: 昵称
        """
        if fq == 1:
            print('========== 第一次做错操作 ========== \n')
        else:
            print('========== 第二次做对操作 ========== \n')

        game_name = self.game_name()
        game_result = {}

        if game_name == "猜词游戏":
            game_result = self.result.all_game.word_guess.guess_word_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '还原单词':
            game_result = self.result.all_game.word_restore.restore_word_lib_hw_operate(fq, half_exit, second_ans)
        #
        elif game_name == '连连看':
            game_result = self.result.all_game.word_match.word_match_lib_hw_operate(fq, half_exit)

        elif game_name == '单词拼写':
            game_result = self.result.all_game.word_spell.word_spell_lib_hw_operate(fq, half_exit, second_ans)
        #
        elif game_name == '单词听写':
            game_result = self.result.all_game.listen_spell.listen_spell_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '词汇选择':
            game_result = self.result.all_game.vocab_choice.vocab_choice_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '句型转换':
            game_result = self.result.all_game.sentence_change.sentence_change_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '听音连句':
            game_result = self.result.all_game.sentence_listen_link.sentence_listen_link_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '强化炼句':
            game_result = self.result.all_game.sentence_strengthen.sentence_strengthen_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '连词成句':
            game_result = self.result.all_game.sentence_link.sentence_link_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '单项选择':
            game_result = self.result.all_game.single_choice.single_choice_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '补全文章':
            game_result = self.result.all_game.complete_article.complete_article_lib_hw_operate(fq, half_exit, second_ans)
        #
        elif game_name == '完形填空':
            game_result = self.result.all_game.cloze.cloze_game_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '阅读理解':
            game_result = self.result.all_game.read_understand.article_understand_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '选词填空':
            game_result = self.result.all_game.select_blank.select_blank_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '听后选择':
            game_result = self.result.all_game.listen_choice.listen_choice_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '听音选图':
            game_result = self.result.all_game.image_choice.image_choice_lib_hw_operate(fq, half_exit, second_ans)

        elif game_name == '闪卡练习':
            self.result.all_game.word_flash.play_flash_game(half_exit)

        elif game_name == '单词跟读':
            self.result.all_game.word_speak.word_speak_game_operate(nickname, half_exit)
        return game_name, game_result





