#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/12/27 9:12
# -----------------------------------------
import random

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.homework_rebuild.object_pages.homework_game_page import HomeworkGameOperate
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.punch_activity.object_page.punch_sql_handle import PunchSqlHandle
from conf.base_page import BasePage
from conf.decorator import teststep
from utils.toast_find import Toast


class PunchActivityPage(BasePage):
    def __init__(self):
        self.library = LibraryGamePage()

    @teststep
    def wait_check_alert_punch_tip_page(self):
        locator = (By.XPATH, '//android.widget.ImageView[contains(@content-desc, "21天打卡活动")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_home_punch_notice_page(self):
        """主页的打卡提示页面检查点"""
        locator = (By.XPATH, '//android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_activity_book_item_page(self):
        """打卡页面检查点"""
        locator = (By.ID, self.id_type() + 'activitie_book_item')
        return self.get_wait_check_page_result(locator, timeout=10)

    @teststep
    def wait_check_class_list_page(self):
        """班级列表页面检查点"""
        locator = (By.CLASS_NAME, 'android.widget.ListView')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_punch_lock_icon_page(self, book_id):
        """打卡锁图标检查点"""
        locator = (By.XPATH, '//android.widget.TextView[@content-desc="{}"]/following-sibling::'
                             'android.widget.ImageView[@index="3"]'.format(book_id))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_select_checkpoint_page(self):
        """选择关卡页面检查点"""
        locator = (By.ID, self.id_type() + 'progress_topic')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_share_tip_page(self):
        """炫耀一下按钮提示页面检查点"""
        locator = (By.XPATH, '//*[contains(@text, "“炫耀一下”才算完成任务呦~")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_checkpoint_continue_tip_by_index_page(self, index):
        """关卡继续提示页面检查点"""
        locator = (By.XPATH, '//android.support.v7.widget.RecyclerView/android.view.ViewGroup[@index="{}"]/'
                             'android.widget.ImageView[contains(@resource-id, "tit")]'.format(index))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_page_has_continue_tip_page(self):
        """检查关卡页面是否存在继续按钮"""
        locator = (By.XPATH, '//android.support.v7.widget.RecyclerView/android.view.ViewGroup/'
                             'android.widget.ImageView[contains(@resource-id, "tit")]')
        return self.get_wait_check_page_result(locator)


    @teststep
    def click_alert_tip(self):
        """点击弹出的打卡页面"""
        self.driver.find_element_by_xpath('//*[@resource-id="android:id/content"]/'
                                          'android.view.ViewGroup/android.widget.ImageView').click()

    @teststep
    def home_page_punch_tab(self):
        """主页进入打卡页面的tab"""
        ele = self.driver.find_element_by_xpath('//android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]')
        return ele

    @teststep
    def change_class_btn(self):
        """切换班级按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'spinner_bar')
        return ele

    @teststep
    def class_list(self):
        """班级列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'spinner_bar_item')
        return ele

    @teststep
    def activity_title(self):
        """活动名称"""
        ele = self.driver.find_element_by_id(self.id_type() + 'activity_title')
        return ele.text

    @teststep
    def punch_books(self):
        """打卡列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'entry_tv')
        return ele

    @teststep
    def punch_book_status(self, book_id):
        """打卡书籍状态"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@content-desc="{}"]/preceding-sibling::'
                                                'android.widget.ImageView[contains(@resource-id, "activitie_book_item")]'.format(book_id))
        return self.attr.get_cont_desc(ele)

    @teststep
    def punch_book_id(self, index):
        """获取图书id"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'entry_tv')
        return self.attr.get_cont_desc(ele[index])

    @teststep
    def punch_page_back_icon(self):
        """打卡页面退出按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'back_but')
        return ele

    @teststep
    def checkpoint_list(self):
        """关卡列表"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'selector_circle_tv')
        return ele

    @teststep
    def share_btn(self):
        """炫耀一下按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'progress_topic')
        return ele
    
    @teststep
    def checkpoint_core_process(self, stu_id, activity_class_info):
        if not self.wait_check_activity_book_item_page():
            self.base_assert.except_error("从主页点击打卡tab未进入打卡页面")
        else:
            self.change_class_btn().click()
            if self.wait_check_class_list_page():
                class_list = self.class_list()
                for x in class_list:
                    class_id = self.attr.get_cont_desc(x)
                    print('班级：', x.text, '班级id：', class_id)
                    if class_id not in list(activity_class_info.keys()):
                        self.base_assert.except_error('查询本班级不存在打卡活动， 但是该班级名称出现在打卡班级列表中')
                random_index = random.randint(0, len(class_list) - 1)
                select_class = self.class_list()[random_index]
                select_class_id = self.attr.get_cont_desc(select_class)
                class_punch_info = activity_class_info[select_class_id]
                select_activity_id = class_punch_info['活动id']
                select_class.click()
                if not self.wait_check_activity_book_item_page():
                    self.base_assert.except_error('选择班级后未进入打卡页面')
                else:
                    page_activity_name = self.activity_title()
                    if class_punch_info['活动名称'] != page_activity_name:
                        self.base_assert.except_error("页面展示的活动名称与查询名称不一致")
                    if len(self.punch_books()) != len(class_punch_info['书籍信息']):
                        self.base_assert.except_error('页面展示的书籍个数与查询所得个数不一致')
                PunchSqlHandle().delete_student_activity_record(stu_id, select_activity_id)
                return class_punch_info['书籍信息']

    @teststep
    def punch_page_select_book_operate(self, book_info, nickname):
        """打卡页面书籍选择"""
        punch_books = self.punch_books()
        print('书籍个数：', len(punch_books))
        book_id_info = {}
        for i, x in enumerate(punch_books):
            quoted_id = self.attr.get_cont_desc(x)
            book_id = PunchSqlHandle().get_activity_book_id_by_quoted_id(quoted_id)
            book_id_info[quoted_id] = book_id
            if int(book_id) not in list(book_info.keys()):
                self.base_assert.except_error('此书不应在打卡书籍列表中')
            book_status = self.punch_book_status(quoted_id)
            if book_status == '0':
                if not self.wait_check_punch_lock_icon_page(quoted_id):
                    self.base_assert.except_error('图书状态不可点击， 但未发现解锁锁图标')
                x.click()
                if not Toast().find_toast('今天的书已经读完啦'):
                    self.base_assert.except_error('点击未解锁图书， 未弹出提示')
        select_quoted_id = self.punch_book_id(index=0)
        select_book_id = book_id_info[select_quoted_id]
        book_count = book_info[select_book_id]
        self.punch_books()[0].click()
        if not self.wait_check_select_checkpoint_page():
            self.base_assert.except_error('点击已解锁书籍， 未进入通关页面')
        else:
            if len(self.checkpoint_list()) != book_count:
                self.base_assert.except_error('关卡个数与数据查询个数不一致')
            if len(self.checkpoint_list()) > 10:
                self.base_assert.except_error('关卡个数大于10个')
        return select_quoted_id

    @teststep
    def checkpoint_page_operate(self, nickname, quoted_id):
        for x in range(len(self.checkpoint_list())):
            before_progress = self.attr.get_cont_desc(self.share_btn())
            print('进入关卡前的进度：', before_progress)
            self.checkpoint_list()[x].click()
            if self.library.wait_check_game_page():
                self.library.play_book_games(fq=1, half_exit=True)
            if self.wait_check_select_checkpoint_page():
                if not self.wait_check_checkpoint_continue_tip_by_index_page(x):
                    self.base_assert.except_error('关卡中途退出, 未发现继续学习图标')
            if self.attr.get_cont_desc(self.share_btn()) != before_progress:
                self.base_assert.except_error('中途退出后，书籍打卡进度发生变化')

            self.checkpoint_list()[x].click()
            if self.library.wait_check_game_page():
                HomeworkGameOperate().homework_game_operate(nickname, judge_score=False, is_activity=True)
                if not self.wait_check_select_checkpoint_page():
                    self.click_back_up_button()
                    self.library.result.all_game.word_spell.tips_operate()

            if self.wait_check_select_checkpoint_page():
                if self.wait_check_checkpoint_continue_tip_by_index_page(x):
                    self.base_assert.except_error('已全部做完其中之一关卡内部所有题, 依然继续学习图标')
            if self.attr.get_cont_desc(self.share_btn()) == before_progress:
                self.base_assert.except_error('已全部做其中之一完关卡内部所有题，书籍打卡进度未发生变化')

        if self.wait_check_select_checkpoint_page():
            if self.attr.get_cont_desc(self.share_btn()) != '100':
                self.base_assert.except_error('已经完成所有关卡， 进入不为100')
            self.punch_page_back_icon().click()
            if self.wait_check_activity_book_item_page():
                book_status = self.punch_book_status(quoted_id)
                if book_status == '0':
                    self.base_assert.except_error('关卡全部通过， 但是未点击分享按钮，图书状态不为未完成')
                self.punch_books()[0].click()
            if self.wait_check_select_checkpoint_page():
                self.share_btn().click()
                GameCommonEle().share_page_operate()
                if self.wait_check_select_checkpoint_page():
                    self.punch_page_back_icon().click()
            if self.wait_check_activity_book_item_page():
                book_status = self.punch_book_status(quoted_id)
                if book_status != '1':
                    self.base_assert.except_error('关卡全部通过， 已点击分享按钮，图书状态不为已完成')












