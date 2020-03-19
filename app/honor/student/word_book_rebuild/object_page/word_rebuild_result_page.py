
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast


class ResultPage(BasePage):

    def __init__(self):
        self.home = HomePage()

    @teststep
    def wait_check_result_page(self):
        """结果页 以今日已练单词图片的Id为依据"""
        locator = (By.ID, self.id_type() + 'word_count')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_wx_login_page(self):
        """微信登陆页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"登录微信")]')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_share_page(self):
        """打卡页，以分享图片id为依据"""
        locator = (By.ID, self.id_type() + "share_img")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_next_grade(self):
        """再来一组 以继续挑战的图片的Id为依据"""
        locator = (By.ID, self.id_type() + "level_up_hint")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_study_times_limit_page(self):
        """练习次数已用完页面检查点"""
        locator = (By.ID, self.id_type() + "error_img")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    @teststep
    def date(self):
        """时间日期"""
        ele = self.driver.find_element_by_id(self.id_type() + 'date')
        return ele.text

    @teststep
    def today_word(self):
        """今日已练单词"""
        ele = self.driver.find_element_by_id(self.id_type() + "word_count")
        return ele.text

    @teststep
    def already_remember_word(self):
        """已被单词"""
        ele = self.driver.find_element_by_id(self.id_type() + "all_word_count")
        return ele.text

    @teststep
    def word_detail_info(self):
        """复习新词组"""
        ele = self.driver.find_element_by_id(self.id_type() + "text")
        return ele.text


    @teststep
    def share_button(self):
        """打卡"""
        self.driver.\
            find_element_by_id(self.id_type() + 'punch_clock')\
            .click()
        time.sleep(2)

    @teststep
    def rank_button(self):
        """右上角排名按钮"""
        self.driver.\
            find_element_by_id(self.id_type() + "rank")\
            .click()
        time.sleep(3)

    @teststep
    def more_again_button(self):
        """再来一组"""
        print('再来一组', '\n')
        self.driver.\
            find_element_by_id(self.id_type() + "again")\
            .click()

    @teststep
    def level_up_text(self):
        """单词已练完说明"""
        ele = self.driver.find_element_by_id(self.id_type() + "level_up_hint").text
        print(ele)


    @teststep
    def no_study_btn(self):
        """不练了"""
        self.driver.\
            find_element_by_id(self.id_type() + "cancel")\
            .click()

    @teststep
    def wx_btn(self):
        """微信按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "weixin")
        return ele

    @teststep
    def wx_friend(self):
        """朋友圈"""
        ele = self.driver.find_element_by_id(self.id_type() + 'weixin_friends')
        return ele


    @teststep
    def nex_level_text(self):
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[@index,0]")
        print('已选年级 :%s'% ele)
        print('-'*30, '\n')


    @teststep
    def confirm_button(self):
        """继续练习"""
        self.driver.\
            find_element_by_id(self.id_type() + "confirm")\
            .click()

    @teststep
    def wx_back_up_btn(self):
        """微信页面返回按钮"""
        ele = self.driver.find_element_by_accessibility_id('返回')
        return ele

    @teststep
    def share_page_operate(self):
        """分享页面操作"""
        if self.wait_check_share_page():
            self.wx_btn().click()
            if self.wait_check_wx_login_page():
                self.wx_back_up_btn().click()
            else:
                print('❌❌❌ 未进入微信登陆页面')

        if self.wait_check_share_page():
            self.wx_friend().click()
            if self.wait_check_wx_login_page():
                self.wx_back_up_btn().click()
            else:
                print('❌❌❌ 未进入微信登陆页面')

        if self.wait_check_share_page():
            self.save_img().click()
            if not Toast().find_toast('已保存到本地'):
                print('❌❌❌ 未发现保存图片提示')
            self.click_back_up_button()

    @teststeps
    def check_result_word_data(self, new_word_count, new_explain_words_count, already_recite_count, group_count):
        """结果页面"""
        print(' <结果页>：')
        print('今日已练单词：%s' % self.today_word())
        print('日期：%s' % self.date())
        print(self.already_remember_word())
        print(self.word_detail_info())
        today_word_count = int(self.today_word())               # 今日已练单词 （复习+ 新词）
        already_count = int(re.findall(r'\d+', self.already_remember_word())[0])    # 已背单词
        detail = re.findall(r'\d+', self.word_detail_info())    # 最后一句统计文本
        study_group_count = int(detail[0])                      # 已练组数
        recite_count = int(detail[1])                           # 复习个数
        new_set_words = int(detail[2])                          # 新词个数
        new_explain_count = int(detail[3])                      # 新释义个数


        if already_count != new_word_count:
            print('❌❌❌ 已学单词数不正确，应为', new_word_count)

        if today_word_count != recite_count + new_set_words + new_explain_count:
            print('❌❌❌ 今日已练单词不等于复习+新词+新释义, 应为', recite_count + new_set_words + new_explain_count)

        if study_group_count != group_count+1:
            print('❌❌❌ 已练组数不正确， 应为', group_count+1)

        if new_set_words != new_word_count:
            print('❌❌❌ 新词学单词数不正确，应为', new_word_count)

        if new_explain_count != new_explain_words_count:
            print('❌❌❌ 新释义单词个数不正确， 应为', new_explain_words_count)

        if recite_count != already_recite_count:
            print('❌❌❌ 复习单词个数不正确， 应为', already_recite_count)

        if recite_count > 27:
            if group_count == 0:
                if new_word_count != 0:
                    print('❌❌❌ 复习个数大于等于28个, 不应存在新词个数')
            else:
                print('❌❌❌ 复习组数非第一组, 但是复习个数大于27')
        else:
            if new_word_count == 0:
                print('❌❌❌ 复习单词个数小于28, 新词个数为0')
            else:
                if group_count == 0:
                    if new_word_count not in range(3, 11):
                        print('❌❌❌ 复习单词个数小于28， 第一组新词个数不在3-10之间')
                else:
                    if new_word_count < 3:
                        print('❌❌❌ 复习单词个数小于28，非第一组新词个数小于3个')


    @teststep
    def back_to_home(self):
        self.home.click_back_up_button()
        if self.home.wait_check_tips_page():
            self.home.commit_button()
        if self.home.wait_check_word_title():
            self.home.click_back_up_button()
            if self.home.wait_check_home_page():  # 页面检查点
                print('返回主界面')

    @teststeps
    def result_page_handle(self, new_word_count, new_explain_words_count,
                           already_recite_count, group_count, study_model=1):
        """结果页处理"""
        if self.wait_check_result_page():
            print('进入结果页面')
            self.check_result_word_data(new_word_count, new_explain_words_count,
                                        already_recite_count, group_count)   # 结果页元素
            self.share_button()  # 打卡
            group_num = 6 if study_model == 1 else 9
            GameCommonEle().share_page_operate()  # 炫耀一下页面
            if self.wait_check_result_page():
                self.more_again_button()  # 再练一次
                if group_count == group_num:
                    if not self.wait_check_study_times_limit_page():
                        self.base_assert.except_error('练习次数已达到顶峰值， 未显示练完提示页面')
                    else:
                        print('你已练完今日单词， 保持适度才能事半功倍哦！休息一下，明天再练吧')
                if self.wait_check_next_grade():  # 继续挑战页面
                    self.level_up_text()
                    self.confirm_button().click()


