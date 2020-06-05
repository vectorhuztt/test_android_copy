#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps
from utils.get_attribute import GetAttribute
from utils.wait_element import WaitElement


class VanclassDetailPage(BasePage):
    """ 班级详情页 修改、查询页面元素信息"""
    wait = WaitElement()

    # 积分排行榜
    @teststeps
    def wait_check_score_page(self):
        """以“title:积分排行榜”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'积分排行榜')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def score_all_tab(self, index):
        """本周 &上周 &本月 &全部 index=1-4"""
        locator = (By.XPATH, "//android.widget.TextView")
        ele = self.wait.wait_find_elements(locator)[index]
        return ele

    @teststep
    def selected(self, var):
        """元素 selected属性值"""
        value = var.get_attribute('selected')
        return value

    @teststep
    def st_order(self):
        """排序"""
        locator = (By.ID, self.id_type() + 'tv_order')
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_icon(self):
        """头像"""
        locator = (By.ID, self.id_type() + "iv_student_icon")
        return self.wait.wait_find_elements(locator)

    @teststep
    def st_name(self):
        """学生 昵称"""
        locator = (By.ID, self.id_type() + "tv_student_name")
        return self.wait.wait_find_elements(locator)

    @teststep
    def num(self):
        """积分/星星数目"""
        locator = (By.ID, self.id_type() + "tv_nums")
        return self.wait.wait_find_elements(locator)

    # 星星排行榜
    @teststeps
    def wait_check_star_page(self):
        """以“title:星星排行榜”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'星星排行榜')]")
        return self.wait.wait_check_element(locator)

    # 本班作业
    @teststeps
    def wait_check_page(self, var):
        """以“title: 班级名称/ 作业名称/本班卷子/口语作业”为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'%s')]" % var)
        return self.wait.wait_check_element(locator)

    @teststep
    def exit_wechat_login_page(self):
        """退出微信登录页面"""
        locator = (By.ID, self.id_type() + 'com.tencent.mm:id/m1')
        self.wait.wait_find_elements(locator).click()

    @teststeps
    def all_tab(self):
        """全部 tab"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'全部')]")
        return self.wait.wait_find_element(locator)

    @teststeps
    def unfinished_tab(self):
        """未完成 tab"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'未完成')]")
        return self.wait.wait_find_element(locator)

    @teststeps
    def finished_tab(self):
        """已完成 tab"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'已完成')]")
        return self.wait.wait_find_element(locator)


    @teststep
    def wait_check_end_tips_page(self):
        """没有更多了"""
        locator = (By.ID, self.id_type() + 'end')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def hw_name(self):
        """作业name"""
        locator = (By.ID, self.id_type() + 'tv_homework_name')
        return self.wait.wait_find_elements(locator)


    @teststep
    def accurency(self):
        """正答率"""
        locator = (By.ID, self.id_type() + 'tv_testbank_status')
        return self.wait.wait_find_elements(locator)


    @teststep
    def spend_time(self):
        """用时"""
        locator = (By.ID, self.id_type() + 'tv_spend_time')
        return self.wait.wait_find_elements(locator)

    @teststep
    def progress(self):
        """完成进度"""
        locator = (By.ID, self.id_type() + 'roundProgressBar')
        return self.wait.wait_find_elements(locator)


    @teststep
    def finish_status(self):
        """已经有x人完成"""
        locator = (By.ID, self.id_type() + 'tv_homework_desc')
        return self.wait.wait_find_elements(locator)

    @teststep
    def create_time(self):
        """作业创建时间"""
        locator = (By.ID, self.id_type() + 'tv_create_date')
        return self.wait.wait_find_elements(locator)

    @teststep
    def remind(self):
        """提醒 按钮"""
        locator = (By.ID, self.id_type() + 'remind')
        return self.wait.wait_find_elements(locator)

    @teststep
    def rank_button(self, index):
        """排行榜 按钮"""
        locator = (By.ID, self.id_type() + 'iv_ranking')
        self.wait.wait_find_elements(locator)[index].click()

    # 分享
    @teststep
    def share_button(self):
        """分享 按钮"""
        locator = (By.ID, self.id_type() + 'share')
        self.wait.wait_find_element(locator).click()


    @teststeps
    def wait_check_share_page(self):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'微信好友')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def share_img(self):
        """图片"""
        locator = (By.ID, self.id_type() + 'share_img')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wechat_friend(self):
        """微信好友"""
        locator = (By.ID, self.id_type() + 'weixin')
        self.wait.wait_find_element(locator).click()
        print('微信好友')

    @teststep
    def wechat_circle(self):
        """微信朋友圈"""
        locator = (By.ID, self.id_type() + 'weixin_friends')
        self.wait.wait_find_element(locator).click()
        print('微信朋友圈')

    @teststep
    def save_img(self):
        """保存图片"""
        locator = (By.ID, self.id_type() + 'save_img')
        self.wait.wait_find_element(locator).click()
        print('保存图片')

    # 打卡
    @teststep
    def reward_button(self):
        """分享 按钮"""
        locator = (By.ID, self.id_type() + 'reward')
        self.wait.wait_find_element(locator).click()

    @teststeps
    def wait_check_reward_page(self):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@text,'打卡')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def get_reward_button(self):
        """礼包 按钮"""
        locator = (By.ID, self.id_type() + 'iv_reward')
        self.wait.wait_find_element(locator).click()

    @teststep
    def reward_desc(self):
        """提示：点击礼包打卡吧"""
        locator = (By.ID, self.id_type() + 'tv_reward_desc')
        return self.wait.wait_find_element(locator).text


    @teststep
    def reward_tips(self):
        """获取奖励 说明"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@index,'2')]")
        ele = self.wait.wait_find_element(locator)
        print(ele.text)

    # 打卡结果页
    @teststeps
    def wait_check_reward_result_page(self):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@resource-id,'{}tv_cards')]".format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def reward_img(self):
        """图片"""
        locator = (By.ID, self.id_type() + "iv_reward_pic")
        return self.wait.wait_check_element(locator, timeout=5)


    @teststep
    def check_complete_button(self):
        """查看完整卡片 按钮"""
        locator = (By.ID, self.id_type() + "tv_cards")
        self.wait.wait_find_element(locator).click()

    # 完整卡片页
    @teststeps
    def wait_check_complete_page(self):
        """以“title”为依据"""
        locator = (By.XPATH,
                   "//android.widget.TextView[contains(@resource-id, '{}iv_frag')]".format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def img_num(self):
        """图片 张数"""
        locator = (By.ID, self.id_type() + "tv_nums")
        return self.wait.wait_find_elements(locator)

    @teststeps
    def button_enbaled_judge(self, length, button, size1):
        """确定按钮enabled状态"""
        if 0 < length <= 30:
            if length != int(size1):
                print('❌❌❌ Error- 字符数展示有误', length, size1)
            else:
                if self.attr.get_enabled(button) == 'false':
                    print('❌❌❌ Error- 确定按钮不可点击')

        elif length == 0:
            if length != int(size1):
                print('❌❌❌ Error- 字符数展示有误', length, size1)
            else:
                if self.attr.get_enabled(button) == 'true':
                    print('❌❌❌ Error- 确定按钮未置灰可点击')
        elif length > 30:
            if length != int(size1):
                print('❌❌❌ Error- 字符数展示有误', length, size1)
            else:
                if self.attr.get_enabled(button) == 'true':
                    print('❌❌❌ Error- 确定按钮未置灰可点击')
        return self.attr.get_enabled(button)

