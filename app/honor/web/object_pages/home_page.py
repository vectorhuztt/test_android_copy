#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/8/20 11:49
# -----------------------------------------
import time

from selenium.webdriver.common.by import By

from conf.base_web import BaseDriverPage
from conf.decorator import teststep
from utils.wait_element import WaitElement


class WebHomePage(BaseDriverPage):
    wait = WaitElement()

    @teststep
    def wait_check_home_page(self):
        """首页页面检查点"""
        locator = (By.ID, 'logo')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_test_class_page(self):
        """测试班级页面检查点 """
        locator = (By.XPATH, '//*[contains(text(),"MVP")]')
        return self.wait.wait_check_element(locator, timeout=5)


    @teststep
    def wait_check_tips_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-dialog__header')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_no_more_remind_page(self):
        """首页页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-checkbox__input')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_empty_blanket_page(self):
        """题筐为空页面检查点"""
        time.sleep(2)
        locator = (By.CSS_SELECTOR, '.testbank-list .empty-block')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_delete_tip_page(self):
        time.sleep(2)
        locator = (By.CLASS_NAME, 'el-message-box__content')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_class_page(self):
        """单词本页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(), "布置日期")]')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_blanket_page(self):
        """题筐页面检查点"""
        time.sleep(2)
        locator = (By.XPATH, '//*[contains(text(), "生成试卷")]')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def wait_check_assign_homework_page(self):
        """布置试卷/作业页面检查点"""
        time.sleep(2)
        locator = (By.ID, 'homework-student-list-box')
        return self.wait.wait_check_element(locator, timeout=5)

    @teststep
    def click_logo(self):
        """点击在线助教logo"""
        locator = (By.ID, 'logo')
        self.wait.wait_find_element(locator).click()
        time.sleep(2)

    @teststep
    def blanket_tab(self):
        """题筐tab"""
        locator = (By.CSS_SELECTOR, '.head-container a[href$=testbank-cart]')
        return self.wait.wait_find_element(locator)

    @teststep
    def blanket_bank_num(self):
        """题筐内的题数"""
        locator = (By.CSS_SELECTOR, '.head-container a[href$=testbank-cart] .highlight')
        ele = self.wait.wait_find_element(locator)
        print('题筐内题数：', ele.text)
        return int(ele.text)

    @teststep
    def no_more_remind_checkbox(self):
        """不在题型按钮"""
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-checkbox__input')
        return self.wait.wait_find_element(locator)

    @teststep
    def tip_content(self):
        """提示内容"""
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) .el-dialog__body')
        return self.wait.wait_find_element(locator).text

    @teststep
    def delete_tip_content(self):
        """删除提示内容"""
        locator = (By.CSS_SELECTOR, '.el-message-box__message')
        return self.wait.wait_find_element(locator).text

    @teststep
    def click_confirm_delete_btn(self):
        """点击删除提示的确定按钮"""
        locator = (By.CSS_SELECTOR, '.el-message-box__btns .el-button--primary')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_no_more_tip(self):
        """不再提醒"""
        locator = (By.CSS_SELECTOR, '.el-checkbox__input .el-checkbox__original')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_confirm_btn(self):
        """点击确定按钮"""
        locator = (By.CSS_SELECTOR, '.el-dialog__wrapper:not([style="display: none;"]) '
                                    '.dialog-footer .el-button--primary')
        self.wait.wait_find_element(locator).click()

    @teststep
    def select_test_class(self):
        """选择测试班级"""
        locator = (By.CSS_SELECTOR, '.vanclass-list li:last-child .el-checkbox__inner')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_more_class(self):
        """更多班级"""
        locator = (By.CSS_SELECTOR, '.toggle-link')
        self.wait.wait_find_element(locator).click()

    @teststep
    def click_test_class(self):
        """点击测试班级"""
        locator = (By.CSS_SELECTOR, '#class-list a:last-child')
        self.wait.wait_find_element(locator).click()

    @teststep
    def homework_name(self):
        """作业名称"""
        locator = (By.CSS_SELECTOR, '.table-list .homework-name')
        return self.wait.wait_find_elements(locator)

    @teststep
    def delete_btn(self):
        """删除按钮"""
        locator = (By.CSS_SELECTOR, '.controls .icon-cross')
        return self.wait.wait_find_elements(locator)

    @teststep
    def mine_bank_pool(self):
        """我的题库"""
        locator = (By.CSS_SELECTOR, '.list a[href$="myresource"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def library_icon(self):
        """图书馆图标"""
        locator = (By.CSS_SELECTOR, '.list a[href$="library"]')
        return self.wait.wait_find_element(locator)

    @teststep
    def mine_pool_bank_type_tab(self):
        """我的题库上方题型tab按钮"""
        locator = (By.CSS_SELECTOR, '.tab-group .tab')
        return self.wait.wait_find_elements(locator)

    @teststep
    def mine_pool_like_or_my_tab(self):
        """我的题库中收藏或者我的tab"""
        locator = (By.CSS_SELECTOR, '.page-container a')
        return self.wait.wait_find_elements(locator)

    @teststep
    def tag_list(self):
        """标签列表"""
        locator = (By.CSS_SELECTOR, '.tag-wrapper .tag')
        return self.wait.wait_find_elements(locator)

    @teststep
    def select_all_checkbox(self):
        """全选按钮"""
        locator = (By.CSS_SELECTOR, 'thead .el-checkbox')
        return self.wait.wait_find_element(locator)

    @teststep
    def blanket_page_select_all_checkbox(self):
        """题筐页面全选按钮"""
        locator = (By.CSS_SELECTOR, '.content .el-checkbox')
        return self.wait.wait_find_element(locator)

    @teststep
    def join_blanket(self):
        """加入题筐按钮"""
        locator = (By.CSS_SELECTOR, '.head-banner-container .controls .el-button')
        return self.wait.wait_find_element(locator)

    @teststep
    def multi_like_or_delete_btn(self):
        """批量删除或者收藏按钮"""
        locator = (By.CSS_SELECTOR, '.content .item')
        return self.wait.wait_find_elements(locator)

    @teststep
    def bank_control_btn(self):
        """生成试卷/题单/作业按钮"""
        locator = (By.CSS_SELECTOR, '.controls .el-button')
        return self.wait.wait_find_elements(locator)

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

