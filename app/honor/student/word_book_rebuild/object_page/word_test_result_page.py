#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/11/1 10:25
# -----------------------------------------
import json
import re
from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.library.object_page.game_page import LibraryGamePage
from app.honor.student.word_book_rebuild.object_page.word_rebuild_sql_handler import WordDataHandlePage
from app.honor.student.word_book_rebuild.object_page.word_test_sql_handler import WordTestSqlHandler
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.dict_slice import dict_slice


class WordTestResultPage(BasePage):

    def __init__(self):
        self.sql_handler = WordTestSqlHandler()

    @teststep
    def wait_check_test_result_page(self):
        """测试结果页面检查点"""
        locator = (By.ID, self.id_type() + 'head')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_again_btn_page(self):
        locator = (By.ID, self.id_type() + 'again')
        return self.get_wait_check_page_result(locator)

    @teststep
    def student_test_id(self):
        """当前测试id"""
        ele = self.driver.find_element_by_id(self.id_type() + 'head')
        test_id = json.loads(ele.get_attribute('contentDescription'))['test_id']
        return test_id

    @teststep
    def result_score(self):
        """结果得分"""
        ele = self.driver.find_element_by_id(self.id_type() + "score")
        return int(ele.text)

    @teststep
    def nickname(self):
        """用户名称"""
        ele = self.driver.find_element_by_id(self.id_type() + "name")
        return ele.text

    @teststep
    def test_count_summery(self):
        """测试总数总结"""
        ele = self.driver.find_element_by_id(self.id_type() + "word_num")
        return ele.text

    @teststep
    def test_record_summery(self):
        """测试记录总结"""
        ele = self.driver.find_element_by_id(self.id_type() + "record")
        return ele.text

    @teststep
    def share_btn(self):
        """打卡按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "clock")
        return ele

    @teststep
    def wrong_again_btn(self):
        """错题再练按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "again")
        return ele

    @teststep
    def result_back_btn(self):
        """结果页后退按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "back")
        return ele

    @teststep
    def db_cal_fvalue_dict_operate(self, stu_id,  word_dict, game_return, is_right=True):
        """单词结果页F值计算结果与从数据库获取结果进行对比
            :param stu_id:  学生id
            :param is_right:  是否是正确单词列表
            :param game_return: 游戏次数 0 首次测试 >0: 错题再练
            :param word_dict: 比较的单词字典
            :return cal_dict: F值变化后的dict
        """
        cal_dict, db_dict = {}, {}
        for x in word_dict:
            cal_dict[x] = []
            db_dict[x] = []
            for y in word_dict[x]:
                fvalue = self.sql_handler.get_fvalue_by_word_explain_id(stu_id, int(x), y[0])
                db_dict[x].append((y[0], fvalue))

                if is_right:
                    if y[1] < 5:
                        cal_dict[x].append((y[0], y[1]+1))
                    else:
                        cal_dict[x].append((y[0], y[1]))
                else:
                    if y[1] == 5 and game_return >= 1:
                        cal_dict[x].append((y[0], y[1] - 1))
                    else:
                        cal_dict[x].append((y[0], y[1]))
        print('F值计算结果：', cal_dict)
        print('F值db结果：', db_dict)
        if cal_dict != db_dict:
            self.base_assert.except_error('结果页F值计算结果与数据库结果不一致')


    @teststep
    def star_score_check_operate(self, stu_id, pass_word_list, wrong_word_list):
        """星星积分核对操作
            :param stu_id: 学生id
            :param pass_word_list: 测试通过单词列表
            :param wrong_word_list: 测试未通过单词列表
        """
        star_score_result = self.sql_handler.get_student_test_star_score(stu_id)
        cal_score_value = sum([len(pass_word_list[x]) for x in pass_word_list])
        cal_star_value = sum([len(wrong_word_list[x]) for x in wrong_word_list]) + cal_score_value

        if int(star_score_result['score']) != cal_score_value:
            self.base_assert.except_error("积分数与实际计算积分数不一致， 请核实。 student_data表数据为%d， 实际计算数据为%d" % (int(star_score_result['score']), cal_score_value))

        if int(star_score_result["star"]) != cal_star_value:
            self.base_assert.except_error("星星数量与实际计算星星数不一致， 请核实。 student_data表数据为%d， 实际计算数据为%d" % (int(star_score_result['star']), cal_star_value))

    @teststeps
    def check_result_page_data_operate(self, stu_id, nickname, test_word_dict, wrong_count, game_return):
        """结果页面数据校验
           :param game_return: 做题次数
           :param wrong_count:  错误单词个数
           :param test_word_dict: 测试单词字典信息
           :param stu_id:  学生id
           :param nickname:  学生昵称
        """
        if self.wait_check_test_result_page():
            test_count = len(test_word_dict)
            page_score = self.result_score()
            print('测试得分：', page_score, '\n',
                  '学生名称：', self.nickname(), '\n',
                  self.test_count_summery(), '\n',
                  self.test_record_summery())

            wrong_word_list = dict_slice(test_word_dict, end=wrong_count)
            pass_word_list = dict_slice(test_word_dict, start=wrong_count)

            print('错误单词：', wrong_word_list)
            print('正确单词：', pass_word_list)
            self.db_cal_fvalue_dict_operate(stu_id, wrong_word_list, game_return, is_right=False)
            self.db_cal_fvalue_dict_operate(stu_id, pass_word_list, game_return, is_right=True)

            test_id = self.student_test_id()
            db_result_data = self.sql_handler.get_result_data(test_id)

            db_right_count = db_result_data[0]
            db_total_count = db_right_count + db_result_data[1]

            db_score = int(db_result_data[3])

            split_time = db_result_data[2].split(':')
            db_spend_time = int(split_time[0] * 60) + int(split_time[1]) + (1 if int(split_time[2]) >= 30 else 0)
            pass_count = 0 if db_score < 90 else db_right_count

            if db_score != page_score:
                self.base_assert.except_error('测试分数与计算分数不一致，应为%d, 页面为%d' % (db_score, page_score))

            if self.nickname() != nickname:
                self.base_assert.except_error("当前页面昵称与设置中昵称不一致")

            word_count = int(re.findall(r'\d+', self.test_count_summery())[0])
            if db_total_count != word_count:
                self.base_assert.except_error("页面统计测试总数与实际个数不一致， 页面为%d，实际为%d" % (word_count, test_count))

            record_info = re.findall(r'\d+', self.test_record_summery())
            studied_words_count = WordDataHandlePage().get_student_studied_words_count(stu_id)
            if studied_words_count != int(record_info[0]):
                self.base_assert.except_error("页面已背单词个数与实际已背数量不一致， 页面为%d, 实际为%d" % (int(record_info[0]), studied_words_count))

            if pass_count != int(record_info[1]):
                self.base_assert.except_error("页面测试通过单词个数与实际通过数量不一致， 页面为%d, 实际为%d" % (int(record_info[1]), pass_count))

            if db_spend_time != int(record_info[2]):
                self.base_assert.except_error("页面统计时间与实际用时不一致，页面为%d， 实际为%d" % (int(record_info[2]), db_spend_time))

            self.star_score_check_operate(stu_id, pass_word_list, wrong_word_list)

            if page_score == 100:
                if self.wait_check_again_btn_page():
                    self.base_assert.except_error("得分为100分， 但是错题再练可点击")

            self.share_btn().click()
            GameCommonEle().share_page_operate()
            return wrong_word_list







