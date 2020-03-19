#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute


class ResultPage(BasePage):
    """结果页"""
    @teststeps
    def wait_check_result_page(self, var=20):
        """以“title:排行榜”的ID为依据"""
        locator = (By.ID, self.id_type() + "rank")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def correct_rate(self):
        """准确率"""
        rate = self.driver\
            .find_element_by_id(self.id_type() + "correct_rate").text
        return rate

    @teststep
    def result_score(self):
        """积分"""
        score = self.driver \
            .find_element_by_id(self.id_type() + "score").text
        return score

    @teststep
    def result_star(self):
        """星星"""
        star = self.driver \
            .find_element_by_id(self.id_type() + "star").text
        return star

    @teststep
    def result_time(self):
        """时间"""
        ele = self.driver.find_element_by_id(self.id_type() + "time")
        value = re.sub("\D", "", ele.text)
        return value

    @teststep
    def rank(self):
        """title: 排行榜"""
        rank = self.driver\
            .find_element_by_id(self.id_type() + "rank").text
        return rank

    @teststep
    def rank_menu(self):
        """排行榜下拉按钮"""
        self.driver\
            .find_element_by_id("android:id/text1").click()
        time.sleep(1)

    @teststep
    def rank_menu_item(self):
        """排行榜下拉菜单"""
        item = self.driver.find_elements_by_id("android:id/text1")
        time.sleep(1)
        return item

    # 以下为排行榜list内容
    @teststep
    def rank_index(self):
        """排名"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "index")
        return item

    @teststep
    def rank_name(self):
        """学生昵称"""
        time.sleep(1)
        item = self.driver \
            .find_elements_by_id(self.id_type() + "name")
        return item

    @teststep
    def rank_accuracy_rate(self):
        """准确率最高的那次的正确率"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "rate")
        return item

    @teststep
    def rank_spend_time(self):
        """准确率最高的那次 完成所用时间"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "time")
        return item

    @teststep
    def check_result_button(self):
        """查看答案按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "detail") \
            .click()

    # 以下为查看答案页面元素
    @teststeps
    def wait_check_detail_page(self):
        """title:查看答案"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'查看答案')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def mine_result(self):
        """查看答案 页面每个小题后面 对错标识"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "iv_mine")
        value = GetAttribute().get_selected(item)
        return value

    @teststep
    def error_again_button(self):
        """错题再练按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "again") \
            .click()
        time.sleep(1)

    @teststep
    def again_button(self):
        """错题再练/再练一遍按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "again") \
            .click()

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class name为依据"""
        time.sleep(1)
        self.driver \
            .find_element_by_class_name("android.widget.ImageButton").click()

    @teststeps
    def back_up(self):
        """返回到作业list"""
        time.sleep(1)
        j = 0
        while j < 2:
            self.back_up_button()  # 结果页 返回按钮
            j += 1

    @teststeps
    def result_page_correct_rate(self, count, rate):
        """结果页结果统计 -- 准确率"""
        print('进入结果页')
        if self.wait_check_result_page():  # 结果页检查点
            if len(count) != 0:  # 答对的题数
                correct_rate = re.findall(r"\d+", self.correct_rate())[0]  # 本次结果统计——准确率

                num = len(count) * 100 / int(rate)
                accuracy_rate = int(num) + int("%.f" % (num - int(num)))  # 根据答题情况 计算准确率

                print('统计结果:', accuracy_rate)
                if int(correct_rate) == accuracy_rate:
                    print("准确率逻辑无误 - 答对%s题 准确率:%s" % (len(count), correct_rate + '%'))
                else:
                    print("❌❌❌ Error 准确率逻辑有误 - 答对%s题 但准确率为:%s" % (len(count), correct_rate + '%'))
                    # MyError(self.driver).my_error(int(correct_rate) != accuracy_rate)
            else:
                print("答对0题 准确率为:0%")
            print('==================================================')

    @teststeps
    def result_page_score(self, questions):
        """结果页结果统计 -- 积分"""
        print('进入结果页')
        if self.wait_check_result_page():  # 结果页检查点
            score = re.sub("\D", "", self.result_score())  # 本次结果统计——积分

            if int(score) == questions:
                print("积分逻辑无误 - 答对%s题 积分:%s" % (questions, score))
            else:
                print("❌❌❌ 积分逻辑有误 - 答对%s题 但积分为:%s" % (questions, score))
                # MyError(self.driver).my_error(int(score) != len(questions))

            print('==================================================')
        return questions

    @teststeps
    def result_page_star(self, questions):
        """结果页结果统计 -- 星星"""
        print('进入结果页')
        if self.wait_check_result_page():  # 结果页检查点
            star_count = re.sub("\D", "", self.result_star())  # 本次结果统计——星星

            if questions == int(star_count):
                print("星星逻辑无误 - 做了%s题 星星数:%s" % (questions, star_count))
            else:
                print("❌❌❌ 星星逻辑有误 - 做了%s题 但星星数为:%s" % (questions, star_count))
                # MyError(self.driver).my_error(int(rate) != int(star_count))

            print('==================================================')
            return star_count

    @teststeps
    def result_page_time(self, now, button=''):
        """结果页结果统计 -- 所用时间"""
        print('进入结果页')
        if self.wait_check_result_page():  # 结果页检查点
            result_time = self.get_time(self.result_time())  # 本次结果统计——所用时间
            print('result_time:', result_time, now)
            if button != '错题再练按钮':
                if now == result_time:
                    print("本次答题所用时间:", result_time)
                elif now < result_time:
                    print("本次答题所用时间:%s秒, 时间差为：%s秒" % (result_time, result_time - now))
                else:
                    print("❌❌❌ 时间逻辑有误 - 做题页面时间为 %s 结果页统计时间为:%s" % (now, result_time))
                    # MyError(self.driver).my_error(now > result_time)
            else:  # 错题再练
                if now == result_time:
                    print("本次答题所用时间：", result_time)
                elif result_time - now <= 2:
                    print("本次答题所用时间：%s秒 时间差为:%s秒 " % (result_time, result_time - now))
                else:
                    print("❌❌❌ 时间逻辑有误 - 做题页面时间为 %s 结果页统计时间为:%s" % (now, result_time))
                    # MyError(self.driver).my_error(now > result_time)
            print('==================================================')
            return result_time

    @teststeps
    def result_page_ranking(self, nickname):
        """结果页结果统计 -- 排行榜"""
        index = []
        optimal_rate = []  # 最优准确率
        optimal_time = []  # 最优准确率所用时间
        if self.wait_check_result_page():  # 结果页检查点
            # 本次结果统计——准确率、积分、星星、所用时间
            correct_rate = re.findall(r"\d+", self.correct_rate())[0]
            now_time = self.get_time(self.result_time())  # 本次结果统计——所用时间 不带格式

            self.rank_menu()  # 结果页 排行榜下拉菜单
            item = self.rank_menu_item()
            for j in range(len(item)):  # 班级切换
                self.rank_menu_item()[j].click()  # 结果页 切换不同班级排行榜

                rank_name = self.rank_name()  # 排行榜list条目比较
                rank_index = self.rank_index()
                for i in range(len(rank_name)):
                    rank_rate = re.sub("\D", "", self.rank_accuracy_rate()[i].text)  # 准确率
                    spend_time = self.rank_spend_time()[i+1].text
                    rank_time = self.get_time(spend_time)  # 排行榜不带格式的时间 xxxx
                    # i+1的原因是排行榜的时间与右上角本次所用时间resource—id相同
                    mat = re.search(r"(\d{1,2}:\d{1,2})", spend_time)  # 排行榜带格式的时间 xx:xx

                    if rank_name[i].text == nickname and len(rank_name) != 1:  # 排行榜不只有自己
                        print(correct_rate, rank_rate)
                        if correct_rate == rank_rate:  # 将本次成绩与排行榜中最优成绩作比较-相等
                            if now_time < rank_time:  # 成绩相等时 比较时间
                                print('本次用时较短 Congratulations')
                            elif now_time == rank_time:
                                print('本次准确率、所用时间与之前成绩持平  Fighting')
                            else:
                                print('本次用时较长 Fighting')
                        elif correct_rate < rank_rate:
                            print('本次成绩非最优 Fighting')
                        else:
                            print('❌❌❌ 排行榜逻辑有问题 - 成绩相等时,比较时间')
                            # MyError(self.driver).my_error(correct_rate > rank_rate)
                        print('排行榜成绩 - 排名、昵称、准确率、所用时间:', rank_index[i].text, rank_name[i].text, rank_rate+'%', mat.group(0))
                    elif len(rank_name) == 1:  # 排行榜只有自己
                        print('排行榜只有自己， 成绩为 - 昵称、准确率、所用时间:', rank_name[i].text, rank_rate+'%', mat.group(0))

                    index.append(rank_index[i].text)
                    optimal_rate.append(rank_rate)
                    optimal_time.append(rank_time)

                if j != len(item)-1:
                    self.rank_menu()  # 结果页 排行榜下拉菜单
        else:
            print('未进入结果页')

        print('==================================================')

    def get_time(self, time_str):
        """将带有格式的时间（xx:xx）转换为int类型"""
        now = []
        var = re.sub("\D", "", time_str)
        # 小时
        if int(var[0]) != 0:
            now.append(60 * int(var[0]) * 10 + 60 * int(var[1]))
        else:
            now.append(60 * int(var[1]))

        # 分钟
        if int(var[2]) != 0:
            now.append(int(var[2])*10 + int(var[3]))
        else:
            now.append(int(var[3]))

        for i in range(len(now)):
            if i + 1 < len(now):
                now[0] += now[i + 1]

        return int(now[0])
