import time

from app.honor.student.login.test_data.account import VALID_ACCOUNT
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from app.honor.student.word_book_rebuild.object_page.wordbook_public_page import WorldBookPublicPage
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast


class LoginPage(BasePage):

    @teststeps
    def wait_check_page(self):
        """以“登录按钮”的xpath@text为依据"""
        locator = (By.ID, '{}btn_login'.format(self.id_type()))
        try:
            WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def input_username(self):
        """以“请输入手机号码”的TEXT为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "ed_user_nickname")
        return ele

    @teststep
    def input_password(self):
        """以“请输入登录密码”的XPATH为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "ed_user_pwd")
        return ele

    @teststep
    def login_button(self):
        """以“登录”Button的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + "btn_login") \
            .click()

    @teststep
    def register_button(self):
        """以“注册帐号”的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + 'register') \
            .click()

    @teststep
    def remember_password(self):
        """以“显示密码”的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + 'pwd_visible') \
            .click()

    @teststep
    def visible_password(self):
        """以“显示密码”的ID为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + 'pwd_visible')
        return ele

    @teststep
    def forget_password(self):
        """以“忘记密码？”的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + 'forget_pwd') \
            .click()

    # 注册
    @teststeps
    def wait_check_register_page(self):
        """以下一步的id作为依据"""
        locator = (By.ID, "{}next".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_not_receive_code_page(self):
        """没有接收到验证码页面提示"""
        locator = (By.ID, "{}voice_verify".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_resend_page(self):
        """时间过后出现重新发送按钮"""
        locator = (By.XPATH, "//android.widget.Button[contains(@text,'重新发送')]")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststeps
    def wait_check_register_nick_page(self):
        """以注册的id作为依据"""
        locator = (By.ID, "{}register".format(self.id_type()))
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_protocol_content_page(self):
        """协议内容页面检查点"""
        locator = (By.ID, "com.android.browser:id/webview_wrapper")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def wait_check_switch_page(self):
        locator = (By.ACCESSIBILITY_ID, "注册协议")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def switch_tab(self):
        """切换窗口按钮"""
        ele = self.driver.find_element_by_id('com.android.browser:id/tab_switcher')
        return ele

    @teststep
    def close_web_tab_btn(self):
        """关闭网页"""
        ele = self.driver.find_element_by_id('com.android.browser:id/closetab')
        return ele

    @teststep
    def input_nickname(self):
        """以“请设置昵称”的id为依据"""
        ele = self.driver.find_element_by_id("{}nick_name".format(self.id_type()))
        return ele

    # 忘记密码
    @teststeps
    def wait_check_forget_page(self):
        """以title:找回密码 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'找回密码')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def input_phone(self):
        """以“请输入手机号码”的id为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "phone")
        return ele

    @teststep
    def input_code(self):
        """以“请输入 验证码”的id为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + "code")
        return ele

    @teststep
    def get_code_button(self):
        """以“获取验证码 按钮”的ID为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + 'count_time')
        return ele

    @teststep
    def next_button(self):
        """以“下一步 按钮”的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + 'next') \
            .click()

    @teststep
    def back_login_button(self):
        """以“返回登录 按钮”的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + 'back_login') \
            .click()

    @teststeps
    def wait_check_reset_page(self):
        """以title:找回密码 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'找回密码')]")
        try:
            WebDriverWait(self.driver, 20, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    @teststep
    def protocol(self):
        ele = self.driver.find_element_by_id('{}protocol'.format(self.id_type()))
        return ele

    @teststep
    def new_pwd(self):
        """以“请输入 新密码”的id为依据"""
        ele = self.driver \
            .find_element_by_id("{}pwd".format(self.id_type()))
        return ele

    @teststep
    def new_pwd_confirm(self):
        """以“再次确认 新密码”的ID为依据"""
        ele = self.driver \
            .find_element_by_id(self.id_type() + 'pwd_confirm')
        return ele

    @teststep
    def reset_button(self):
        """以“重置 按钮”的ID为依据"""
        self.driver \
            .find_element_by_id(self.id_type() + 'reset') \
            .click()

    @teststep
    def hide_keyboard(self):
        """['com.baidu.input_huawei/.ImeService',
        'com.android.inputmethod.latin/.LatinIME',
        'com.nuance.swype.emui/com.nuance.swype.input.HuaweiIME',
        'io.appium.android.ime/.UnicodeIME']"""

        time.sleep(2)
        # ClickBounds().click_bounds(664, 709)
        #  os.system("adb shell ime set io.appium.android.ime/.UnicodeIME")
        a = self.driver.active_ime_engine
        print('当前输入法是：' + a)
        # self.driver.deactivate_ime_engine()
        # self.driver.activate_ime_engine('com.android.inputmethod.latin/.LatinIME')
        # a = self.driver.active_ime_engine
        # print('当前输入法是：' + a)
        self.driver.hide_keyboard()

    @teststeps
    def login_operate(self, stu_account, stu_password):
        """登录"""
        print('在登录界面：')
        time.sleep(2)
        phone = self.input_username()
        pwd = self.input_password()

        phone.send_keys(stu_account)
        pwd.send_keys(stu_password)
        self.login_button()
        time.sleep(2)

    @teststeps
    def app_status(self, stu_account=VALID_ACCOUNT.account(), stu_password=VALID_ACCOUNT.password()):
        """判断应用当前状态"""
        activity = self.wait_activity()
        if self.wait_check_page():  # 在登录界面
            self.login_operate(stu_account, stu_password)

        elif HomePage().wait_check_home_page():  # 在主界面
            print('主界面')

        elif WorldBookPublicPage().wait_check_game_title_page():
            print('做题页面')

        elif activity == '':  # 崩溃退出
            self.launch_app()  # 重启APP
            if HomePage().wait_check_home_page():  # 在主界面
                print('主界面')
            elif self.wait_check_page():  # 在登录界面
                self.login_operate(stu_account, stu_password)
        else:
            print('在其他页面')
            self.close_app()  # 关闭APP
            self.launch_app()  # 重启APP
            if HomePage().wait_check_home_page():  # 在主界面
                print('主界面')
            elif self.wait_check_page():  # 在登录界面
                self.login_operate(stu_account, stu_password)

    @teststeps
    def enter_user_info_page(self):
        """由 主界面 进入个人信息页"""
        if HomePage().wait_check_home_page():
            HomePage().click_tab_profile()  # 进入首页后点击‘个人中心’按钮
            if UserCenterPage().wait_check_user_center_page():
                UserCenterPage().click_avatar_profile()  # 点击登录头像按钮，进行个人信息操作

    @teststep
    def launch_app(self):
        """Start on the device the application specified in the desired capabilities.
        """
        self.driver.launch_app()
        time.sleep(5)

    @teststep
    def close_app(self):
        """Close on the device the application specified in the desired capabilities.
        """
        self.driver.close_app()

    @teststep
    def remove_app(self):
        """Remove on the device the application
        """
        self.driver.remove_app("com.vanthink.student.debug")

    @teststep
    def is_app_installed(self):
        """Check app was installed on the device the application
        """
        self.driver.is_app_installed("com.vanthink.student.debug")

    @teststep
    def install_app(self):
        """Remove on the device the application
        """
        self.driver.install_app('../student_debug_1.2.7.apk')
        print('安装APP')

    @teststep
    def verification_code_operate(self, phone, operate_type):
        """验证码操作"""
        value = 0
        for j in range(2):
            if j == 1:
                self.get_code_button().click()  # 获取验证码 按钮
            value = verify_find(phone, operate_type)  # 获取验证码
            if self.get_code_button().get_attribute('enabled') == "true":
                print('❌❌❌ 获取验证码按钮未置灰！')
            if operate_type == 'register':
                if not self.wait_check_not_receive_code_page():
                    print('❌❌❌ 未发现收不到验证码信息提示！')
            if j == 0:
                time.sleep(60)
                if not self.wait_check_resend_page():
                    print('❌❌❌ 按钮未变为重新发送')
                if self.wait_check_not_receive_code_page():
                    print('❌❌❌ 发送语音验证码提示未消失')
        return value

    @teststep
    def send_code_operate(self, value):
        print('验证码：', value)
        code = self.input_code()
        code.send_keys('00')
        self.next_button()  # 下一步 按钮

        if not Toast().find_toast('验证码验证失败'):
            print("❌❌❌ 未发现验证码验证失败信息提示！")

        code.send_keys(value)  # 输入 验证码
        self.next_button()  # 下一步 按钮