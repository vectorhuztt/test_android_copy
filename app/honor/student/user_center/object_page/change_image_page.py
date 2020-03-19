#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.click_bounds import ClickBounds


class MeizuPage(BasePage):
    """魅族5.1"""

    # 拍照 魅族5.1
    @teststeps
    def wait_check_camera_page(self, var=10):
        """以 “拍照键”的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.camera:id/shutter_btn")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 第一页面
    @teststep
    def click_camera_button(self):
        """以相机拍照按钮"""
        time.sleep(2)
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/shutter_btn") \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.camera:id/btn_retake")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 保存按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/btn_done") \
            .click()

    @teststep
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.meizu.media.camera:id/btn_retake") \
            .click()

    # 第三页面
    @teststep
    def wait_check_save_page(self):
        """取消 按钮 的为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '取消')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_save_button(self):
        """相机保存按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'完成')]") \
            .click()

    @teststep
    def click_cancel_button(self):
        """相机取消按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'取消')]") \
            .click()

    # 相册 魅族5.1
    @teststep
    def wait_check_album_page(self):
        """最新tab 的单个内容 的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.gallery:id/thumbnail")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_album_list_page(self):
        """相册列表页面检查点"""
        locator = (By.ID, "com.meizu.media.gallery:id/album_cover")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_elements(*locator))
            return True
        except:
            return False

    # 第一页面
    @teststep
    def click_album(self):
        """进入相册tab"""
        print('进入相册列表页')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'相册')]") \
            .click()

    @teststep
    def wait_check_all_picture_page(self):
        """所有图片 的为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text, '所有图片')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def open_album(self):
        """打开 第一个相册"""
        print('选择相册')
        self.driver \
            .find_elements_by_id("com.meizu.media.gallery:id/album_name")[0] \
            .click()

    # 第二页面  检查点用 wait_check_album_list_page()
    @teststep
    def choose_image(self):
        """选择相册图片"""
        print('选择照片')
        self.driver.find_elements_by_id('com.meizu.media.gallery:id/thumbnail')[0].click()

    # 第三页面
    @teststep
    def wait_check_photo_page(self):
        """ 确定 按钮 的resource-id为依据"""
        locator = (By.ID, "com.meizu.media.gallery:id/fragment_container")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def commit_button(self):
        """相册确定按钮"""
        print('点击 确定按钮')
        self.driver \
            .find_element_by_xpath("//android.widget.TextView[contains(@text,'确定')]") \
            .click()

    @teststep
    def back_up_button(self):
        """相册返回按钮"""
        self.driver \
            .find_element_by_id("android:id/home") \
            .click()


