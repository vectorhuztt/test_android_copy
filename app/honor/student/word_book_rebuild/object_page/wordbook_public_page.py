#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 14:37
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute


class WorldBookPublicPage(BasePage):

    @teststep
    def wait_check_game_title_page(self):
        """游戏标题页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_title')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_play_voice_page(self):
        """喇叭播放按钮"""
        locator = (By.ID, '{}play_voice'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def game_title(self):  # 题型标题
        title = self.driver\
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    @teststep
    def game_mode_id(self):
        """获取题目的mode_id"""
        mode_id = int(self.game_title().get_attribute('contentDescription').split('  ')[1])
        return mode_id

    @teststep
    def get_explain_id(self, explain_ele):
        return explain_ele.get_attribute('contentDescription')

    @teststep
    def check_word_order_is_right(self, study_words, word_info, sys_only=False):
        """查看单词练习顺序是否正确"""
        print('======== 开始单词校验 ===========')
        record_page_ids = list(word_info.keys())
        error_code = []
        print("数据库记录id：", study_words)
        print("页面获取id：", record_page_ids)
        if sys_only or len(study_words) >= 10:
            for x in record_page_ids:
                if int(x) not in study_words:
                    print('❌❌❌ 此单词不在需要练习列表中！', word_info[x])
                    error_code.append(x)
        else:
            for x in study_words:
                if str(x) not in record_page_ids:
                    print('❌❌❌ 此单词为老师布置，但是未在学习列表中！', word_info[x])
                    error_code.append(x)

        if not len(error_code):
            print('单词顺序校验成功\n')

        print('======== 单词顺序校验完毕 ============\n')

    @teststep
    def check_word_is_only_has_vocab_apply(self, explain_id, new_explain_words, stu_id):
        """查看单词是否只有词汇运用"""
        if explain_id in new_explain_words:
            print('此单词是新释义单词')
            word_level = WordDataHandlePage().get_level_by_explain_id(explain_id, stu_id)
            lager_level_count = WordDataHandlePage().check_has_other_studied_explain(explain_id, stu_id, word_level)
            if lager_level_count:
                print('❌❌❌ 存在F值比此单词大的解释，单词复习只有词汇运用，不应在此游戏中出现')