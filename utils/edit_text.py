#!/usr/bin/env python
# encoding:UTF-8  
# @Author  : SUN FEIFEI
import time
from conf.base_page import BasePage
from conf.decorator import teststeps


class DelEditText(BasePage):
    """编辑框 编辑"""

    @teststeps
    def del_text(self, edit_text):
        edit_text.click()  # 激活该文本框
        context = edit_text.get_attribute('text')  # 获取文本框里的内容
        self.edit_text_clear(context)  # 删除文本框中是内容

    @teststeps
    def edit_text_clear(self, text):
        """"
            清除EditText文本框里的内容
            @param:text 要清除的内容
        """
        self.driver.keyevent(123)
        time.sleep(3)
        for i in range(0, len(text)):
            self.driver.keyevent(67)
