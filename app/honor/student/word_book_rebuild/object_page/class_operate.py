#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/6/27 11:52
# -----------------------------------------

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.vanclass.object_page.vanclass_page import VanclassPage
from app.honor.student.word_book_rebuild.test_data.account import STU_ACCOUNT
from conf.base_page import BasePage
from conf.decorator import teststep
from utils.reset_phone_find_toast import verify_find


class QuitAddClass(BasePage):
    def __init__(self):
        self.home = HomePage()
        self.van = VanclassPage()

    @teststep
    def wait_check_vanclass_page(self):
        """班级页面检查点"""
        locator = (By.CLASS_NAME, self.id_type() + "class_name")
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_any_elements_located(locator))
            return True
        except:
            return False

    @teststep
    def class_num(self):
        """班号"""
        ele = self.driver.find_elements_by_id(self.id_type() + 'class_no')
        return ele

    @teststep
    def quit_all_class_operate(self):
        """退出班级操作"""
        self.home.click_test_vanclass()                          # 班级tab
        if self.van.wait_check_page():                           # 班级页面检查点
            self.home.screen_swipe_down(0.5, 0.2, 0.9, 1000)
            while self.wait_check_vanclass_page():
                if self.van.wait_check_page():
                    van_name = self.van.class_name()[0].text
                    self.van.class_name()[0].click()
                    self.quit_tips_operate(van_name)             # 退出班级提示框

    @teststep
    def quit_tips_operate(self, van_name):
        """退出班级 具体操作"""
        if self.van.wait_check_vanclass_page(van_name):    # 页面检查点
            self.van.quit_vanclass()                       # 退出班级 按钮
            self.home.tips_operate_commit()                # 提示框
            print('确定 退出')
            print('------------------------------')
            if self.van.wait_check_quit_page():
                self.van.phone_name()  # 提示
                value = verify_find(STU_ACCOUNT, 'quitClass')  # 获取验证码
                self.van.code_input().send_keys(value)         # 输入验证码
                print(STU_ACCOUNT)
                print('验证码:', value)
                self.van.quit_button()                         # 退出班级 按钮

    @teststep
    def apply_class_operate(self, test_class_num):
        """加入班级操作"""
        self.home.click_test_vanclass()                        # 班级tab
        if self.van.wait_check_page():                         # 班级页面检查点
            if self.van.wait_check_van_list_page():
                class_nums = self.class_num()
                van_names = []
                while len(van_names) < len(class_nums):       # 非测试班级则退出，是则保留
                    for i, num in enumerate(self.class_num()):
                        class_name = self.van.class_name()[i].text
                        van_num = num.text.split('：')[1]
                        if class_name in van_names:
                            continue
                        else:
                            van_names.append(class_name)

                            if van_num not in test_class_num:      # 检验是否已加入测试班级
                                num.click()                         # 不是测试班级的
                                self.quit_tips_operate(class_name)            # 退出班级
                            else:
                                test_class_num.remove(van_num)

            if len(test_class_num):
                for x in test_class_num:
                    if self.van.wait_check_page():
                        self.van.add_class_button()                         # 若没有班级列表
                        if self.home.wait_check_tips_page():     # 页面检查点
                            self.home.input().send_keys(x)       # 输入班级号
                            self.home.commit_button()            # 点击确定按钮
                        if self.van.wait_check_apply_page():
                            print('班级：', self.van.class_name_modify())
                            print('班号：', self.van.apply_vanclass_no())
                            print('老师：', self.van.apply_teacher_name())
                            self.van.remark_name_modify().send_keys('Test')   # 输入昵称
                            self.van.apply_class_button()  # 申请入班 按钮
                        print('-'*30, '\n')
        self.home.click_tab_hw()


