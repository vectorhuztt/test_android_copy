#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/12 8:50
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.games.flash_card_page import FlashCard
from app.honor.student.word_book_rebuild.object_page.games.word_spelling_page import SpellingWord
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.games_keyboard import Keyboard


class MineWordsPage(BasePage):
    """单词本 - 我的单词"""
    def __init__(self):
        self.flash = FlashCard()
        self.spell = SpellingWord()
        self.data = WordDataHandlePage()
        self.assert_act = AssertAction()

    @teststeps
    def wait_check_mine_word_page(self):
        """以“我的单词”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'我的单词')]")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_end_page(self):
        """滑到底 页面检查"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'到底啦 下拉刷新试试')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststeps
    def wait_check_no_word_page(self):
        """wording:您还没有已背单词哦，快开始背单词吧"""
        locator = (By.ID, "//android.widget.TextView[contains(@text,'到底啦 下拉刷新试试')]")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except Exception:
            return False

    @teststeps
    def no_word_tip_text(self):
        """wording:您还没有已背单词哦，快开始背单词吧"""
        ele = self.driver.find_element_by_id(self.id_type() + 'status_error_hint_view').text
        print(ele.text)

    @teststep
    def click_my_word_btn(self):
        """我的单词"""
        self.driver.\
            find_element_by_id(self.id_type() + 'my_word')\
            .click()

    @teststep
    def total_word(self):
        """单词总数"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "total_word")
        return int(ele.text.split(':')[1])

    @teststep
    def get_words(self):
        """单词"""
        ele = self.driver\
            .find_elements_by_id(self.id_type() + "word")
        return ele

    @teststep
    def progress(self):
        """每个单词的轮次"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "progress")
        return ele

    @teststep
    def order_info(self):
        """排名"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_order")
        return ele

    @teststep
    def st_icon(self):
        """头像"""
        ele = self.driver\
            .find_elements_by_id(self.id_type() + "iv_head")
        return ele

    @teststep
    def st_name(self):
        """学生姓名"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_name")
        return ele

    @teststep
    def word_page_scale(self):
        """获取一页单词所占页面比例"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rv')
        return float('%.2f' % (ele.size['height']/self.get_window_size()[1]))


    @teststeps
    def get_all_mine_words(self, studied_words):
        """获取所有我的单词"""
        word_list = []
        swipe_scale = self.word_page_scale()

        while not self.wait_check_end_page():
            words = self.get_words()
            for x in words:
                if x.text in word_list:
                    continue
                else:
                    word_list.append(x.text)
            self.screen_swipe_up(0.5, 0.8, 0.9 - swipe_scale, 1100)
        print('我的单词：', word_list)
        error_words = [x for x in word_list if x not in studied_words]
        self.assert_act.assertFalse(error_words, '数据库未统计但是在我的单词中出现的单词：' + str(error_words))
        self.screen_swipe_up(0.5, 0.9, 0.9 - swipe_scale, 1000)

    @teststeps
    def flash_study_operate(self, count, stu_id):
        print('================ 闪卡学习模式 =====================\n')
        familiar_explains = self.data.get_student_familiar_explain_ids(stu_id)
        star_explains = self.data.get_student_star_explain_ids(stu_id)
        print('标星', star_explains)
        print('标熟', familiar_explains)

        for x in range(count):
            if self.flash.wait_check_flash_study_page():
                explain = self.flash.study_word_explain()
                explain_id = explain.get_attribute('contentDescription')
                print(explain_id)
                print('单词：', self.flash.study_word(), '\n',
                      '解释：', explain.text, '\n',
                      '句子：', self.flash.study_sentence(), '\n',
                      '句子解释：', self.flash.study_sentence_explain(), '\n',
                      '推荐老师：', self.flash.author(), '\n'
                      )
                if self.flash.star_button().get_attribute('selected') == 'true':
                    if explain_id not in star_explains:
                        print('❌❌❌ 标星按钮已被点击， 但是该单词不是标星单词')
                else:
                    if explain_id in star_explains:
                        print('❌❌❌ 标星按钮未被点击， 但是该单词是标星单词')
                    self.flash.star_button().click()
                    if x == 0:
                        self.flash.tips_operate()

                if self.flash.familiar_button().get_attribute('enabled') == 'true':
                    if explain_id not in familiar_explains:
                        print('❌❌❌ 标熟按钮未被点击， 但是该单词是标熟单词')
                    self.flash.familiar_button().click()
                    if x == 0:
                        self.flash.tips_operate()
                else:
                    if explain_id in familiar_explains:
                        print('❌❌❌ 标熟按钮已被点击， 但是该单词不是标熟单词')
                self.flash.fab_next_btn().click()
                print('-'*30, '\n')


    @teststeps
    def flash_copy_operate(self, count):
        print('================ 闪卡抄写模式 =====================\n')
        for x in range(count):
            if self.flash.wait_check_copy_page():
                word = self.flash.copy_word()
                print('单词：', word)
                print('解释：', self.flash.copy_explain().text)
                for i, alpha in enumerate(word):
                    Keyboard().keyboard_operate(i, alpha)
                print('-' * 30, '\n')
                time.sleep(3)

    @teststeps
    def spelling_operate(self, count, stu_id):
        print('================ 单词拼写模式 =====================\n')
        for x in range(count):
            if self.spell.wait_check_normal_spell_page():
                self.spell.next_btn_operate('false', self.spell.fab_commit_btn)
                explain = self.spell.word_explain()
                explain_id = explain.get_attribute('contentDescription')
                word = self.data.get_word_by_explain_id(stu_id, explain_id)
                for i, alpha in enumerate(word):
                    self.spell.keyboard_operate(i, alpha)
                self.spell.next_btn_operate('true', self.spell.fab_commit_btn)
                self.spell.fab_next_btn().click()
                print('-' * 30, '\n')