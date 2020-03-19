#!/usr/bin/env python
# encoding:UTF-8
# @Author  : SUN FEIFEI
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from app.honor.student.homework.object_page.result_page import ResultPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.raise_exception import MyError


class Homework(BasePage):
    """作业包内 作业列表页面 元素信息"""

    @teststeps
    def wait_check_hw_page(self):
        """以“作业”的class_name为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@resource-id,"
                             "'{}tv_homework_name')]".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_game_list_page(self, var):
        """以 小游戏的class_name为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, %s)]" % var)
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def homework_name(self, index):
        """抬头： 作业包的名称 、老师名 & 作业模式"""
        item = self.driver \
            .find_elements_by_class_name("android.widget.TextView")[index].text
        return item

    @teststep
    def homework_list(self):
        """作业名称"""
        ele = self.driver \
            .find_elements_by_id(self.id_type() + "tv_homework_name")
        return ele

    @teststep
    def games_type(self):
        """小游戏数目 """
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_testbank_type")
        return item

    @teststep
    def games_title(self):
        """小游戏title """
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_testbank_name")
        return item

    @teststep
    def tv_testbank_type(self, index):
        """小游戏类型"""
        item = self.driver\
            .find_elements_by_id(self.id_type() + "tv_testbank_type")[index].text
        return item

    @teststeps
    def tv_testbank_name(self, index):
        """小游戏模式--匹配小括号内游戏模式"""
        item = self.driver\
            .find_elements_by_id(self.id_type() + "tv_testbank_name")[index].text
        m = re.match(".*\（(.*)\）.*", item)  # title中有一个括号
        return m.group(1)

    @teststeps
    def tv_game_type(self, index):
        """小游戏模式--匹配小括号内游戏模式"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_testbank_name")[index].text
        m = re.match(".*\（(.*)\）.*\（", item)  # 有两个括号，匹配第二个
        return m.group(1)

    @teststep
    def status(self):
        """题目状态"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_testbank_status")
        return item

    @teststep
    def count(self):
        """题目总数格式：共X题"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_testbank_count")
        return item

    @teststep
    def rank_icon(self):
        """排行榜icon"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "iv_ranking")
        return item

    # 小键盘 右上角的 隐藏按钮
    @teststep
    def hide_button(self):
        """隐藏按钮 的resource-id"""
        self.driver \
            .find_elements_by_id(self.id_type() + "keyboard_hide")\
            .click()

    # 从结果页返回小游戏list
    def back_operate(self):
        """从结果页返回小游戏list"""
        if ResultPage().wait_check_result_page():
            self.back_up_button()  # 返回小游戏界面

    # 以下为排行榜页面元素
    @teststep
    def wait_check_rank_page(self):
        """以“title:排行榜”的ID为依据"""
        locator = (By.XPATH,  "//android.widget.TextView[contains(@text,'排行榜')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def no_data(self):
        """暂无数据"""
        time.sleep(2)
        item = self.driver \
            .find_elements_by_xpath("//android.widget.TextView[contains(@index,0)]")[1].text
        return item

    @teststep
    def class_name(self):
        """班级名称"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_title")
        return item

    @teststep
    def text_view(self):
        """所有排行榜TextView元素总数-包括班级名称+list条目"""
        item = self.driver \
            .find_elements_by_xpath("//android.support.v7.widget.RecyclerView/*/android.widget.TextView")
        return item

    @teststep
    def rank_index(self, index):
        """排名"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_index")[index].text
        return item

    @teststep
    def student_icon(self, index):
        """头像"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "iv_student_icon")[index].text
        return item

    @teststep
    def student_name(self, index):
        """学生昵称"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_student_name")[index].text
        return item

    @teststep
    def accuracy_rate(self):
        """准确率最高的那次的正确率"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_accuracy")
        return item

    @teststep
    def spend_time(self, index):
        """准确率最高的那次 完成所用时间"""
        item = self.driver \
            .find_elements_by_id(self.id_type() + "tv_spend_time")[index].text
        return item

    @teststep
    def back_up_button(self):
        """以“返回按钮”的class name为依据"""
        time.sleep(1)
        self.driver \
            .find_element_by_class_name("android.widget.ImageButton").click()

    # 公共元素 及操作
    @teststep
    def next_button_judge(self, var):
        """‘下一题’按钮 状态判断"""
        value = GetAttribute().get_enabled(self.next_button())
        if value != var:  # 测试 下一步 按钮 状态
            print('❌❌❌ 下一步按钮 状态Error', value)

    @teststep
    def rate(self):
        """获取作业数量"""
        rate = self.driver\
            .find_element_by_id(self.id_type() + "rate").text
        return rate

    @teststeps
    def swipe_screen(self, game_type):
        """小游戏页面滑屏"""
        self.screen_swipe_up(0.5, 0.75, 0.6539, 1000)  # 滑动后到底，因为小游戏list最多只有两页，滑动一次即可到底
        game_count = self.games_count(8, game_type)[0]
        return game_count

    @teststeps
    def games_count(self, index, game_type, title):
        """该类型小游戏的数量"""
        if self.wait_check_game_list_page(title):
            if game_type in ('连词成句', '阅读理解', '闪卡练习'):
                self.screen_swipe_up(0.5, 0.8, 0.1, 1000)

            item = self.games_type()  # 小游戏类型
            title = self.games_title()  # 页面内小游戏数目
            print('game_type:', game_type)
            count = []  # 小游戏数目
            for i in range(index, len(item)):
                var = self.tv_testbank_type(i)  # 获取小游戏类型
                if var == game_type:
                    count.append(i)
            print('小游戏：', count)
            print('---------------')
            return count, len(title)

    @teststeps
    def content(self):
        """小游戏条目展示内容"""
        title = []
        for i in range(2):
            title.append(self.homework_name(i))
        print('小游戏title内容:', title)

        count = self.games_type()
        for j in range(len(count)):
            game_type = self.tv_testbank_type(j)
            game_status = self.status()[j].text
            count = self.count()[j].text
            icon = self.rank_icon()[j]
            print('小游戏条目内容:', game_type, game_status, count, icon)

    # 以下为排行榜功能
    @teststeps
    def ranking(self, index, nickname):
        """排行榜icon"""
        status = self.status()[index].text
        print('题目状态：', status)

        self.rank_icon()[index].click()  # 点击排行榜icon
        if self.wait_check_rank_page():  # 排行榜页面检查点
            own_info = []
            class_name = self.class_name()  # 班级名称
            if self.no_data() == '暂无数据':
                print('排行榜目前暂无数据，当前所在班级为 %s' % class_name[0].text)
            else:
                for i in range(len(class_name)):
                    print('------------------------------')
                    print('班级：', class_name[i].text)
                    if status == '未开始':
                        self.ranking_no_start(class_name, nickname)  # 排行榜 昵称
                        break
                    else:
                        own_info.append(self.ranking_list(i, class_name, nickname))
                        break

            print('============================================')
            if self.wait_check_rank_page():  # 排行榜页面检查点
                self.back_up_button()  # 返回 游戏列表

            return own_info  # 返回值
        else:
            print('作业暂无排行清空')

    @teststeps
    def list_item(self, class_name):
        """排行榜list条目内容"""
        class_count = []  # 统计 第几个text_view 是班级
        text_view = self.text_view()  # 页面内所有text_view
        for j in range(len(class_name)):
            for i in range(len(text_view)):
                if text_view[i].text == class_name[j].text:
                    class_count.append(i)

        return class_count, text_view

    @teststeps
    def ranking_no_start(self, class_name, nickname):
        """题目状态：未开始"""
        for i in range(len(class_name)):
            rank_name = self.student_name(i)  # 昵称
            if rank_name == nickname:  # todo 未开始状态时，排行榜条目不应出现本人信息
                print('❌❌❌ Error--题目状态：未开始')
            else:
                print('题目状态：未开始 - no error')

    @teststeps
    def info_statistic(self, i, class_name):
        """名次、昵称、最优准确率、所用时间各生成一个list"""
        j = 0
        rank_index = []  # 排名
        rank_name = []  # 昵称
        rank_rate = []  # 最优准确率
        rank_time = []  # 所用时间 - 带格式 xx:xx
        mat = []  # 所用时间 - 不带格式 xxxx
        text = []  # 包含名次、昵称、最优准确率、所用时间 所有内容的一个大list

        # print('名次、昵称、最优准确率、所用时间各生成一个list:')
        info = self.list_item(class_name)
        if i+1 < len(class_name):  # 多于一个班级
            for index in range(info[0][i]+1, info[0][i+1]):
                text.append(info[1][index].text)
        else:  # 只有一个班级
            for index in range(info[0][i]+1, len(info[1])):
                text.append(info[1][index].text)

        while j < len(text):  # 名次、昵称、最优准确率、所用时间各生成一个list
            rank_index.append(text[j])
            rank_name.append(text[j + 1])
            rank_rate.append(re.sub("\D", "", text[j + 2]))  # 最优准确率
            rank_time.append(text[j + 3])  # 带格式的时间 xxxx
            mat.append(re.sub("\D", "", text[j + 3]))  # 不带格式的时间 xx:xx
            j += 4
        return rank_index, rank_name, rank_rate, rank_time, mat

    @teststeps
    def ranking_list(self, i, class_name, nickname):
        """排行榜列表的操作"""
        own_rate = []
        own_time = []
        item = self.info_statistic(i, class_name)
        for index in range(len(item[0])):
            if len(item[0]) > 1:  # 排行榜不只有一个人
                if item[1][index] == nickname:  # 本人
                    if index != 0:
                        if item[0][index] != 1:  # 说明不是第一名 - 排行榜不只有自己 且自己不是第一名，list第一条是自己的信息
                            print(item[0][index], item[1][index], item[2][index] + "%", item[3][index], '   本人成绩')
                        else:  # 是第一名
                            print('Congratulations排行榜排名第一   成绩：', item[2][index] + "%", item[3][index])
                        own_rate.append(item[2][index])
                        own_time.append(item[3][index])
                else:  # 排行榜其他人
                    if index == 0:
                        print('排行榜无本人，其他人成绩：')
                    print(item[0][index], item[1][index], item[2][index] + "%", item[3][index])
            elif len(item[0]) == 1:  # 排行榜只有一个人
                print('排行榜只有一个人:')
                if item[1][index] == nickname:  # 本人
                    print('本人成绩：', item[2][index] + "%", item[3][index])
                    own_rate.append(item[2][index])
                    own_time.append(item[3][index])
                else:
                    print('昵称: %s, 成绩：%s %s' % (item[1][index], item[2][index] + "%", item[3][index]))
            elif len(class_name) == 0:  # 排行榜暂无数据
                print('排行榜暂无数据')
            else:
                print('❌❌❌ Error - 排行榜')

        print('------------------------------')
        print('检查排行榜排序:', item[0], item[2], item[4])
        for z in range(len(item[0])):
            if len(item[0]) > 1:  # 排行榜不只有一个人
                if item[0][0] != 1:  # 不是第一名
                    if z != 0 and z+1 <= len(item[0])-1:  # 排除第一条信息
                        # print('不是第一名 且 排除第一条信息:', z, item[2][z], item[4][z])
                        self.check_ranking(z, item[2], item[4])
                else:    # 是第一名
                    if z+1 <= len(item[0])-1:
                        # print('是第一名:', z, item[2][z], item[4][z])
                        self.check_ranking(z, item[2], item[4])

        return own_rate, own_time, class_name

    @teststeps
    def check_ranking(self, j, rank_rate, rank_time):
        """排行榜排序逻辑检查"""
        if int(rank_rate[j]) > int(rank_rate[j + 1]):
            print('准确率高')
        elif int(rank_rate[j + 1]) == int(rank_rate[j]):  # 准确率相等
            if int(rank_time[j + 1]) > int(rank_time[j]):  # 比较时间
                print('所用时间短')
            elif int(rank_time[j + 1]) == int(rank_time[j]):
                print('准确率&所用时间均相同')
            else:
                print('❌❌❌ 排名逻辑有问题 - 所用时间', rank_time[j + 1], rank_time[j])
        else:
            print('❌❌❌ 排名逻辑有问题 - 准确率', rank_rate[j], rank_rate[j + 1])

    @teststeps
    def rate_judge(self, rate, i):
        """判断当前小题rate的值是否正确"""
        time.sleep(1)
        if int(self.rate()) != int(rate) - i:   # 测试当前rate值显示是否正确
            print('❌❌❌ Rate Error - 当前rate值为%s, 应为%s' % (int(self.rate()), int(rate) - i))

    @teststeps
    def next_button_operate(self, var):
        """下一步按钮 判断 加 点击操作"""
        self.next_button_judge(var)  # 下一题 按钮 状态判断
        self.next_button().click()  # 点击 下一题 按钮

    @teststeps
    def now_time(self, ele):
        """判断游戏界面 计时功能控件 是否在计时"""
        time.sleep(1)
        print('判断计时:', ele)
        time_list = []
        for i in range(len(ele)):
            time_list.append(ResultPage().get_time(ele[i]))
        if len(time_list) > 1:
            if any(time_list[i + 1] > time_list[i] for i in range(0, len(time_list) - 1)):
                print('计时功能无误:', time_list)
                return True
            else:
                print('❌❌❌ Error - 计时错误:', time_list)
                MyError(self.driver).my_error(any(time_list[i + 1] <= time_list[i] for i in range(0, len(time_list) - 1)))
        else:  # 只有一道题
            print('只有一道题，时间为:', time_list[0])
            return True
