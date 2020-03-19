#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/20 11:49
# -----------------------------------------
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.honor.web.object_pages.base import BaseDriverPage
from conf.decorator import teststep


class WebHomePage(BaseDriverPage):
    @teststep
    def wait_check_home_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.ID, 'logo')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_test_class_page(self):
        """测试班级页面检查点 """
        locator = (By.XPATH, '//*[contains(text(),"MVP")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    @teststep
    def wait_check_tips_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-dialog__header')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_no_more_remind_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-checkbox__input')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_empty_blanket_page(self):
        """题筐为空页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.testbank-list .empty-block')
        try:
            WebDriverWait(self.driver, 15, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_delete_tip_page(self):
        time.sleep(2)
        locator = (By.CLASS_NAME, 'el-message-box__content')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_class_page(self):
        """单词本页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(), "布置日期")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @teststep
    def wait_check_blanket_page(self):
        """题筐页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(), "生成试卷")]')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    @teststep
    def wait_check_assign_homework_page(self):
        """布置试卷/作业页面检查点"""
        time.sleep(2)
        locator = (By.ID, 'homework-student-list-box')
        try:
            WebDriverWait(self.driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False


    @teststep
    def click_logo(self):
        """点击在线助教logo"""
        self.driver.find_element_by_id('logo').click()
        time.sleep(2)

    @teststep
    def blanket_tab(self):
        """题筐tab"""
        ele = self.driver.find_element_by_css_selector('.head-container a[href$=testbank-cart]')
        return ele

    @teststep
    def blanket_bank_num(self):
        """题筐内的题数"""
        ele = self.driver.find_element_by_css_selector('.head-container a[href$=testbank-cart] .highlight')
        print('题筐内题数：', ele.text)
        return int(ele.text)

    @teststep
    def no_more_remind_checkbox(self):
        """不在题型按钮"""
        ele = self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style="display: none;"]) .el-checkbox__input')
        return ele

    @teststep
    def tip_content(self):
        """提示内容"""
        ele = self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style="display: none;"]) .el-dialog__body')
        return ele.text

    @teststep
    def delete_tip_content(self):
        """删除提示内容"""
        ele = self.driver.find_element_by_css_selector('.el-message-box__message')
        return ele.text

    @teststep
    def click_confirm_delete_btn(self):
        """点击删除提示的确定按钮"""
        self.driver.find_element_by_css_selector('.el-message-box__btns .el-button--primary').click()

    @teststep
    def click_no_more_tip(self):
        """不再提醒"""
        self.driver.find_element_by_css_selector('.el-checkbox__input .el-checkbox__original').click()

    @teststep
    def click_confirm_btn(self):
        """点击确定按钮"""
        self.driver.find_element_by_css_selector('.el-dialog__wrapper:not([style="display: none;"]) '
                                                 '.dialog-footer .el-button--primary').click()

    @teststep
    def select_test_class(self):
        """选择测试班级"""
        self.driver.find_element_by_css_selector('.vanclass-list li:last-child .el-checkbox__inner').click()
        time.sleep(1)

    @teststep
    def click_more_class(self):
        """更多班级"""
        self.driver.find_element_by_css_selector('.toggle-link').click()
        time.sleep(1)

    @teststep
    def click_test_class(self):
        """点击测试班级"""
        self.driver.find_element_by_css_selector('#class-list a:last-child').click()
        time.sleep(2)

    @teststep
    def homework_name(self):
        """作业名称"""
        ele = self.driver.find_elements_by_css_selector('.table-list .homework-name')
        return ele

    @teststep
    def delete_btn(self):
        """删除按钮"""
        ele = self.driver.find_element_by_css_selector('.controls .icon-cross')
        return ele

    @teststep
    def mine_bank_pool(self):
        """我的题库"""
        ele = self.driver.find_element_by_css_selector('.list a[href$="myresource"]')
        return ele

    @teststep
    def library_icon(self):
        """图书馆图标"""
        ele = self.driver.find_element_by_xpath('.list a[href$="library"]')
        return ele

    @teststep
    def mine_pool_bank_type_tab(self):
        """我的题库上方题型tab按钮"""
        ele = self.driver.find_elements_by_css_selector('.tab-group .tab')
        return ele

    @teststep
    def mine_pool_like_or_my_tab(self):
        """我的题库中收藏或者我的tab"""
        ele = self.driver.find_elements_by_css_selector('.page-container a')
        return ele

    @teststep
    def tag_list(self):
        """标签列表"""
        ele = self.driver.find_elements_by_css_selector('.tag-wrapper .tag')
        return ele

    @teststep
    def select_all_checkbox(self):
        """全选按钮"""
        ele = self.driver.find_element_by_css_selector('thead .el-checkbox')
        return ele

    @teststep
    def blanket_page_select_all_checkbox(self):
        """题筐页面全选按钮"""
        ele = self.driver.find_element_by_css_selector('.content .el-checkbox')
        return ele

    @teststep
    def join_blanket(self):
        """加入题筐按钮"""
        ele = self.driver.find_element_by_css_selector('.head-banner-container .controls .el-button')
        return ele

    @teststep
    def multi_like_or_delete_btn(self):
        """批量删除或者收藏按钮"""
        ele = self.driver.find_elements_by_css_selector('.content .item')
        return ele

    @teststep
    def bank_control_btn(self):
        """生成试卷/题单/作业按钮"""
        ele = self.driver.find_elements_by_css_selector('.controls .el-button')
        return ele

    @teststep
    def select_test_class_operate(self):
        """选择测试班级操作"""
        if not self.wait_check_test_class_page():
            self.click_more_class()
            time.sleep(1)
        self.click_test_class()

    @teststep
    def tips_operate(self):
        """提示信息处理"""
        if self.wait_check_tips_page():
            print(self.tip_content(), '\n')
            if self.wait_check_no_more_remind_page():
                self.no_more_remind_checkbox().click()
            self.click_confirm_btn()
            time.sleep(2)


    @teststep
    def tip_box_operate(self):
        """删除作业提示处理"""
        if self.wait_check_delete_tip_page():
            print(self.delete_tip_content(), '\n')
            self.click_confirm_delete_btn()
            time.sleep(5)

