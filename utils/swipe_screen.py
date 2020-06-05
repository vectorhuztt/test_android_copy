#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author  : SUN FEIFEI
from conf.decorator import teststeps
from conf.base_page import BasePage


class SwipeFun(BasePage):
    """滑屏 操作"""

    @teststeps
    def swipe_horizontal(self, ratio_y, start_x, end_x, steps=1000):
        """
        左/右滑动 y值不变
        :param ratio_y: y坐标系数
        :param start_x: 滑动起点x坐标系数
        :param end_x: 滑动终点x坐标系数
        :param steps: 持续时间ms
        :return: None
        """
        screen = self.get_window_size()
        y = int(screen[1] * ratio_y)
        x1 = int(screen[0] * start_x)
        x2 = int(screen[0] * end_x)
        self.driver.swipe(x1, y, x2, y, steps)

    @teststeps
    def swipe_vertical(self, ratio_x, start_y, end_y, steps=1000):
        """
        上/下滑动 x值不变
        :param ratio_x: x坐标系数
        :param start_y: 滑动起点y坐标系数
        :param end_y: 滑动终点y坐标系数
        :param steps: 持续时间ms
        :return: None
        """
        screen = self.get_window_size()
        x = int(screen[0] * ratio_x)
        y1 = int(screen[1] * start_y)
        y2 = int(screen[1] * end_y)

        self.driver.swipe(x, y1, x, y2, steps)
