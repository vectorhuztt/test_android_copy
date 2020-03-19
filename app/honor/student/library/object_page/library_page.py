# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/26 15:55
# -------------------------------------------
import re
import time

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.library.object_page.library_h5_page import H5SharePage
from app.honor.student.login.object_page.home_page import HomePage
from conf.decorator import teststep, teststeps
from utils.toast_find import Toast


class LibraryPage(LibraryGamePage):
    def __init__(self):
        super().__init__()
        self.h5_page = H5SharePage()

    @teststep
    def wait_check_library_page(self, school_name):
        """图书馆页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"{}-图书馆")]'.format(school_name))
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_test_label_page(self, label_name):
        """测试标签页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[@text="{}"]'.format(label_name))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_test_book_page(self, book_name):
        """测试图书页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@resource-id, "book_name") and @text="{}"]'.format(book_name))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_end_tip_page(self):
        """到底了页面提示检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"到底啦 下拉刷新试试")]')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_no_data_reload_page(self):
        """重现加载页面检查点"""
        locator = (By.ID, self.id_type() + 'status_error_hint_view')
        return self.get_wait_check_page_result(locator, timeout=5)


    @teststep
    def course_more_btn(self, course_type):
        """每种图书下的查看更多按钮"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@resource-id, "hint_text") and @text="{}"]/'
                                                'following-sibling::android.widget.TextView'.format(course_type))
        return ele

    @teststep
    def label_name(self):
        """图书标签名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'hint_text')
        return ele

    # 书籍页面元素
    @teststep
    def wait_check_book_page(self):
        """书单等待页面"""
        locator = (By.ID, self.id_type() + 'book_title')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def book_names(self):
        """图书名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'book_name')
        return ele

    @teststep
    def book_title(self):
        """书单标题"""
        ele = self.driver.find_element_by_id(self.id_type() + 'book_title')
        return ele.text

    @teststep
    def book_set_num(self):
        """图书统计"""
        ele = self.driver.find_element_by_id(self.id_type() + 'book_num')
        return ele.text

    @teststep
    def book_summary(self):
        """书单描述"""
        ele = self.driver.find_element_by_id(self.id_type() + 'book_summary')
        return ele.text

    @teststep
    def test_book(self, book_name):
        """测试书籍"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@resource-id, "book_name") '
                                                'and @text="{}"]'.format(book_name))
        return ele

    @teststep
    def get_book_process_by_name(self, book_name):
        """根据书单名称获取书单进度"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="{}"]/../following-sibling::android.widget.RelativeLayout//'
                                                'android.widget.TextView'.format(book_name))
        return ele.text

    # 书单页面
    @teststep
    def wait_check_book_set_page(self):
        """书单页面检查点"""
        locator = (By.ID, self.id_type() + 'sign')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_no_rank_page(self):
        locator = (By.ID, self.id_type() + 'no_rank')
        return self.get_wait_check_page_result(locator, timeout=5)

    def wait_check_user_name_page(self, nickname):
        """检查图书页面是否存在用户名"""
        locator = (By.XPATH, '//android.widget.TextView[@resource-id="{}name" and @text="{}"]'.format(self.id_type(), nickname))
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def punch_share_btn(self):
        """立即打卡按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sign')
        return ele

    @teststep
    def share_btn(self):
        """分享按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'share')
        return ele

    @teststep
    def user_process(self, nickname):
        """学生本书单的进度"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id="{}name" and @text="{}"]/following-sibling::'
                                                'android.widget.LinearLayout//android.widget.TextView'
                                                '[contains(@resource-id, "progress_num")]'.format(self.id_type(), nickname))
        return ele.text


    @teststep
    def user_like_btn(self, nickname):
        """学生排行点赞按钮"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id="{}name" and @text="{}"]/following-sibling::'
                                                'android.widget.TextView[contains(@resource-id, "like")]'.format(self.id_type(), nickname))
        return ele

    @teststep
    def start_study_button(self):
        """开始/继续学习按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sign_bottom')
        return ele

    @teststeps
    def select_test_book_operate(self, test_book_name):
        """书单页面处理"""
        if self.wait_check_book_page():
            print('图书名称：', self.book_title())
            print('图书统计：', self.book_set_num())
            description = self.book_summary()
            print('图书简介：', description)
            while not self.wait_check_test_book_page(test_book_name):
                self.screen_swipe_left(0.5, 0.9, 0.5, 1000)
            try:
                book_process = self.get_book_process_by_name(test_book_name)
            except:
                book_process = 0
            self.test_book(test_book_name).click()
            return book_process, description

    @teststep
    def bookset_page_operate(self, book_process, nickname, today_has_studied):
        if self.wait_check_book_set_page():
            print('书单名称：', self.book_title())
            book_summary = self.book_summary()
            print('书单简介：', book_summary)
            book_count = int(re.findall(r'\d+', book_summary)[0])
            no_speak_tip = False
            like_num = 0
            has_nickname = False
            if book_process == '0%':
                if self.wait_check_no_rank_page():
                    print('暂无排行')
                else:
                    while True:
                        if self.wait_check_user_name_page(nickname):
                            has_nickname = True

                        if self.wait_check_end_tip_page():
                            break
                        else:
                            self.screen_swipe_up(0.5, 0.9, 0.6, 1000)
                    if has_nickname:
                        self.base_assert.except_error('当前用户图书书单进度为0%, 但在书单中排行出现')
            else:
                if self.wait_check_no_rank_page():
                    self.base_assert.except_error('书单进度不为0, 排行榜为空')
                else:
                    while not self.wait_check_user_name_page(nickname):
                        self.screen_swipe_up(0.5, 0.9, 0.6, 1000)
                    user_process = self.user_process(nickname)
                    if book_process != user_process:
                        self.base_assert.except_error('书单进度与当前用户进度不一致')

                    user_like_btn = self.user_like_btn(nickname)
                    if user_like_btn.get_attribute('selected') == 'true':
                        user_like_btn.click()
                        if Toast().find_toast('一天内不可以重复点赞哦！'):
                            print('一天内不可以重复点赞哦')
                    else:
                        before_like_num = user_like_btn.text
                        user_like_btn.click()
                        if self.user_like_btn(nickname).text != str(int(before_like_num) + 1):
                            self.base_assert.except_error('点击可点击点赞按钮之后, 点赞个数未增加')
                        # like_num = self.user_like_btn(nickname).text

            self.punch_share_btn().click()
            if today_has_studied:
                if self.wait_check_share_area_page():
                    GameCommonEle().share_page_operate()
                else:
                    self.base_assert.except_error('本日已有做题记录，点击立即打卡未出现分享页面')
                    self.click_back_up_button()
            else:
                if self.wait_check_share_area_page():
                    self.base_assert.except_error('本日没有有做题记录，点击立即打卡出现分享页面')
                if self.wait_check_no_data_reload_page():
                    print('先看书， 再打卡')
                self.click_back_up_button()
            return no_speak_tip, like_num, book_count


    @teststeps
    def from_bank_back_to_home_operate(self, school_name):
        """从书籍大题页面返回主页面"""
        if self.wait_check_book_set_page():
            self.click_back_up_button()
            if self.wait_check_book_page():
                self.click_back_up_button()
                if self.wait_check_top_name_page('其他'):
                    self.click_back_up_button()
                    if self.wait_check_library_page(school_name):
                        HomePage().click_tab_hw()