class SimulatorPage(BasePage):
    """夜神模拟器"""

    # 模拟器 5.1
    @teststep
    def wait_check_album_page(self, var=10):
        """以相册title:“选择照片”的text为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'选择照片')]")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def choose_album_mul(self):
        """5.1 模拟器 选择相册370,720"""
        print('选择相册')
        ClickBounds().click_bounds(560, 270)


class HonorPage(BasePage):
    """华为7.0"""

    # 拍照 华为7.0
    @teststeps
    def wait_check_camera_page(self, var=10):
        """以 “拍照键”的resource-id为依据"""
        locator = (By.ID, "com.huawei.camera:id/shutter_button")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 第一页面
    @teststep
    def click_camera_button(self):
        """以相机拍照按钮"""
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.huawei.camera:id/shutter_button") \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.huawei.camera:id/btn_cancel")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id("com.huawei.camera:id/btn_done") \
            .click()

    @teststep
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.huawei.camera:id/btn_cancel") \
            .click()

    # 相册 华为7.0
    @teststep
    def wait_check_album_page(self, var=10):
        """相册 的resource-id为依据"""
        locator = (By.ID, "com.android.gallery3d:id/album_name")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def open_album(self):
        """打开 第二个相册"""
        print('进入相册')
        self.driver \
            .find_elements_by_id("com.android.gallery3d:id/album_name")[1] \
            .click()

    @teststep
    def wait_check_picture_page(self, var=10):
        """选择图片 的为依据"""
        locator = (By.ID, "com.android.gallery3d:id/head_actionmode_title")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


class PixelPage(BasePage):
    """Pixel 8.1"""
    # 拍照
    @teststep
    def wait_check_camera_page(self, var=10):
        """选择图片 的为依据"""
        locator = (By.ID, "com.google.android.GoogleCamera:id/camera_switch_button")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 第一页面
    @teststep
    def click_retake_button(self):
        """相机'切换前置后置摄像头'按钮"""
        print('切换前置后置摄像头')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/camera_switch_button") \
            .click()

    @teststep
    def click_camera_button(self):
        """以相机拍照按钮"""
        print('点击 拍照按钮')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/center_placeholder") \
            .click()

    @teststep
    def cancel_button(self):
        """以相机  左上角 取消按钮"""
        print('点击 取消按钮')
        self.driver \
            .find_elements_by_class_name("android.view.View")[1] \
            .click()

    # 第二页面
    @teststeps
    def wait_check_retake_page(self, var=10):
        """以 “”的resource-id为依据"""
        locator = (By.ID, "com.google.android.GoogleCamera:id/retake_button")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def click_done_button(self):
        """相机'完成'按钮"""
        print('点击 完成按钮')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/shutter_button") \
            .click()

    @teststep
    def click_retake_button(self):
        """相机'retake'按钮"""
        print('点击 重拍按钮')
        self.driver \
            .find_element_by_id("com.google.android.GoogleCamera:id/retake_button") \
            .click()

    # 相册
    @teststep
    def wait_check_album_page(self, var=10):
        """相册 的resource-id为依据"""
        locator = (By.ID, "com.google.android.apps.photos:id/title")
        try:
            WebDriverWait(self.driver, var, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def open_album(self):
        """打开 第二个相册"""
        print('选择相册')
        self.driver \
            .find_elements_by_id("com.google.android.apps.photos:id/title")[2] \
            .click()

    @teststep
    def wait_check_picture_page(self):
        """图片 的class_name为依据"""
        locator = (By.CLASS_NAME, "android.view.ViewGroup")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    # 权限询问页面
    @teststep
    def wait_check_permission_page(self):
        """ 的id为依据"""
        locator = (By.ID, "com.android.packageinstaller:id/permission_message")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def permission_allow_button(self):
        """允许 按钮"""
        self.driver \
            .find_element_by_id("com.android.packageinstaller:id/permission_allow_button") \
            .click()


class ChangeImage(BasePage):
    """更换头像功能所有控件信息
        之所以在这里定义,是为了避免每次调用click_bounds()时，再次计算坐标"""
    def __init__(self):
        self.meizu = MeizuPage()
        self.simu = SimulatorPage()
        self.honor = HonorPage()
        self.pixel = PixelPage()

    @teststeps
    def pixel_permission_allow(self):
        """ Pixel 拍照权限"""
        if self.pixel.wait_check_permission_page():
            self.pixel.permission_allow_button()  # 允许 按钮

    @teststeps
    def album_upload_save(self):
        """相册 上传照片 正常流程"""
        print('-------------相册修改---------------')
        if self.simu.wait_check_album_page():  # 5.1模拟器
            self.simu.choose_album_mul()  # 选择相册
            time.sleep(2)
            self.meizu.choose_image()  # 选择照片
            if self.meizu.wait_check_save_page():
                self.meizu.click_save_button()  # 完成 按钮
        elif self.honor.wait_check_album_page():  # 真机 华为7.0
            self.honor.open_album()  # 进入某相册
            if self.honor.wait_check_picture_page():
                self.meizu.choose_image()  # 选择照片
                if self.meizu.wait_check_save_page():
                    self.meizu.click_save_button()  # 完成按钮
        elif self.meizu.wait_check_album_page():  # 真机 魅族5.1
            self.meizu.click_album()  # 进入相册列表页
            if self.meizu.wait_check_album_list_page():
                self.meizu.open_album()  # 选择某相册
                if self.meizu.wait_check_album_page():
                    self.meizu.choose_image()  # 选择照片
                    if self.meizu.wait_check_photo_page():
                        self.meizu.commit_button()  # 确定按钮
                        if self.meizu.wait_check_save_page():
                            self.meizu.click_save_button()  # 完成按钮

        elif self.pixel.wait_check_album_page():  # 真机 Pixel
            self.pixel.open_album()  # 进入某相册
            if self.pixel.wait_check_picture_page():
                self.meizu.choose_image()  # 选择照片
                if self.meizu.wait_check_save_page():
                    self.meizu.click_save_button()  # 完成按钮

    @teststeps
    def album_upload_cancel(self):
        """相册 上传照片 - 取消"""
        print('------------取消相册修改--------------')
        if self.simu.wait_check_album_page():  # 5.1模拟器
            self.simu.choose_album_mul()  # 选择相册
            time.sleep(2)
            self.meizu.choose_image()  # 选择照片
            if self.meizu.wait_check_save_page():
                self.meizu.click_cancel_button()  # 取消 按钮
        elif self.honor.wait_check_album_page():  # 真机 华为7.0
            self.honor.open_album()  # 进入某相册
            if self.honor.wait_check_picture_page():
                self.meizu.choose_image()  # 选择照片
                if self.meizu.wait_check_save_page():
                    self.meizu.click_cancel_button()  # 取消按钮
        elif self.meizu.wait_check_album_page():  # 真机 魅族5.1
            self.meizu.click_album()   # 进入相册列表页
            if self.meizu.wait_check_album_list_page():
                self.meizu.open_album()  # 选择某相册
                if self.meizu.wait_check_album_page():
                    self.meizu.choose_image()  # 选择照片
                    if self.meizu.wait_check_photo_page():
                        self.meizu.commit_button()  # 确定按钮
                        if self.meizu.wait_check_save_page():
                            self.meizu.click_cancel_button()  # 取消按钮
        elif self.pixel.wait_check_album_page():  # 真机 Pixel
            self.pixel.open_album()  # 进入某相册
            if self.pixel.wait_check_picture_page():
                self.meizu.choose_image()  # 选择照片
                if self.meizu.wait_check_save_page():
                    self.meizu.click_cancel_button()  # 取消按钮

    @teststeps
    def photo_upload_save(self):
        """拍照 上传照片 正常保存"""
        print('-------------拍照修改---------------')
        if self.meizu.wait_check_camera_page():  # 真机 魅族5.1
            self.meizu.click_camera_button()  # 拍照键
            if self.meizu.wait_check_retake_page():
                self.meizu.click_done_button()  # 完成按钮
                if self.meizu.wait_check_save_page():
                    self.meizu.click_save_button()  # 保存按钮
                    return True
        elif self.honor.wait_check_camera_page():  # 真机 华为7.0
            self.honor.click_camera_button()  # 拍照键
            if self.honor.wait_check_retake_page():
                self.honor.click_done_button()  # 完成按钮
                if self.meizu.wait_check_save_page():
                    self.meizu.click_save_button()  # 保存按钮
                    return True
        elif self.pixel.wait_check_camera_page():  # 真机 Pixel
            self.pixel.click_camera_button()  # 拍照键
            if self.pixel.wait_check_retake_page():
                self.pixel.click_done_button()  # 完成按钮
                return True
        else:  # 模拟器 5.1
            return False

    @teststeps
    def photo_upload_cancel(self):
        """拍照 上传照片- 取消"""
        print('------------取消拍照修改--------------')
        if self.meizu.wait_check_camera_page():  # 真机 魅族5.1
            self.meizu.click_camera_button()  # 拍照按钮
            if self.meizu.wait_check_retake_page():
                self.meizu.click_done_button()  # 完成按钮
                if self.meizu.wait_check_save_page():
                    self.meizu.click_cancel_button()  # 取消按钮
                    return True
        elif self.honor.wait_check_camera_page():  # 真机 华为7.0
            self.honor.click_camera_button()  # 拍照按钮
            if self.honor.wait_check_retake_page():
                self.honor.click_done_button()  # 完成按钮
                if self.meizu.wait_check_save_page():
                    self.meizu.click_cancel_button()  # 取消按钮
                    return True
        elif self.pixel.wait_check_camera_page():  # 真机 Pixel
            self.pixel.cancel_button()  # 取消按钮
            return True
        else:  # 模拟器 5.1
            return False

    @teststeps
    def photo_upload_retake(self):
        """拍照 上传照片 -重拍"""
        print('-------------重拍修改---------------')
        if self.meizu.wait_check_camera_page():  # 真机 魅族5.1
            self.meizu.click_camera_button()  # 拍照键
            if self.meizu.wait_check_retake_page():
                self.meizu.click_retake_button()  # 重拍 按钮

                if self.meizu.wait_check_camera_page():
                    self.meizu.click_camera_button()  # 拍照键
                    if self.meizu.wait_check_retake_page():
                        self.meizu.click_done_button()  # 完成 按钮
                        if self.meizu.wait_check_save_page():
                            self.meizu.click_save_button()  # 保存 按钮
                            return True
        elif self.honor.wait_check_camera_page():  # 真机 华为7.0
            self.honor.click_camera_button()  # 拍照按钮
            if self.honor.wait_check_retake_page():
                self.honor.click_retake_button()  # 重拍 按钮

                if self.honor.wait_check_camera_page():
                    self.honor.click_camera_button()  # 拍照按钮
                    if self.honor.wait_check_retake_page():
                        self.honor.click_done_button()  # 完成 按钮
                        if self.meizu.wait_check_save_page():
                            self.meizu.click_save_button()  # 保存按钮
                            return True
        elif self.pixel.wait_check_camera_page():  # 真机 Pixel
            self.pixel.click_camera_button()  # 拍照键
            if self.pixel.wait_check_retake_page():
                self.pixel.click_retake_button()  # 重拍按钮

                if self.pixel.wait_check_camera_page():  # 真机 Pixel
                    self.pixel.click_camera_button()  # 拍照按钮
                    if self.pixel.wait_check_retake_page():
                        self.pixel.click_done_button()  # 完成按钮
                return True
        else:  # 模拟器 5.1
            return False

