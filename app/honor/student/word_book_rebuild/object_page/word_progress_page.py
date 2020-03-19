import collections
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from conf.base_page import BasePage
from conf.decorator import teststep
from conf.base_config import GetVariable as gv


class ProgressPage(BasePage):
    def __init__(self):
        self.common = WordDataHandlePage()

    @teststep
    def wait_check_progress_page(self):
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'单词本进度')]")
        try:
            WebDriverWait(self.driver, 15, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_sys_label_page(self):
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'{}')]".format(gv.GRADE + ' （系统）'))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def word_progress_icon(self):
        """词书进度"""
        self.driver.\
            find_element_by_id(self.id_type() + 'word_statistics')\
            .click()

    @teststep
    def first_turn(self):
        """一轮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'first_time').text
        print(ele, end='，')

    @teststep
    def third_turn(self):
        """三轮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'three_time').text
        print(ele, end='，')

    @teststep
    def total(self):
        """总数"""
        ele = self.driver.find_element_by_id(self.id_type() + 'total').text
        print(ele)

    @teststep
    def label_name(self):
        """标签名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'name')
        return ele

    @teststep
    def word_statistics(self, name):
        """单词数据"""
        ele = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'{}')]/following-sibling::"
                                                "android.widget.TextView".format(name))
        return ele.text

    @teststep
    def find_pencil_icon(self):
        try:
            self.driver.find_element_by_id(self.id_type() + 'img')
            return True
        except:
            return False

    @teststep
    def get_word_homework_names(self, stu_id):
        """获取标签名称"""
        word_homework_id = self.common.get_all_word_homework_ids(stu_id)
        word_homework_names = [self.common.get_word_homework_name(x) for x in word_homework_id]
        return word_homework_names

    @teststep
    def progress_ele_check(self, stu_id):
        """页面元素打印"""
        print("\n----<词书进度页面>----\n")

        self.first_turn()  # 一轮
        self.third_turn()  # 三轮
        self.total()  # 总数

        label_name = self.get_word_homework_names(stu_id)  # 数据库标签名称
        label_info = collections.OrderedDict()
        while True:
            labels = self.label_name()  # 页面标签名
            for l in labels:
                statics = self.word_statistics(l.text)
                label_info[l.text] = statics
            if self.wait_check_sys_label_page():
                break
            else:
                self.screen_swipe_down(0.5, 0.9, 0.5, 2000)

        self.judge_studying_icon(list(label_info.keys()), label_name)  # 进行中 词书判断
        sys_labels = [x for x in list(label_info.keys()) if '系统' in x]
        no_revoke_sys_label = [x for x in sys_labels if '已撤销' not in x]
        if len(no_revoke_sys_label) != 0:
            if len(no_revoke_sys_label) != 1:
                print('❌❌❌ Error-- 有多个系统词书存在,未被撤销词书数量不为1', no_revoke_sys_label)

        key_list = list(map(lambda x: x[:-7] if '进行中' in x else x, list(label_info.keys())))
        word_book_list = list(map(lambda x: x[:-4] if '已撤销' in x else x, key_list))
        label_name.sort()
        word_book_list.sort()
        if label_name == word_book_list:
            print("词书标签与数据库一致")

            for label in list(label_info.keys()):
                word_data = label_info[label]
                count = re.findall(r'\d+', word_data)
                print(label, '\t', word_data)
                print('一轮单词数:', count[1], ' 三轮单词数:', count[0], ' 单词总数:', count[2], '\n')

                if '进行中' in label:
                    homework_name = label[:-7]
                elif '已撤销' in label:
                    homework_name = label[:-4]
                else:
                    homework_name = label

                homework_id = self.common.get_word_homework_id_by_name(homework_name)
                label_id = self.common.get_student_label_id_by_homework_id(stu_id, homework_id)
                word_list = self.common.get_wordbank_by_label_id(label_id)

                if int(count[2]) == len(word_list):
                    print('单词总数数验证正确')
                else:
                    print('❌❌❌ Error-- 总数与数据库数据不匹配', count[2])

                self.count_compare(stu_id, homework_id, int(count[1]), int(count[0]))
        else:
            print('❌❌❌ Error-- 词书标签与数据库不一致', word_book_list)

    @teststep
    def count_compare(self, stu_id, word_homework_id, first_count, third_count):
        """获取对应熟练度的单词数，并与页面数字比较"""
        count = self.common.get_words_count(stu_id, word_homework_id)  # 返回单词id 与单词熟练度
        if count[0] == first_count:
            print('一轮单词数验证正确')
        else:
            print('❌❌❌ Error-- 一轮单词数与数据库不匹配')

        if count[1] == third_count:
            print('三轮单词数验证正确')
        else:
            print('❌❌❌ Error-- 三轮单词数与数据库不匹配')

        print('----------------------------------\n')

    @teststep
    def judge_studying_icon(self, label_info_keys, label_name):
        doing_word_book = [x for x in label_info_keys if '进行中' in x]
        if len(doing_word_book) == 1:
            if doing_word_book[0][:-7] == label_name[-1]:
                print('正在练习的词书核实正确', doing_word_book[0][:-7], '\n')
            else:
                print('❌❌❌ Error-- 正在练习的词书与数据库不一致！', label_name[-1], '\n')
        else:
            print('❌❌❌ Error-- 正在练习的词书与不止一个！', doing_word_book, '\n')
