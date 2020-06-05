#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from selenium.webdriver.common.by import By

from conf.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.swipe_screen import SwipeFun


class WaitElement(BasePage):
    """页面检查点 及 等待元素加载"""

    def wait_check_502_or_500_page(self):
        """页面报错重新加载页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@resource-id, "status_error_hint_view") '
                             'and contains(@text, "50")]')
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False


    def wait_check_retry_page(self):
        """页面报错重新加载页面"""
        locator = (By.XPATH, '//android.widget.TextView[contains(@resource-id, "status_error_hint_view") '
                             'and contains(@text, "网络环境较差")]')
        try:
            WebDriverWait(self.driver, 3, 0.5).until(lambda x: x.find_element(*locator))
            return True
        except:
            return False

    def refresh_page_operate(self, locator, timeout, poll, count):
        """页面刷新操作"""
        if count >= 3:
            raise Exception('网络中断，无法查询定位')
        if self.wait_check_502_or_500_page() or self.wait_check_retry_page():
            SwipeFun().swipe_vertical(0.5, 0.3, 0.8)
            return self.wait_check_element(locator=locator, timeout=timeout, poll=poll, count=count + 1)
        else:
            return False

    def wait_check_element(self, locator, timeout=10, poll=0.5, count=0):
        """判断元素是否存在
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :param count: 刷新次数
        :returns: 存在就返回True,不存在就返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return self.refresh_page_operate(locator=locator, timeout=timeout, poll=poll, count=count)

    def wait_find_element(self, locator, timeout=10, poll=0.5, count=0):
        """查找元素并返回元素
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :param count: 页面刷新次数
        :returns: 元素
        """
        try:
            return WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_element(*locator))
        except Exception:
            return self.refresh_page_operate(locator=locator, timeout=timeout, poll=poll, count=count)

    def wait_find_elements(self, locator, timeout=15, poll=0.5, count=0):
        """查找元素并返回元素
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :param count: 刷新次数
        :returns: 元素
        """
        try:
            return WebDriverWait(self.driver, timeout, poll).until(
                EC.presence_of_all_elements_located(locator))
        except Exception:
            return self.refresh_page_operate(locator=locator, timeout=timeout, poll=poll, count=count)

    def wait_until_not_element(self, locator, timeout=15, poll=0.5):
        """判断元素是否已经不存在
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 不存在返回True,存在返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until_not(
                EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False

    def judge_is_clickable(self, locator, timeout=15, poll=0.5):
        """ 判断某个元素中是否可见并且可点击
        :param locator: 元素属性
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 通过判断enabled属性值，返回元素或false
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(
                EC.element_to_be_clickable(locator))
            return True
        except Exception:
            return False

    def judge_is_selected(self, element, timeout=15, poll=0.5):
        """ 判断某个元素是否被选中
        :param element: 元素
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 元素
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(
                EC.element_to_be_selected(element))
            return True
        except Exception:
            return False

    def judge_is_visibility(self, element, timeout=15, poll=0.5):
        """判断元素是否可见
        :param element: 元素
        :param timeout: 最大查找时间
        :param poll: 间隔时间
        :returns: 可见就返回True,不可见就返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(EC.visibility_of(element))
            return True
        except:
            return False

    def judge_is_exists(self, locator, timeout=15, poll=0.5):
        """判断元素是否存在
        :param locator: 元素属性
        :returns: 存在就返回True,不存在就返回False
        """
        try:
            WebDriverWait(self.driver, timeout, poll).until(lambda x: x.find_element(*locator))
            return True
        except Exception:
            return False

    def return_app(self):
        if 'NATIVE' in self.driver.current_context:
            pass
        else:
            contexts = self.driver.contexts
            for i in contexts:
                if 'NATIVE' in i:
                    self.driver.switch_to.context(i)
                    break
