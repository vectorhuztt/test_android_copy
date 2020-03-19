from selenium.webdriver.common.by import By
from app.honor.student.games.all_game_init import AllGameClass
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.word_book_rebuild.object_page.ranking_page import RankingPage
from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class DetailPage(BasePage):
    def __init__(self):
        self.rank = RankingPage()
        self.home = HomePage()
        self.all_game = AllGameClass()

    @teststep
    def wait_check_exam_title_page(self):
        """以 试卷的标题作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'试卷')]")
        return self.get_wait_check_page_result(locator)

    @teststeps
    def wait_check_van_class_list_page(self):
        """班级列表页面检查点"""
        locator = (By.XPATH, "//android.widget.ListView/android.widget.CheckedTextView")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_rank_page(self):
        """以 炫耀一下的text作为 页面检查点"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'炫耀一下')]")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_share_page(self):
        """以 分享图片的id作为 页面检查点"""
        locator =(By.ID, "{}share_img".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_detail_page(self):
        """以 详情页的id作为 页面检查点"""
        locator =(By.ID, "{}status_content_view".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_again_btn_page(self):
        """以 再练一次的id 作为页面检查点"""
        locator = (By.ID, "{}again".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_qr_failed_page(self):
        """以 二维码生成失败页面检查点"""
        locator = (By.ID, "{}no_network_view".format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def get_all_text(self):
        """获取所有文本"""
        ele = self.driver.find_elements_by_class_name('android.widget.TextView')
        return ele

    @teststep
    def user_nickname(self):
        """用户昵称"""
        ele = self.driver.find_element_by_id('{}name'.format(self.id_type()))
        return ele.text

    @teststep
    def class_name(self):
        """班级名称"""
        ele = self.driver.find_elements_by_id('android:id/text1')
        return ele

    @teststep
    def score_got(self):
        """分数"""
        score = self.driver.find_element_by_id('{}cover_title_two'.format(self.id_type()))
        return score.text

    @teststep
    def rank_info(self):
        """班级排名"""
        ele = self.driver.find_element_by_id('{}rank'.format(self.id_type()))
        return ele.text

    @teststep
    def class_students(self):
        """班级学生"""
        ele = self.driver.find_elements_by_id('{}tv_name'.format(self.id_type()))
        return ele

    @teststep
    def class_students_score(self):
        """学生获得的分数"""
        ele = self.driver.find_elements_by_id('{}tv_score'.format(self.id_type()))
        return ele

    @teststep
    def check_detail(self):
        """查看详情 按钮"""
        self.driver \
            .find_element_by_id("{}detail".format(self.id_type())) \
            .click()

    @teststep
    def ques_type(self):
        """题型名称"""
        ele = self.driver.find_elements_by_id('{}tv_name'.format(self.id_type()))
        return ele

    @teststep
    def ques_score(self, var):
        """题型分数"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/'
                                                'following-sibling::android.widget.TextView'
                                                '[contains(@resource-id,"{1}tv_score")]'.format(var, self.id_type()))
        return ele

    @teststep
    def ques_desc(self, var):
        """题型 描述"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{0}")]/'
                                                'following-sibling::android.widget.TextView'
                                                '[contains(@resource-id, "{1}tv_desc")]'.format(var, self.id_type()))
        return ele.text

    @teststep
    def detail_title(self):
        """试卷详情页 点击分数后的标题"""
        ele = self.driver.find_element_by_id('{}tv_title'.format(self.id_type()))
        return ele.text

    @teststep
    def detail_score(self):
        """题型详情页题目下方的分数描述"""
        ele = self.driver.find_element_by_id('{}tv_score'.format(self.id_type()))
        return ele.text

    @teststep
    def detail_back_to_home(self):
        """由试卷详情 返回主界面"""
        self.home.click_back_up_button()
        if self.wait_check_rank_page():
            self.home.click_back_up_button()
            if self.wait_check_exam_title_page():
                self.home.click_back_up_button()
                if self.home.wait_check_home_page():
                    print('返回主界面')

    @teststeps
    def rank_page_operate(self, nickname):
        """排行版页面元素解析"""
        name = self.user_nickname()
        print('昵称：', name)
        if name == nickname:
            print('用户昵称核实正确')
        else:
            self.base_assert.except_error('用户昵称与个人中心不一致！')
        score = self.score_got()
        print('分数：', score)

        rank = self.rank_info()
        print('排名：', rank, '\n')

        class_tab = self.class_name()
        class_tab[0].click()
        print('班级页面检查点：', self.wait_check_van_class_list_page())
        if self.wait_check_van_class_list_page():
            class_list = self.class_name()
            self.class_name()[0].click()
            for i in range(len(class_list)):
                if self.wait_check_rank_page():
                    class_tab = self.class_name()
                    class_tab[0].click()
                    print('班级页面检查点：', self.wait_check_van_class_list_page())
                    if self.wait_check_van_class_list_page():
                        print('班级：', self.class_name()[i].text)
                        self.class_name()[i].click()
                        if self.wait_check_rank_page():
                            print('名称\t分数')
                            for j in range(len(self.class_students())):
                                student_name = self.class_students()[j].text
                                student_score = self.class_students()[j].text
                                print(student_name, '\t', student_score)
                            print('-'*20, '\n')
        if self.wait_check_rank_page():
            self.rank.share_button()
            if self.wait_check_share_page():
                print('<分享页面>')
            elif self.wait_check_qr_failed_page():
                print('分享二维码生成失败')
            self.home.click_back_up_button()

    @teststep
    def print_exam_info(self, ele):
        """打印出试卷头部信息"""
        print(ele[1].text, ':', ele[2].text)  # 试卷名称
        print(ele[5].text, ':', ele[3].text + ele[4].text)  # 试卷模式
        print(ele[8].text, ':', ele[6].text + ele[7].text)  # 时间
        print(ele[11].text, ':', ele[9].text + ele[10].text)  # 题数
        print(ele[13].text, ':', ele[12].text)  # 限制

    @teststep
    def get_ques_info(self, section_ids):
        """试卷详情页面 元素解析"""
        print('\n 试卷详情页面 \n')
        ele = self.get_all_text()
        self.print_exam_info(ele)

        tips = []
        while True:
            ques_types = self.ques_type()  # 试卷题型
            for i in range(len(ques_types)):
                if ques_types[i].text in tips:
                    continue
                else:
                    score = self.ques_score(ques_types[i].text)
                    desc = self.ques_desc(ques_types[i].text)
                    print(ques_types[i].text, desc, score.text)
                    tips.append(ques_types[i].text)
            if len(tips) < len(section_ids):
                self.home.screen_swipe_up(0.5, 0.8, 0.5, 2000)
            else:
                break
        self.home.click_back_up_button()
        return tips

    @teststep
    def check_ques_detail(self, exam_data):
        """详情页 具体步骤"""
        index = 0
        while index < len(exam_data):
            quote_list = [x.text for x in self.ques_type()]
            quote_name = list(exam_data.keys())[index]
            bank_data = exam_data[quote_name]
            if quote_name in quote_list:
                score = self.ques_score(quote_name)  # 分数
                desc = self.ques_desc(quote_name)   # 描述
                score.click()  # 点击分数进入题目的详情页
                print('\n-----', quote_name, '------\n')
                if self.wait_check_again_btn_page():
                    title = self.detail_title()  # 题型的标题
                    score = self.detail_score()    # 分数
                    print(title, '  ', score, '\n')
                    self.ques_detail(quote_name, bank_data)  # 题型详情页的操作
                    index = index + 1
                    self.home.click_back_up_button()
                    if self.wait_check_detail_page():
                        pass
            else:
                self.home.screen_swipe_down(0.5, 0.8, 0.4, 2000)  # 滑屏

    @teststep
    def ques_detail(self, ques_type, bank_info):
        """不同题型的详情页处理方法"""
        if ques_type in ['还原单词', '猜词游戏', '单词拼写', '词汇选择', '单词听写']:
            self.all_game.word_spell.word_game_result_check_operate(bank_info)

        elif ques_type in ['完形填空', '单项选择', '阅读理解', '听后选择']:
            self.all_game.listen_choice.single_choice_result_operate(bank_info, ques_type)

        elif ques_type in ['连连看']:
            self.all_game.word_match.word_match_result_operate(bank_info)

        elif ques_type == '强化炼句':
            self.all_game.sentence_strengthen.sentence_strengthen_result_operate(bank_info)

        elif ques_type == '补全文章':
            self.all_game.complete_article.complete_article_result_operate(bank_info)

        elif ques_type == '选词填空':
            self.all_game.select_blank.select_bank_result_operate(bank_info)

        if ques_type == '听音连句':
            self.all_game.sentence_listen_link.sentence_listen_link_result_operate(bank_info)

        elif ques_type == '连词成句':
            self.all_game.sentence_link.sentence_link_result_operate(bank_info)

        elif ques_type == '句型转换':
            self.all_game.sentence_change.sentence_change_result_operate(bank_info)

        else:
            print('-'*30, '\n')


