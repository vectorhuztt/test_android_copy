import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book_rebuild.object_page.wordbook_rebuild_page import WordBookRebuildPage
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep
from utils.wait_element import WaitElement


class RankingPage(BasePage):
    """单词本 - 排行榜"""
    def __init__(self):
        self.home = HomePage()
        self.wait = WaitElement()

    @teststeps
    def wait_check_rank_page(self):
        """以“学生测试版”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'学生测试版')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def total(self):
        locator = (By.ID, self.id_type() + 'total')
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def click_rank_icon(self):
        """点击排行榜图标"""
        locator = (By.ID, self.id_type() + 'rank')
        self.wait.wait_find_element(locator).click()

    @teststep
    def choose_class(self):
        """班级展示 及切换"""
        locator = (By.ID, "android:id/text1")
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def classes_ele(self):
        """班级展示 及切换"""
        locator = (By.ID, "android:id/text1")
        return self.wait.wait_find_elements(locator)

    @teststep
    def word_num(self):
        """单词数"""
        locator = (By.ID, self.id_type() + "tv_score")
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def word_type(self):
        """wording:词"""
        locator = (By.ID, self.id_type() + "type")
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def share_button(self):
        """炫耀一下"""
        locator = (By.ID, self.id_type() + "share")
        self.wait.wait_find_element(locator).click()

    @teststep
    def rank_num(self):
        """班级排名"""
        locator = (By.ID, self.id_type() + "tv_ranking")
        ele = self.wait.wait_find_element(locator)
        return ele.text

    @teststep
    def order_num(self):
        """排名 数字"""
        locator = (By.ID, self.id_type() + "tv_order")
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_icon(self):
        """头像"""
        locator = (By.ID, self.id_type() + "iv_head")
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生姓名"""
        locator = (By.ID, self.id_type() + "tv_name")
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_score(self):
        """提示title"""
        locator = (By.ID, self.id_type() + "tv_score")
        return self.wait.wait_find_elements(locator)

    @teststep
    def students_name(self):
        """排行榜里学生名称"""
        locator = (By.XPATH, '//android.widget.RelativeLayout/android.widget.TextView'
                             '[contains(@resource-id, "{}tv_name")]'.format(self.id_type()))
        return self.wait.wait_find_elements(locator)


    @teststep
    def students_score(self):
        """排行榜中学生背的单词数"""
        locator = (By.XPATH, '//android.widget.RelativeLayout/android.widget.TextView'
                             '[contains(@resource-id,"{}tv_score")]'.format(self.id_type()))
        return self.wait.wait_find_elements(locator)

    # 炫耀一下
    @teststeps
    def wait_check_share_page(self):
        """以“title: 炫耀一下”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'炫耀一下')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def play_rank_word(self, total_word):
        print('排行榜 页面\n')
        self.choose_class()
        time.sleep(2)
        classes = self.classes_ele()
        for i in range(len(classes)):
            stu_class = self.classes_ele()[i].text
            self.classes_ele()[i].click()
            time.sleep(3)
            self.ele_operate(stu_class, total_word)
            if i != len(classes)-1:
                self.choose_class()
            else:
                print('排行榜浏览结束')
        WordBookRebuildPage().click_back_up_button()

    @teststep
    def ele_operate(self, stu_class, total_word):
        word_type = self.word_type()
        class_rank = self.rank_num()
        print('当前所在班级：', stu_class)
        score = self.st_score()[0].text
        print ('已背：', score + word_type)
        if int(score) != int(total_word):
            print('❌❌❌ Error - 次数与主页面单词数不一致！')
        else:
            print('单词数核实一致！')

        print('当前班级排名：', class_rank)
        self.share_button()
        if self.wait_check_share_page():
            self.home.click_back_up_button()
            if self.wait_check_rank_page():
                self.rank_numbers_info()

    def get_student_rank_info(self, students_info,i):
        student_names = self.students_name()
        student_scores = self.students_score()
        order = self.order_num()

        for j in range(len(student_names)):
            if i == 0:
                if j <= 2:
                    if order[i].text != '':
                        print('❌❌❌ Error - 名次位于第三名没有小皇冠标识')
            if student_names[j].text in students_info.keys():
                continue
            else:
                students_info[student_names[j].text] = student_scores[j].text
        return students_info

    @teststep
    def rank_numbers_info(self):
        students_info = {}
        student_names = self.students_name()
        if len(student_names) >= 6:
            for i in range(2):
                students_info = self.get_student_rank_info(students_info, i)
                self.home.screen_swipe_up(0.5, 0.8, 0.3, 1000)
        else:
            self.get_student_rank_info(students_info, i=0)
        self.home.screen_swipe_down(0.5, 0.2, 0.9, 1000)
        print("\n排行榜情况如下(只显示班级前10名 + 自己的名次)")
        for name in students_info.keys():
            score = students_info[name]
            print(name, '\t', score)
        time.sleep(3)
        print('----------------------------------')







