import os
import time

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from conf.base_config import GetVariable as gv
from xml.etree.ElementTree import ElementTree
from selenium.common.exceptions import WebDriverException

from utils.get_attribute import GetAttribute


class BasePage(object):
    attr = GetAttribute()

    @classmethod
    def set_assert(cls, base_assert):
        cls.base_assert = base_assert

    def get_assert(self):
        return self.base_assert

    @classmethod
    def set_driver(cls, dri):
        cls.driver = dri

    def get_driver(self):
        return self.driver

    @classmethod
    def id_type(cls):
        return str(gv.ID_TYPE)

    @classmethod
    def set_db(cls, mysql):
        cls.mysql = mysql

    def get_db(self):
        return self.mysql

    def alert_operate(self, accept=True):
        alert = Alert(self.driver)
        print(alert.text)
        alert.accept() if accept else alert.dismiss()

    def click_blank(self):
        self.driver.tap([(self.get_window_size()[0] * 0.5, 100), ])

    def get_window_size(self):
        """获取当前窗口大小"""
        window = self.driver.get_window_size()
        y = window['height']
        x = window['width']
        return x, y

    def click_back_up_button(self):
        """以“返回按钮”的class name为依据"""
        ele = self.driver.find_element_by_xpath("//android.widget.ImageButton[@content-desc='转到上一层级']")
        ele.click()

    def next_button(self):
        """下一步按钮"""
        ele = self.driver.find_element_by_id(self.id_type() + "fab_next")
        return ele

    def wait_activity(self):
        """获取当前窗口活动类"""
        activity = self.driver.current_activity
        return activity

    def page_source_android(self):
        """以“获取page_source”的TEXT为依据"""
        print('打开：', self.driver.page_source)

    def screen_swipe_left(self, a, b, c, steps=0.5):
        """向左侧滑动"""
        screen = self.get_window_size()
        x1 = int(screen[0] * a)
        y1 = int(screen[1] * b)
        x2 = int(screen[0] * c)
        self.driver.swipe(x1, y1, x2, y1, steps)

    def screen_swipe_right(self, a, b, c, steps=0.5):
        """向右侧滑动"""
        screen = self.get_window_size()
        x1 = int(screen[0] * a)
        y1 = int(screen[1] * b)
        x2 = int(screen[0] * c)
        self.driver.swipe(x1, y1, x2, y1, steps)

    def screen_swipe_up(self, a, b, c, steps=0.5):
        """向上/向下滑动"""
        screen = self.get_window_size()
        x1 = int(screen[0] * a)
        y1 = int(screen[1] * b)
        y2 = int(screen[1] * c)
        self.driver.swipe(x1, y1, x1, y2, steps)
        time.sleep(1)

    def screen_swipe_down(self, a, b, c, steps=0.5):
        """向下滑动"""
        screen = self.get_window_size()
        x1 = int(screen[0] * a)
        y1 = int(screen[1] * b)
        y2 = int(screen[1] * c)
        self.driver.swipe(x1, y1, x1, y2, steps)

    def get_element_location(self, ele):
        """获取元素 顶点坐标"""
        x = ele.location['x']
        y = ele.location['y']
        return x, y

    def get_element_size(self, ele):
        """获取元素 width & height"""
        width = ele.size['width']
        height = ele.size['height']
        return width, height

    def is_chinese(self, item):
        """判断一个unicode是否是汉字"""
        if u'\u4e00' <= item <= u'\u9fa5':
            return True
        else:
            return False

    def is_alphabet(self, item):
        """判断一个unicode是否是英文字母"""
        if (u'\u0041' <= item <= u'\u005a') or (u'\u0061' <= item <= u'\u007a'):
            return True
        else:
            return False

    def get_element_bounds(self, element):
        """获取元素 左上角/中心点/右下角的坐标值"""
        loc = self.get_element_location(element)
        size = self.get_element_size(element)
        
        x_left = loc[0]
        y_up = loc[1]
        x_center = loc[0] + size[0] / 2
        y_center = loc[1] + size[1] / 2
        x_right = loc[0] + size[0]
        y_down = loc[1] + size[1]

        return x_left, y_up, x_center, y_center, x_right, y_down

    def swipe_up_ele(self, element=None, steps=10):
        """
        swipe up
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_center
            to_y = y_up
        else:
            x, y = self.get_window_size()
            from_x = 0.5*x
            from_y = 0.5*y
            to_x = 0.5*x
            to_y = 0.25*y

        self.driver\
            .swipe(from_x, from_y, to_x, to_y, steps)

    def swipe_down_ele(self, element=None, steps=10):
        """
        swipe down
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_center
            to_y = y_down
        else:
            x, y = self.get_window_size()
            from_x = 0.5*x
            from_y = 0.5*y
            to_x = 0.5*x
            to_y = 0.75*y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

    def swipe_left_ele(self, element=None, steps=10):
        """
        swipe left
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_left
            to_y = y_center
        else:
            x, y = self.get_window_size()
            from_x = 0.5*x
            from_y = 0.5*y
            to_x = 0.25*x
            to_y = 0.5*y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

    def swipe_right_ele(self, element=None, steps=10):
        """
        swipe right
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self.get_element_bounds(element)

            from_x = x_center
            from_y = y_center
            to_x = x_right
            to_y = y_center
        else:
            x, y = self.get_window_size()
            from_x = 0.5*x
            from_y = 0.5*y
            to_x = 0.75*x
            to_y = 0.5*y

        self.driver. \
            swipe(from_x, from_y, to_x, to_y, steps)

    def _find_element_by_swipe(self, direction, using, value, element=None, steps=10, max_swipe=6):
        times = max_swipe

        stability_width = 0
        stability_height = 0
        for i in range(times):
            try:
                e = self.driver.element(using, value)

                width = e.rect['width']
                height = e.rect['height']
                if stability_width != width or stability_height != height:
                    stability_width = width
                    stability_height = height
                    raise WebDriverException
                else:
                    return e
            except WebDriverException:
                if direction == 'up':
                    self.swipe_up_ele(element=element, steps=steps)
                elif direction == 'down':
                    self.swipe_down_ele(element=element, steps=steps)
                elif direction == 'left':
                    self.swipe_left_ele(element=element, steps=steps)
                elif direction == 'right':
                    self.swipe_right_ele(element=element, steps=steps)

                if i == times - 1:
                    raise WebDriverException

    def find_element_by_swipe_up(self, using, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe up
        :param using: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('up', using, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_down(self, using, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe down
        :param using: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('down', using, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_left(self, using, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe left
        :param using: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('left', using, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_right(self, using, value, element=None, steps=10, max_swipe=6):
        """
        find element by swipe right
        :param using: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        return self._find_element_by_swipe('right', using, value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_on_horizontal(self, using, value, element=None, steps=10, max_swipe=6):
        """
        find element on horizontal
        :param using: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        try:
            return self.find_element_by_swipe_left(using, value,
                                                   element=element, steps=steps, max_swipe=max_swipe)
        except WebDriverException:
            pass

        return self.find_element_by_swipe_right(using, value,
                                                element=element, steps=steps, max_swipe=max_swipe)

    def find_element_on_vertical(self, using, value, element=None, steps=10, max_swipe=6):
        """
        find element on vertical
        :param using: The element location strategy.
                      "id","xpath","link text","partial link text","name","tag name","class name","css selector"
        :param value: The value of the location strategy.
        :param element: WebElement of appium, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: WebElement of appium

        Raises:
            WebDriverException.
        """
        try:
            return self.find_element_by_swipe_up(using, value,
                                                 element=element, steps=steps, max_swipe=max_swipe)
        except WebDriverException:
            pass

        return self.find_element_by_swipe_down(using, value,
                                               element=element, steps=steps, max_swipe=max_swipe)

    def _tap(self, x, y):
        self.driver.touch('tap', {'x': x, 'y': y})

    def _press(self, x, y):
        self.driver.touch('press', {'x': x, 'y': y, 'steps': 100})

    def _side_of_element(self, direction, element, rate):
        rect = element.rect

        width = rect['width']
        height = rect['height']

        x_center = rect['x'] + rect['width'] / 2
        y_center = rect['y'] + rect['height'] / 2

        x_left = rect['x']
        y_up = rect['y']
        x_right = rect['x'] + rect['width']
        y_down = rect['y'] + rect['height']

        x = y = 0
        if direction == 'above':
            x = x_center
            y = y_up - rate * height
        elif direction == 'under':
            x = x_center
            y = y_down + rate * height
        elif direction == 'left':
            x = x_left - rate * width
            y = y_center
        elif direction == 'right':
            x = x_right + rate * width
            y = y_center

        return x, y

    def _click_side_of_element(self, direction, element, rate):
        x, y = self._side_of_element(direction, element, rate)

        self._tap(x, y)

    def _press_side_of_element(self, direction, element, rate):
        x, y = self._side_of_element(direction, element, rate)

        self._press(x, y)

    def click_above_of_element(self, element, rate=1):
        """
        click above the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._click_side_of_element('above', element, rate)

    def click_under_of_element(self, element, rate=1):
        """
        click under the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._click_side_of_element('under', element, rate)

    def click_left_of_element(self, element, rate=1):
        """
        click the left of the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._click_side_of_element('left', element, rate)

    def click_right_of_element(self, element, rate=1):
        """
        click the right of the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._click_side_of_element('right', element, rate)

    def press_above_of_element(self, element, rate=1):
        """
        press above the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._press_side_of_element('above', element, rate)

    def press_under_of_element(self, element, rate=1):
        """
        press under the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._press_side_of_element('under', element, rate)

    def press_left_of_element(self, element, rate=1):
        """
        press the left of the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._press_side_of_element('left', element, rate)

    def press_right_of_element(self, element, rate=1):
        """
        press the right of the gaven element
        :param element: WebElement of appium
        :param rate: rate of the width or height of the element
        :return: None
        """
        self._press_side_of_element('right', element, rate)

    def wait_string(self, string, timeout=10000, interval=1000):
        """
        wait string between the gaven time
        :param string: string
        :param timeout: timeout(ms) that wait the gaven strings
        :param interval: interval(ms)
        :return: True or False
        """
        times = int(timeout / interval) + 1
        interval_s = interval / 1000

        for i in range(times):
            time.sleep(interval_s)

            source = self.driver.source
            if string in source:
                return True

            if i == times - 1:
                return False

    def wait_string_use_and(self, *args, timeout=10000, interval=1000):
        """
        wait all strings between the gaven time
        :param args: strings
        :param timeout: timeout(ms) that wait the gaven strings
        :param interval: interval(ms)
        :return: True or False
        """
        times = int(timeout / interval) + 1
        interval_s = interval / 1000

        for i in range(times):
            time.sleep(interval_s)

            source = self.driver.source
            previous = False
            for j in range(len(args)):
                if args[j] in source:
                    if j != 0 and not previous:
                        return False

                    previous = True

                    if j == len(args) - 1:
                        return True
                else:
                    if previous:
                        return False

            if i == times - 1:
                return False

    def wait_string_use_or(self, *args, timeout=10000, interval=1000):
        """
        wait anyone string between the gaven time
        :param args: strings
        :param timeout: timeout(ms) that wait the gaven strings
        :param interval: interval(ms)
        :return: True or False
        """
        times = int(timeout / interval) + 1
        interval_s = interval / 1000

        for i in range(times):
            time.sleep(interval_s)

            source = self.driver.source
            for string in args:
                if string in source:
                    return True

            if i == times - 1:
                return False

    def _find_element_in_nodes(self, nodes, using, value):
        for node in nodes:
            result = self._find_element_in_node(node, using, value)
            if result is not None:
                return result

    def _find_element_in_node(self, node, using, value):
        if node.get(using) == value:
            return node

        child_nodes = node.findall('node')
        if len(child_nodes):
            return self._find_element_in_nodes(child_nodes, using, value)
        else:
            return None

    @staticmethod
    def _parse_bounds(bounds_str):
        bounds = bounds_str.split(',')
        x_left = int(bounds[0].strip('['))
        y_up = int(bounds[1].split(']')[0])
        x_right = int(bounds[1].split(']')[1].strip('['))
        y_down = int(bounds[2].strip(']'))

        x_center = (x_left + x_right) / 2
        y_center = (y_up + y_down) / 2

        return x_center, y_center

    @staticmethod
    def _delete_file(filename):
        if os.path.exists(filename):
            os.remove(filename)

    def _wait_element(self, using, value, timeout=10000, interval=1000):
        times = int(timeout / interval) + 1
        interval_s = interval / 1000

        stability_flag = ''
        for i in range(times):
            time.sleep(interval_s)

            file = 'source.xml'
            with open(file, 'wt', encoding='utf-8') as f:
                f.write(self.driver.source)

            try:
                tree = ElementTree()
                tree.parse(file)
                root = tree.getroot()

                nodes = root.findall('node')
                result = self._find_element_in_nodes(nodes, using, value)
                if result is not None:
                    bounds_str = result.get('bounds')
                    if stability_flag != bounds_str:
                        stability_flag = bounds_str
                    else:
                        self._delete_file(file)
                        return result

                if i == times - 1:
                    self._delete_file(file)
                    return None
            except Exception:
                self._delete_file(file)
                raise Exception

    def find_element(self, element):
        """判断元素是否存在"""
        try:
            self.driver \
                .find_element_by_id(element)
            return True
        except:
            return False
