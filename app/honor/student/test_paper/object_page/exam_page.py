import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.games.all_game_init import AllGameClass
from app.honor.student.games.word_match_new import LinkWordGame
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.answer_page import AnswerPage
from app.honor.student.test_paper.object_page.games.blank_cloze import BlankCloze
from app.honor.student.test_paper.object_page.games.cloze_test import ClozeTest
from app.honor.student.test_paper.object_page.games.complete_text import CompleteText
from app.honor.student.test_paper.object_page.games.link_to_sentence import Conjunctions
from app.honor.student.test_paper.object_page.games.word_guess import GuessingWord
from app.honor.student.test_paper.object_page.games.listen_select import ListenSelect
from app.honor.student.test_paper.object_page.games.listen_spell import ListenSpell
from app.honor.student.test_paper.object_page.games.listen_to_sentence import ListenSentence
from app.honor.student.test_paper.object_page.games.read_understand import ReadUnderstand
from app.honor.student.test_paper.object_page.games.word_restore import RestoreWord
from app.honor.student.test_paper.object_page.games.sentence_enhance import SentenceEnhance
from app.honor.student.test_paper.object_page.games.sentence_exchange import ExamSentenceExchange
from app.honor.student.test_paper.object_page.games.single_choice import SingleChoice
from app.honor.student.test_paper.object_page.games.vocab_select import VocabSelect
from app.honor.student.test_paper.object_page.games.word_match import WordMatch
from app.honor.student.test_paper.object_page.games.word_spell import WordSpell
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class ExamPage(BasePage):
    """试卷页面"""

    def __init__(self):
        self.home = HomePage()
        self.game = VocabSelect()
        self.answer = AnswerPage()
        self.all_game = AllGameClass()

    @teststep
    def wait_check_exam_title_page(self):
        """以 试卷的标题作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'试卷')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_counter_page(self):
        """以 做试卷时的计时作为 页面检查点"""
        locator = (By.ID, self.id_type() + "time_container")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_exam_confirm_page(self):
        """以 试卷确认的标题作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'试卷确认')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_rank_page(self):
        """以 炫耀一下的text作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'炫耀一下')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_end_page(self):
        """等待 滑到底提示"""
        try:
            self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"到底啦 下拉刷新试试")]')
            return True
        except:
            return False

    @teststep
    def exam_names(self):
        """试卷名称"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_name')
        return ele

    @teststep
    def finish_count(self):
        """完成人数"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_finishcount')
        return ele

    @teststep
    def finish_status(self):
        """完成状态"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'rtv_mode')
        return ele

    @teststep
    def get_all_text(self):
        """获取所有文本"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def click_start_exam_button(self):
        """点击 开始考试"""
        self.driver.\
            find_element_by_id(self.id_type() + 'start_write')\
            .click()

    @teststep
    def index_group(self):
        ele = self.driver.find_elements_by_id(self.id_type() + 'recyclerview')
        return ele

    @teststep
    def close_answer(self):
        """关闭答题卷页面"""
        self.driver.find_element_by_id(self.id_type() + 'answerclose').click()

    @teststep
    def exam_back_to_home(self):
        self.home.click_back_up_button()
        if self.wait_check_exam_title_page():
            self.home.click_back_up_button()
            if self.home.wait_check_home_page():
                print('返回主页面')

    @teststeps
    def select_one_exam(self):
        """随机选择一个试卷"""
        exams_info = {}     # 将试卷存入一个字典当周，以试卷名作为key，试卷描述与完成状态作为value
        while True:
            exams = self.exam_names()
            finish_status = self.finish_status()  # 试卷完成状态
            finish_count = self.finish_count()   # 试卷几人完成
            for i in range(len(exams)):
                exams_info[exams[i].text] = finish_status[i].text + ' -- '+finish_count[i].text
            if not self.wait_check_end_page():  # 没有发现滑动到底的则进行滑动
                self.home.screen_swipe_up(0.5, 0.9, 0.7, 1000)
            else:
                # exams_info[exams[-1].text] = finish_status[-1].text + ' -- ' + finish_count[-1].text
                self.home.screen_swipe_down(0.5, 0.2, 0.9, 1000)
                break

        for name in exams_info.keys():
            print(name, '   ', exams_info[name])

        exam = self.exam_names()[0]
        test_name = exam.text
        print('选择试卷：', test_name)
        exam.click()
        print('------------------------------\n')
        return test_name

    @teststeps
    def exam_confirm_ele_operate(self):
        """确认页面 文本展示"""
        ele = self.get_all_text()
        print('\n<试卷确认页面>：\n')
        self.print_exam_info(ele)
        print(ele[14].text + '\n' + ele[15].text + '\n' + ele[16].text + '\n' + ele[17].text)  # 说明
        print('--------------------------------\n')
        return int(ele[9].text)

    @teststep
    def print_exam_info(self, ele):
        """打印出试卷头部信息"""
        print(ele[1].text, ':', ele[2].text)     # 试卷名称
        print(ele[5].text, ':', ele[3].text+ele[4].text)  # 试卷模式
        print(ele[8].text, ':', ele[6].text+ele[7].text)  # 时间
        print(ele[11].text, ':', ele[9].text+ele[10].text)  # 题数
        print(ele[13].text, ':', ele[12].text)  # 限制

    @teststeps
    def get_ques_name(self, total):
        """获取所有题型"""
        if self.wait_check_exam_counter_page():
            self.answer.answer_check_button().click()
            if self.answer.wait_check_answers_page():
                tip_num = []
                tips = []
                while True:
                    titles = self.answer.question_titles()
                    for i, x in enumerate(titles):
                        if x.text in tips:
                            continue
                        else:
                            if i == len(titles) - 1:
                                self.home.screen_swipe_up(0.5, 0.87, 0.7, 1000)
                            ques_num = self.answer.ques_num(x.text)
                            num = int(re.findall(r'\d+', ques_num)[0])
                            tips.append(x.text)
                            print(x.text, ' ', ques_num)
                            tip_num.append(num)
                    if sum(tip_num) < total:
                        self.home.screen_swipe_up(0.5, 0.9, 0.4, 1000)
                    else:
                        break

                self.close_answer()
                print('--------------------------------\n')
                return tips

    @teststeps
    def play_examination(self, tips, exam_json):
        """做题过程"""
        if self.wait_check_exam_counter_page():
            self.answer.answer_check_button().click()   # 查看答题卷
            if self.answer.wait_check_answers_page():
                index = 0
                while index < len(tips):
                    title_list = [x.text for x in self.answer.question_titles()]       # 题型数组
                    if tips[index] in title_list:
                        first_index = self.answer.tip_index(tips[index])    # 题型的第一道题
                        ques_num = self.answer.ques_num(tips[index])          # 题数描述 （共*题）
                        num = int(''.join(re.findall(r'\d+', ques_num)))  # 从描述中获取题数
                        first_index[0].click()     # 点击第一题进入习题
                        self.exam_process(tips[index], num, exam_json)   # 对应习题的游戏过程
                        self.answer.answer_check_button().click()    # 游戏结束后点击答题卷进入下一题
                        if self.answer.wait_check_answers_page():
                            pass
                        index = index + 1
                    else:
                        self.home.screen_swipe_up(0.5, 0.8, 0.4, 2000)

                if self.answer.wait_check_answers_page():
                    self.answer.submit_tip_operate()  # 交卷
                    if self.wait_check_rank_page():
                        self.exam_back_to_home()  # 返回

    @teststeps
    def exam_process(self, title, num, exam_json):
        print('\n-------%s-共%d题------\n' % (title, num))
        if '听后选择' in title:
            ListenSelect().play_listening_select_game(num, exam_json)
            self.answer.wait_result_btn_enabled()

        elif '猜词游戏' in title:
            GuessingWord().play_guessing_word_game(num, exam_json)

        elif '单项选择' in title:
            SingleChoice().play_single_choice_game(num, exam_json)

        elif '词汇选择' in title:
            VocabSelect().play_vocab_select_game(num, exam_json)

        elif '单词拼写' in title:
            WordSpell().play_word_spell_game(num, exam_json)

        elif '单词听写' in title:
            ListenSpell().play_listen_spell_game(num, exam_json)

        elif '连词成句' in title:
            Conjunctions().play_conjunctions_game(num, exam_json)

        elif '还原单词' in title:
            RestoreWord().play_restore_word_game(num, exam_json)

        elif '连连看' in title:
            WordMatch().play_word_match_game(num, exam_json)

        elif '强化炼句' in title:
            SentenceEnhance().play_sentence_enhance_game(num, exam_json)

        elif '听音连句' in title:
            ListenSentence().play_listen_sentence_game(num, exam_json)

        elif '句型转换' in title:
            ExamSentenceExchange().play_sentence_exchange_game(num, exam_json)

        elif '完形填空' in title:
            ClozeTest().play_cloze_test_game(num, exam_json)

        elif '选词填空' in title:
            BlankCloze().play_bank_cloze_game(num, exam_json)

        elif '补全文章' in title:
            CompleteText().play_complete_article_game(num, exam_json)

        elif '阅读理解' in title:
            ReadUnderstand().play_read_understand_game(num, exam_json)

        else:
            pass
















