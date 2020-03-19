#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/8 10:55
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf.base_page import BasePage
from conf.decorator import teststep, teststeps


class WKGamePage(BasePage):

    @teststep
    def wait_check_wk_page(self):
        """微课页面检查点"""
        locator = (By.ID, self.id_type() + "rotate")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_play_btn_page(self):
        """播放按钮页面检查点"""
        locator = (By.ID, self.id_type() + "exo_play")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def video_pause_btn(self):
        """播放暂停按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'exo_pause')
        return ele

    @teststep
    def video_play_btn(self):
        """播放按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'exo_play')
        return ele

    @teststep
    def play_time(self):
        """播放时间"""
        ele = self.driver.find_element_by_id(self.id_type() + 'exo_position')
        return ele.text


    @teststep
    def screen_rotate_btn(self):
        """屏幕旋转按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + 'rotate')
        return ele

    @teststep
    def video_size(self):
        """视频大小"""
        ele = self.driver.find_element_by_id(self.id_type() + 'exo_content_frame')
        return ele.size


    @teststeps
    def wk_game_operate(self):
        """微课的游戏过程"""
        if self.wait_check_wk_page():
            play_time = self.play_time()
            time.sleep(2)
            if self.play_time() == play_time:
                self.base_assert.except_error('视频进度未发生变化')

            self.video_pause_btn().click()
            pause_time = self.play_time()
            if not self.wait_check_play_btn_page():
                self.base_assert.except_error('点击暂停按钮后按钮未显示暂停')
            else:
                print('暂停播放测试通过')

            time.sleep(2)
            if self.play_time() != pause_time:
                self.base_assert.except_error('点击暂停后视频进度发生变化')
            else:
                print('播放进度测试通过')

            default_size = self.video_size()
            screen_size = self.get_window_size()
            print('当前屏幕尺寸：', screen_size)
            if default_size['height'] == screen_size[0]:
                self.base_assert.except_error('默认视屏大小为全屏大小')
            else:
                print('默认屏大小检查通过')

            self.screen_rotate_btn().click()
            rotate_size = self.video_size()
            print('旋转后的屏幕尺寸：', rotate_size)

            if rotate_size['width'] != screen_size[1]:
                self.base_assert.except_error('横屏后视频的宽度不是手机屏幕的高度')

            if rotate_size['height'] != screen_size[0]:
                self.base_assert.except_error('横屏后视频的高度不等于手机屏幕的宽度')

            self.click_back_up_button()
            if self.video_size() != default_size:
                self.base_assert.except_error('全屏状态点击返回按钮，视频大小未缩小为默认大小')
            else:
                print('全屏返回测试通过')

            self.click_back_up_button()





