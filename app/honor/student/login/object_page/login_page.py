import time


from app.honor.student.login.test_data.account import VALID_ACCOUNT
from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.punch_activity.object_page.punch_page import PunchActivityPage
from app.honor.student.user_center.object_page.user_center_page import UserCenterPage
from selenium.webdriver.common.by import By
from conf.decorator import teststep, teststeps
from conf.base_page import BasePage
from utils.reset_phone_find_toast import verify_find
from utils.toast_find import Toast
from utils.wait_element import WaitElement


class LoginPage(BasePage):
    punch = PunchActivityPage()
    wait = WaitElement()

    @teststeps
    def wait_check_login_page(self):
        """以“登录按钮”的xpath@text为依据"""
        locator = (By.ID, '{}btn_login'.format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def input_username(self):
        """请输入手机号码"""
        locator = (By.ID, "{}ed_user_nickname".format(self.id_type()))
        return self.wait.wait_find_element(locator)


    @teststep
    def input_password(self):
        """请输入登录密码"""
        locator = (By.ID, self.id_type() + "ed_user_pwd")
        return self.wait.wait_find_element(locator)


    @teststep
    def login_button(self):
        """登录按钮"""
        locator = (By.ID, self.id_type() + "btn_login")
        return self.wait.wait_find_element(locator)

    @teststep
    def register_button(self):
        """以“注册帐号”的ID为依据"""
        locator = (By.ID, self.id_type() + 'register')
        self.wait.wait_find_element(locator).click()

    @teststep
    def remember_password(self):
        """以“显示密码”的ID为依据"""
        locator = (By.ID, self.id_type() + 'pwd_visible')
        self.wait.wait_find_element(locator).click()

    @teststep
    def visible_password(self):
        """以“显示密码”的ID为依据"""
        locator = (By.ID, self.id_type() + 'pwd_visible')
        return self.wait.wait_find_element(locator)


    @teststep
    def forget_password(self):
        """以“忘记密码？”的ID为依据"""
        locator = (By.ID, self.id_type() + 'forget_pwd')
        self.wait.wait_find_element(locator).click()

    # 注册
    @teststeps
    def wait_check_register_page(self):
        """以下一步的id作为依据"""
        locator = (By.ID, "{}next".format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_not_receive_code_page(self):
        """没有接收到验证码页面提示"""
        locator = (By.ID, "{}voice_verify".format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_resend_page(self):
        """时间过后出现重新发送按钮"""
        locator = (By.XPATH, "//android.widget.Button[contains(@text,'重新发送')]")
        return self.wait.wait_check_element(locator)

    @teststeps
    def wait_check_register_nick_page(self):
        """以注册的id作为依据"""
        locator = (By.ID, "{}register".format(self.id_type()))
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_protocol_content_page(self):
        """协议内容页面检查点"""
        locator = (By.ID, "com.android.browser:id/webview_wrapper")
        return self.wait.wait_check_element(locator)

    @teststep
    def wait_check_switch_page(self):
        locator = (By.ACCESSIBILITY_ID, "注册协议")
        return self.wait.wait_check_element(locator)

    @teststep
    def switch_tab(self):
        """切换窗口按钮"""
        locator = (By.ID, self.id_type() + 'tab_switcher')
        return self.wait.wait_find_element(locator)

    @teststep
    def close_web_tab_btn(self):
        """关闭网页"""
        locator = (By.ID, 'com.android.browser:id/closetab')
        return self.wait.wait_find_element(locator)

    @teststep
    def input_nickname(self):
        """以“请设置昵称”的id为依据"""
        locator = (By.ID, "{}nick_name".format(self.id_type()))
        return self.wait.wait_find_element(locator)

    # 忘记密码
    @teststeps
    def wait_check_forget_page(self):
        """以title:找回密码 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'找回密码')]")
        return self.wait.wait_check_element(locator)

    @teststep
    def input_phone(self):
        """以“请输入手机号码”的id为依据"""
        locator = (By.ID, self.id_type() + 'phone')
        return self.wait.wait_find_element(locator)

    @teststep
    def input_code(self):
        """以“请输入 验证码”的id为依据"""
        locator = (By.ID, self.id_type() + 'code')
        return self.wait.wait_find_element(locator)

    @teststep
    def get_code_button(self):
        """以“获取验证码 按钮”的ID为依据"""
        locator = (By.ID, self.id_type() + 'count_time')
        return self.wait.wait_find_element(locator)

    @teststep
    def next_button(self):
        """以“下一步 按钮”的ID为依据"""
        locator = (By.ID, self.id_type() + 'next')
        return self.wait.wait_find_element(locator)

    @teststep
    def back_login_button(self):
        """以“返回登录 按钮”的ID为依据"""
        locator = (By.ID, self.id_type() + 'back_login')
        return self.wait.wait_find_element(locator)

    @teststeps
    def wait_check_reset_page(self):
        """以title:找回密码 的TEXT为依据"""
        locator = (By.XPATH, "//android.widget.TextView[contains(@text,'找回密码')]")
        return self.wait.wait_find_element(locator)

    @teststep
    def protocol(self):
        locator = (By.ID, '{}protocol'.format(self.id_type()))
        return self.wait.wait_find_element(locator)

    @teststep
    def new_pwd(self):
        """以“请输入 新密码”的id为依据"""
        locator = (By.ID, self.id_type() + 'pwd')
        return self.wait.wait_find_element(locator)

    @teststep
    def new_pwd_confirm(self):
        """以“再次确认 新密码”的ID为依据"""
        locator = (By.ID, self.id_type() + 'pwd_confirm')
        return self.wait.wait_find_element(locator)

    @teststep
    def reset_button(self):
        """以“重置 按钮”的ID为依据"""
        locator = (By.ID, self.id_type() + 'reset')
        self.wait.wait_find_element(locator).click()

    @teststep
    def handle_punch_activity_alert_tip(self, close_alert):
        """关闭打卡活动页面弹窗"""
        if self.punch.wait_check_alert_punch_tip_page():
            if close_alert:
                self.punch.close_alert_tip().click()
                time.sleep(1)

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
    def login_operate(self, stu_account, stu_password, close_alert):
        """登录"""
        print('在登录界面：')
        time.sleep(2)
        phone = self.input_username()
        pwd = self.input_password()

        phone.send_keys(stu_account)
        pwd.send_keys(stu_password)
        self.login_button().click()
        time.sleep(3)
        self.handle_punch_activity_alert_tip(close_alert)


    @teststeps
    def app_status(self, stu_account=VALID_ACCOUNT.account(), stu_password=VALID_ACCOUNT.password(), close_alert=True):
        """判断应用当前状态"""
        activity = self.wait_activity()
        self.handle_punch_activity_alert_tip(close_alert)

        if self.wait_check_login_page():  # 在登录界面
            self.login_operate(stu_account, stu_password, close_alert)

        elif HomePage().wait_check_home_page():  # 在主界面
            print('主界面')

        elif activity == '':  # 崩溃退出
            self.launch_app()  # 重启APP
            if HomePage().wait_check_home_page():  # 在主界面
                print('主界面')
            elif self.wait_check_login_page():  # 在登录界面
                self.login_operate(stu_account, stu_password, close_alert)
        else:
            print('在其他页面')
            self.close_app()  # 关闭APP
            self.launch_app()  # 重启APP
            self.handle_punch_activity_alert_tip(close_alert)
            if HomePage().wait_check_home_page():  # 在主界面
                print('主界面')
            elif self.wait_check_login_page():  # 在登录界面
                self.login_operate(stu_account, stu_password, close_alert)

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