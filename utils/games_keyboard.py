#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from conf.base_page import BasePage
from conf.decorator import teststeps, teststep


class Keyboard(BasePage):
    """小键盘 q w e等"""

    @teststep
    def keyboard_view(self):
        """小键盘 整体view元素"""
        keyboard = self.driver.find_element_by_xpath('//android.view.View[contains(@resource-id, "keyboard")]')
        return keyboard

    @teststeps
    def games_keyboard(self, key):
        """说明见方法后"""
        keyboard = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                    'capslock', 'z', 'x', 'c', 'v', 'b', 'n', 'm', "backspace",
                    ',', '.', '-', 'blank', "'", 'enter']

        if key.lower() in keyboard:
            screen = self.get_window_size()  # 获取当前手机屏幕大小X,Y
            loc = self.get_element_location(self.keyboard_view())  # 键盘view左上角 顶点坐标
            height = int(screen[1]) - int(loc[1])  # 键盘view高度

            i = keyboard.index(key.lower())
            if i < 10:
                x = 0.08888 * screen[0] * (i+0.5) + 0.00925 * screen[0]*(i+1)
                y = loc[1] + (height/8)
            elif i in range(10, 19):
                x = (0.08888+0.00925) * screen[0] * (i - 9)  # i +1-10
                y = loc[1] + (height/8)*(1+1*2)
            elif i in range(19, 28):
                x = (0.08888+0.00925) * screen[0] * (i - 18)  # i+1-19
                y = loc[1] + (height/8)*(1+2*2)
            else:  # 27--32
                if i > 30:
                    x = 0.08888 * screen[0] * (i-25+0.5) + 0.00925 * screen[0]*(i - 23)  # i-28
                    y = loc[1] + (height/8)*(1+3*2)
                else:
                    x = 0.08888 * screen[0] * (i - 28 + 0.5) + 0.00925 * screen[0] * (i - 27)  # i-28
                    y = loc[1] + (height/8)*(1+3*2)

            self.driver.tap([(x, y)])

    """小键盘
    第一行： # 点击按钮中心点： 0.08888 * screen[0] * (i+0.5)
            # 按钮间隔： 0.00925 * screen[0]*(i+1)
            # y值：loc[1] + (height/8)*(1+0*2)
    第二行： # 第一个按钮之前有缩进（按钮宽度的一半） + 点击按钮中心点：0.08888 * screen[0] * (i +0.5+0.5 - 10)
            # 按钮间隔： 0.00925 * screen[0] * (i + 1 - 10)
            # y值：loc[1] + (height/8)*(1+1*2)
    第三行：  # 第一个按钮宽度变为普通按钮的3/2倍 + 点击按钮中心点：0.08888 * screen[0] * (i +0.5+0.5 - 19)
            # 按钮间隔： 0.00925 * screen[0] * (i + 1 - 19)
            # y值：loc[1] + (height/8)*(1+2*2)
    第四行：
            ！i> 30: 因为空格键占四个按钮的宽度，故:
                    # 点击按钮中心点：0.08888 * screen[0] * (i-25+0.5)
                    # 按钮间隔：0.00925 * screen[0]*(i - 23)
            ! i< 31:  # 点击按钮中心点：0.08888 * screen[0] * (i + 0.5 - 28) 
                     # 按钮间隔：0.00925 * screen[0] * (i +1 - 28)
            # y值：loc[1] + (height/8)*(1+3*2)
    """

    @teststeps
    def dp_to_px(self, y):
        """dp转换成px的系数关系
            ldpi      320*240     1dp=0.75px 
            mdpi       480*320     1dp=1.0px 
            hdpi       800*480     1dp=1.5px 
            xhdpi       1280*720    1dp=2.0px 
            xxhdpi       1920*1080   1dp=3px 
        """
        a = 1  # y == 480
        if y == 1920:
            a = 3
        elif y == 1280:
            a = 2
        elif y == 800:
            a = 1.5
        elif y == 320:
            a = 0.75
        return a

    @teststep
    def keyboard_operate(self, value, word_index):
        """点击键盘 具体操作
            :param value: 单词字母
            :param word_index 单词字母索引值
        """
        if word_index == 3:
            self.games_keyboard('capslock')  # 点击键盘 切换到 大写字母
            self.games_keyboard(value.upper())  # 点击键盘对应 大写字母
            self.games_keyboard('capslock')  # 点击键盘 切换到 小写字母
        else:
            self.games_keyboard(value)  # 点击键盘对应字