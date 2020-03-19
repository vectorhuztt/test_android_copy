# coding: utf-8
# -------------------------------------------
# Author:   Vector
# Date:     2019/3/28 13:13
# -------------------------------------------
import re

from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_init import AllGameClass
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class ResultPage(BasePage):
    def __init__(self):
        self.all_game = AllGameClass()

    @teststep
    def wait_check_result_page(self):
        """结果页面检查点"""
        locator = (By.ID, self.id_type()+'detail')
        return self.get_wait_check_page_result(locator, timeout=15)

    @teststep
    def wait_check_medal_page(self):
        """勋章页面检查点"""
        locator = (By.ID, self.id_type() + 'share_img')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_answer_page(self):
        """查看答案页面"""
        locator = (By.XPATH, '//*[@text="查看答案"]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def check_result_btn(self):
        """查看答案"""
        ele = self.driver.find_element_by_id(self.id_type() + 'detail')
        return ele

    @teststep
    def again_btn(self):
        """错题再练 再练一次按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'again')
        return ele

    @teststep
    def correct_rate(self):
        """正确率"""
        ele = self.driver.find_element_by_id(self.id_type() + 'correct_rate')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def score(self):
        """积分"""
        ele = self.driver.find_element_by_id(self.id_type() + 'score')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def star(self):
        """星星"""
        ele = self.driver.find_element_by_id(self.id_type() + 'star')
        return int(re.findall(r'\d+', ele.text)[0])

    @teststep
    def time(self):
        """时间"""
        ele = self.driver.find_element_by_id(self.id_type() + 'time')
        return ele

    @teststep
    def explains(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'explain')
        return ele

    @teststep
    def words(self, explain):
        """单词"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="%s"]/'
                                                'preceding-sibling::android.widget.TextView' % explain)
        return ele.text

    @teststep
    def voices(self, explain):
        """声音图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="%s"]/'
                                                'preceding-sibling::android.widget.ImageView[contains(@resource-id, "audio")]' % explain)
        return ele

    @teststep
    def correct_wrong_icon(self, explain):
        """我的结果图标"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text="%s"]/'
                                                'preceding-sibling::android.widget.ImageView[contains(@resource-id, "result")]' % explain)
        return ele

    @teststep
    def check_bank_result(self, game_name, mine_answer, has_medal):
        """结果页面答案对照"""
        if has_medal:
            if self.wait_check_medal_page():
                print('获取勋章')
                self.all_game.word_spell.share_page_operate()

        result_page_info = ()
        if self.wait_check_result_page():  # 进入结果页
            self.check_result_btn().click()  # 查看结果
            if self.wait_check_answer_page():
                print('----- 查看答案页面 ------\n')
                if game_name in ['猜词游戏', '还原单词', '单词拼写', '单词听写', '词汇选择']:
                    result_page_info = self.all_game.word_spell.word_game_result_check_operate(mine_answer)

                elif game_name in ['完形填空', '单项选择', '阅读理解', '听后选择']:
                    result_page_info = self.all_game.single_choice.single_choice_result_operate(mine_answer, game_name)

                elif game_name in ['连连看']:
                    result_page_info = self.all_game.word_match.word_match_result_operate(mine_answer)

                elif game_name in ['强化炼句']:
                    result_page_info = self.all_game.sentence_strengthen.sentence_strengthen_result_operate(mine_answer)

                elif game_name in ['听音连句']:
                    result_page_info = self.all_game.sentence_listen_link.sentence_listen_link_result_operate(mine_answer)

                elif game_name in ['句型转换']:
                    result_page_info = self.all_game.sentence_change.sentence_change_result_operate(mine_answer)

                elif game_name in ['连词成句']:
                    result_page_info = self.all_game.sentence_link.sentence_link_result_operate(mine_answer)

                elif game_name in ['补全文章']:
                    result_page_info = self.all_game.complete_article.complete_article_result_operate(mine_answer)

                elif game_name in ['选词填空']:
                    result_page_info = self.all_game.select_blank.select_bank_result_operate(mine_answer)

                elif game_name in ['听音选图']:
                    result_page_info = self.all_game.image_choice.image_choice_result_operate(mine_answer)

            self.click_back_up_button()
            return result_page_info

    @teststep
    def result_multi_data_check(self, fq, result, star_num, score_num, judge_score=True):
        if self.wait_check_result_page():
            print('===== 结果页数据核对 =====\n')
            print('本次做的题数：', result[-1])
            print('本次做对题数：', result[1])
            right_rate = round(result[1] / result[-1] * 100) if fq == 1 else 100

            if right_rate != self.correct_rate():
                self.base_assert.except_error("准确率有误，应为" + str(right_rate) + "实际为" + str(self.correct_rate()))
            else:
                print('准确率核实正确')

            if judge_score:
                if score_num != self.score():
                    self.base_assert.except_error("积分有误, 应当为" + str(score_num) + '页面为' + str(self.score()))
                else:
                    print('积分核实正确')

            if star_num != self.star():
                self.base_assert.except_error('星星有误, 应为：' + str(star_num) + '页面为：' + str(self.star()))
            else:
                print('星星核实正确')

            print('===== 结果页数据核实完毕 =====\n')

            again_btn = self.again_btn()
            if fq == 2:
                if again_btn.text != '再练一遍':
                    self.base_assert.except_error('第二遍做题后， 错填再练按钮内容未变为再练一遍')
                print('-*' * 50, '\n')
            self.again_btn().click()

