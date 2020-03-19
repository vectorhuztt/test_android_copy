#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/11/28 11:24
# -----------------------------------------
from selenium.webdriver.common.by import By

from app.honor.student.games.all_game_common_element import GameCommonEle
from app.honor.student.login.object_page.home_page import HomePage
from conf.base_page import BasePage
from conf.decorator import teststep


class H5SharePage(BasePage):
    # 书单分享页面
    @teststep
    def wait_check_share_h5_page(self):
        locator = (By.ID, 'app')
        return self.get_wait_check_page_result(locator, timeout=5)

    @teststep
    def wait_h5_share_wechat_group_page(self):
        """底部分享微信页面检查点"""
        locator = (By.XPATH, '//*[contains(@text, "分享到微信群")]')
        return self.get_wait_check_page_result(locator, timeout=10)

    @teststep
    def wait_share_wechat_friend_page(self):
        locator = (By.XPATH, '//*[contains(@text, "微信好友")]')
        return self.get_wait_check_page_result(locator, timeout=10)


    @teststep
    def wait_check_share_no_speak_tip_page(self):
        """无口语推荐片段提示页面检查点"""
        locator = (By.XPATH, '//*[@text="提示"]')
        return self.get_wait_check_page_result(locator)

    @teststep
    def share_page_nickname(self):
        """分享"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[2]/android.view.View')
        return ele.text

    @teststep
    def share_page_book_name(self):
        """分享页书籍名称"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[3]')
        return ele.text

    @teststep
    def share_page_play_part_btn(self):
        """分享页面播放按钮"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[4]/android.widget.Image[3]')
        return ele

    @teststep
    def share_page_like_btn(self):
        """分享页面点赞按钮"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[4]/android.widget.Image[4]')
        return ele

    @teststep
    def share_page_like_num(self):
        """分享页面点赞数量"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[4]/android.view.View[2]')
        return ele

    @teststep
    def share_page_show_off_btn(self):
        """分享页面炫耀一下页面"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[5]')
        return ele

    @teststep
    def share_page_phone_icon(self):
        """分享页手机图标"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[6]/android.view.View[4]')
        return ele

    @teststep
    def share_page_phone_num(self):
        """分享页电话号码"""
        ele = self.driver.find_element_by_xpath('//android.view.View[@resource-id="app"]/android.view.View[6]/android.view.View[2]')
        return ele.text.split('电话：')[1]

    @teststep
    def close_no_speak_tip(self):
        """关闭没有推荐口语提示"""
        ele = self.driver.find_element_by_xpath('//*[@text="关闭"]')
        return ele

    @teststep
    def share_page_right_top_share_btn(self):
        """分享页面分享按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'menu_share')
        return ele

    @teststep
    def wechat_group_share_icons(self):
        """点击炫耀一下出现下方分享图标"""
        ele = self.driver.find_elements_by_xpath("//android.view.View[contains(@resource-id, 'layui-m')]//android.widget.Image")
        return ele

    @teststep
    def wechat_friend_share_icons(self):
        """点击右上角出现的微信分享图标"""
        ele = self.driver.find_elements_by_xpath('//android.widget.LinearLayout[contains(@resource-id, "share_area")]/android.widget.TextView')
        return ele

    @teststep
    def h5_wechat_share_operate(self, icons, func):
        """h5页面微信分享过程"""
        for x in icons:
            if func():
                x.click()
                if not GameCommonEle().wait_check_login_wechat_page():
                    self.base_assert.except_error('点击微信分享图标， 未进入微信登陆页面')
                GameCommonEle().wechat_back_up_btn().click()
        if func():
            HomePage().click_blank()

    @teststep
    def share_h5_page_operate(self, nickname, book_name, no_speak_tip, like_num):
        """h5分享页面处理过程"""
        if self.wait_check_share_h5_page():
            # 昵称 书单名 播放按钮 点赞数校验
            share_nick_name = self.share_page_nickname()
            if nickname != share_nick_name:
                self.base_assert.except_error('分享页面用户昵称与系统昵称不一致')

            share_book_name = self.share_page_book_name()
            if book_name != share_book_name():
                self.base_assert.except_error('分享页面书单名称与测试书单不一致')

            self.share_page_play_part_btn().click()
            if no_speak_tip:
                if not self.wait_check_share_no_speak_tip_page():
                    self.base_assert.except_error('排行榜页面提示无口语片段， 但是h5分享页面无此提示')
                else:
                    print('暂无口语片段')
                    self.close_no_speak_tip()
            else:
                if self.wait_check_share_no_speak_tip_page():
                    self.base_assert.except_error('排行榜页面未提示无口语片段， 但是h5分享页面出现此提示')
                    self.close_no_speak_tip()

            if self.wait_check_share_h5_page():
                share_like_num = self.share_page_like_num()
                if like_num != share_nick_name:
                    self.base_assert.except_error('书单页的点赞数与h5分享页的点赞数不一致， 分享页为{}, 书单页为{}'.format(share_like_num, like_num))
                if self.share_page_like_btn().get_attribute('clickable') == 'false':
                    self.base_assert.except_error('h5分享页面点赞图标默认为已点击')
                else:
                    self.share_page_like_btn().click()
                    if self.share_page_like_num() != str(int(share_like_num) + 1):
                        self.base_assert.except_error('h5分享页面，点击点赞图标， 点赞数数未增加')

        self.share_page_show_off_btn().click()
        if not self.wait_h5_share_wechat_group_page():
            self.base_assert.except_error('点击h5的炫耀一下按钮，未显示分享至微信群区域')
        else:
            self.h5_wechat_share_operate(self.wechat_group_share_icons(), self.wait_h5_share_wechat_group_page)

        if self.wait_check_share_h5_page():
            self.share_page_right_top_share_btn().click()
            if not self.wait_share_wechat_friend_page():
                self.base_assert.except_error('点击右上角分享按钮，未出现微信分享图标')
            else:
                self.h5_wechat_share_operate(self.wechat_friend_share_icons(), self.wait_share_wechat_friend_page)

        if self.wait_check_share_h5_page():
            self.click_back_up_button()


