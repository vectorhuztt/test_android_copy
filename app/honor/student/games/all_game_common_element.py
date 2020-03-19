#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/1 11:35
# -----------------------------------------
import re
import time
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.games_keyboard import Keyboard
from utils.get_attribute import GetAttribute
from utils.toast_find import Toast


class GameCommonEle(BasePage):

    def __init__(self):
        self.keyboard = Keyboard()

    """游戏公共元素"""
    @teststep
    def wait_check_end_tip_page(self):
        """游戏标题页面检查点"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text, "到底啦 下拉刷新试试")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_commit_btn_page(self):
        """提交按钮处页面检查点"""
        locator = (By.ID, self.id_type() + 'fab_commit')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_share_area_page(self):
        """分享页面检查点"""
        locator = (By.ID, '{}share_area'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_punch_share_page(self):
        """分享页面检查点"""
        locator = (By.ID, '{}share_img'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_login_wechat_page(self):
        """微信登陆页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@text,"登录微信")]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_game_title_page(self):
        """游戏标题页面检查点"""
        locator = (By.ID, self.id_type() + 'tv_title')
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_word_container_by_index_and_id(self, index):
        """单词容器获取依据"""
        locator = (By.XPATH, "//*[@content-desc='{}' and contains(@resource-id, 'item_container')]".format(index))
        return self.get_wait_check_page_result(locator, timeout=2)

    @teststep
    def wait_check_sentence_container_by_content_desc(self, index):
        """句子容器获取依据"""
        locator = (By.XPATH, "//android.widget.LinearLayout[@content-desc='{}']".format(index))
        return self.get_wait_check_page_result(locator, timeout=2)

    @teststep
    def wait_check_article_container_by_index(self, index):
        """文章类游戏容器获取依据"""
        locator = (By.XPATH, "//android.widget.LinearLayout[@index='{}']/android.view.ViewGroup".format(index))
        return self.get_wait_check_page_result(locator, timeout=2)

    @teststep
    def wait_check_tips_page(self):
        """提示页面检查点"""
        locator = (By.ID, '{}md_title'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_play_voice_page(self):
        """喇叭播放按钮"""
        locator = (By.ID, '{}play_voice'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_dragger_btn(self):
        """检查页面是否存在拖拽按钮"""
        locator = (By.ID, self.id_type() + "dragger")
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_rich_text_page(self):
        """文章类游戏富文本元素页面检查点"""
        locator = (By.ID, '{}rich_text'.format(self.id_type()))
        return self.get_wait_check_page_result(locator)

    @teststep
    def wait_check_keyboard_page(self):
        """键盘页面检查"""
        locator = (By.ID, '{}keyboard_abc_view'.format(self.id_type()))
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_check_permit_tab_page(self):
        """存储允许"""
        locator = (By.ID, 'com.android.packageinstaller:id/permission_message')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def always_permit_allow_btn(self):
        """始终允许按钮"""
        ele = self.driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button')
        return ele

    @teststep
    def game_title(self):  # 题型标题
        title = self.driver \
            .find_element_by_id(self.id_type() + "tv_title")
        return title

    @teststep
    def game_mode_id(self):
        """获取题目的mode_id"""
        mode_id = int(self.game_title().get_attribute('contentDescription').split('  ')[1])
        return mode_id


    @teststep
    def hide_keyboard_btn(self):
        """键盘隐藏按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'keyboard_hide')
        return ele

    @teststep
    def rich_text(self):
        """文章类游戏文章文本"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rich_text')
        return ele

    @teststep
    def question(self):
        """游戏问题"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'question')
        return ele

    @teststep
    def get_opt_text_by_ques(self, ques):
        """根据问题获取选项"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text()="{}"]/android.widget.TextView[contains[@resource-id, '
                                                '"tv_item"]]'.format(ques))
        return ele

    @teststep
    def get_opt_char_by_ques(self, ques):
        """根据问题获取选项字母"""
        ele = self.driver.find_element_by_xpath('//android.widget.TextView[@text()="{}"]/android.widget.TextView[contains[@resource-id, '
                                                '"tv_char"]]'.format(ques))
        return ele


    @teststep
    def clear_btn(self):
        """清除按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'bt_clear')
        return ele

    @teststep
    def tips_content(self):
        """提示 具体内容"""
        item = self.driver \
            .find_element_by_id(self.id_type() + "md_content")
        return item.text

    @teststep
    def click_confirm_btn(self):
        """确定 按钮"""
        self.driver \
            .find_element_by_id(self.id_type() + "md_buttonDefaultPositive") \
            .click()

    @teststeps
    def tips_operate(self):
        """提示信息处理"""
        if self.wait_check_tips_page():
            print(self.tips_content(), '\n')
            self.click_confirm_btn()  # 确定按钮
            time.sleep(2)

    @teststep
    def click_voice(self):
        """播放按钮"""
        self.driver. \
            find_element_by_id(self.id_type() + "play_voice") \
            .click()

    @teststep
    def fab_next_btn(self):
        """下一步按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_next')
        return ele

    @teststep
    def fab_commit_btn(self):
        """下一步提交按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'fab_commit')
        return ele

    @teststep
    def commit_without_fab_btn(self):
        """下一步提交按钮不带fab"""
        ele = self.driver.find_element_by_id(self.id_type() + 'commit')
        return ele

    @teststep
    def opt_options(self):
        """选项 文本"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_item')
        return ele

    @teststep
    def opt_char(self):
        """选项 字母 ABCD"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'tv_char')
        return ele

    @teststep
    def sound_icon(self):
        """喇叭按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'sound')
        return ele

    @teststep
    def drag_btn(self):
        """拖拽按钮"""
        ele = self.driver.find_element_by_id('{}dragger'.format(self.id_type()))
        return ele

    @teststep
    def font_middle(self):
        """第一个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_middle")
        return ele

    @teststep
    def font_large(self):
        """第二个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_large")
        return ele

    @teststep
    def font_great(self):
        """第三个Aa"""
        ele = self.driver.find_element_by_id(self.id_type() + "font_great")
        return ele

    @teststep
    def wechat(self):
        """微信"""
        ele = self.driver.find_element_by_id(self.id_type() + 'weixin')
        return ele

    @teststep
    def friends(self):
        """朋友圈"""
        ele = self.driver.find_element_by_id(self.id_type() + "weixin_friends")
        return ele

    @teststep
    def download(self):
        """保存图片"""
        ele = self.driver.find_element_by_id(self.id_type() + 'save_img')
        return ele

    @teststep
    def wechat_back_up_btn(self):
        """微信页面退回按钮"""
        ele = self.driver.find_element_by_accessibility_id('返回')
        return ele


    @teststeps
    def get_rich_text_input_count(self):
        """获取需要输入的个数"""
        sentence_desc = self.rich_text().get_attribute('contentDescription')
        input_num = len([x for x in sentence_desc.split('##')[1].split('  ') if x != ''])
        return input_num

    @teststep
    def get_rich_text_answer(self):
        """获取我输入的答案"""
        desc = self.rich_text().get_attribute('contentDescription')
        return [x for x in desc.split('## ')[1].split('  ') if x and '(' not in x]

    @teststep
    def rest_bank_num(self):
        """待完成题数"""
        ele = self.driver.find_element_by_id('{}rate'.format(self.id_type()))
        return int(ele.text)

    @teststep
    def bank_time(self):
        """题目时间"""
        ele = self.driver.find_element_by_id('{}time'.format(self.id_type()))
        time_str = re.findall(r'\d', ele.text)
        return int(time_str[0]) * 3600 + int(time_str[1]) * 60 + int(time_str[2]) * 10 + int(time_str[3])

    @teststeps
    def check_position_change(self):
        if self.wait_check_keyboard_page():
            self.hide_keyboard_btn().click()

        self.screen_swipe_down(0.5, 0.2, 0.9, 1000)
        if GetAttribute().get_checked(self.font_large()) == 'false':
            self.base_assert.except_error('页面未默认选择中等字体')

        # 依次点击Aa，并获取第一个填空的X轴位置，比较大小
        large_size = self.rich_text().size

        self.font_middle().click()
        time.sleep(1)
        middle_size = self.rich_text().size

        self.font_great().click()
        time.sleep(1)
        great_size = self.rich_text().size

        if large_size['height'] < middle_size['height']:
            self.base_assert.except_error('大字体变中等字体未发生变化')
        if great_size['height'] < large_size['height']:
            self.base_assert.except_error('超大字变大字体未发生变化')

    @teststeps
    def drag_up_down(self, drag_down=True):
        """拖拽操作"""
        if self.wait_check_dragger_btn():
            loc = self.get_element_location(self.drag_btn())  # 获取按钮坐标
            if drag_down:
                self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, self.get_window_size()[1] - 20)  # 拖拽至最下方
            else:
                self.driver.swipe(loc[0] + 45, loc[1] + 45, loc[0] + 45, loc[1] - 450)  # 拖拽至最上方

    @teststeps
    def next_btn_judge(self, var, fun):
        """下一步按钮状态判断"""
        value = GetAttribute().get_enabled(fun())
        if value != var:  # 测试 下一步 按钮 状态
            self.base_assert.except_error('按钮 状态Error' + str(value))

    @teststeps
    def next_btn_operate(self, var, fun):
        """下一步按钮操作"""
        self.next_btn_judge(var, fun)
        fun().click()
        time.sleep(1.5)

    @teststep
    def get_last_text_id(self):
        """获取最后一个文本的属性"""
        last_text = self.driver.find_elements_by_class_name('android.widget.TextView')
        last_text_id = last_text[-1].get_attribute('resourceId')
        if 'question' in last_text_id:
            return 'ques'
        elif 'item' in last_text_id:
            return 'opt'

    @teststep
    def get_ques_opt_scale(self):
        """获取包含题目或只有选项的屏幕占比"""
        ques_text = self.question()[0].text
        ques_bank = self.driver.find_element_by_xpath('//*[@text="{}"]/..'.format(ques_text))
        ques_options = self.driver.find_element_by_xpath('//*[@text="{}"]/following-sibling::android.view.ViewGroup'.format(ques_text))
        screen_height = self.get_window_size()[1]
        ques_scale = float('%.2f' % (ques_bank.size['height'] / screen_height))
        opt_scale = float('%.2f' % (ques_options.size['height'] / screen_height))
        return ques_scale, opt_scale

    @teststep
    def value_is_explain(self, dict_info):
        """判断字典的key是否都是数字"""
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        result = any([pattern.search(dict_info[x]) for x in dict_info])
        if result:
            return True
        else:
            return False

    @teststeps
    def judge_timer(self, timer):
        if len(timer) > 1:
            if any(timer[i + 1] > timer[i] for i in range(0, len(timer) - 1)):
                print('计时功能无误:', timer, '\n')
                return True
            else:
                self.base_assert.except_error('Error - 计时错误:' + str(timer) + '\n')
        else:  # 只有一道题
            print('只有一道题，时间为:', timer[0], '\n')
            return True


    @teststep
    def rate_judge(self, total, i):
        """待完成数校验"""
        current_rate = self.rest_bank_num()
        if int(current_rate) != total - i:
            self.base_assert.except_error('待完成数不正确 {} 应为：{}'.format(current_rate, total - i))

    @teststeps
    def share_page_operate(self):
        """分享页面具体操作"""
        if self.wait_check_punch_share_page():
            self.wechat().click()
            if not self.wait_check_login_wechat_page():
                self.base_assert.except_error('未跳转到微信登录页面')
            self.wechat_back_up_btn().click()

            if self.wait_check_punch_share_page():
                self.friends().click()
                if not self.wait_check_login_wechat_page():
                    self.base_assert.except_error('未跳转到微信登录页面')
                self.wechat_back_up_btn().click()

            if self.wait_check_punch_share_page():
                self.download().click()
                if not Toast().find_toast('已保存到本地'):
                    if self.wait_check_permit_tab_page():
                        self.always_permit_allow_btn().click()
                        if not Toast().find_toast('已保存到本地'):
                            self.base_assert.except_error('未发现保存图片提示')
                    else:
                        self.base_assert.except_error('未发现保存到本地提示')
                else:
                    print('图片已保存到本地')
                self.click_back_up_button()




