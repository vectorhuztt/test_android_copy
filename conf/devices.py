# coding=utf-8
import os
from conf.base_config import GetVariable as gv
from appium import webdriver

from conf.base_page import BasePage
from conf.log import Log
from conf.login_status import LoginStatus
from conf.report_path import ReportPath
from utils.sql import SqlDb


class Devices:
    """获取连接的设备的信息"""
    @staticmethod
    def get_devices():
        value = os.popen('adb devices')
        device_names = [x.replace('\n', '').replace('\t', '  ').split('  ')[0]
                        for x in value.readlines() if 'device' in x and 'List' not in x]
        device_info = {}
        for x in device_names:
            cmd = 'adb -s ' + x + ' shell getprop ro.build.version.release'
            android_version = os.popen(cmd).read().replace('\n', '')
            device_info[x] = android_version

        print(device_info)
        return device_info

    def appium_desired(self, device_name, android_version, port, run, cases):
        clear_cmd = 'adb -s ' + device_name + ' shell pm clear com.vanthink.student.debug'
        os.system(clear_cmd)

        android = {
            "newCommandTimeout": 3600,
            'platformName': 'Android',
            'deviceName': device_name,
            'package': 'com.vanthink.student.debug',
            'platformVersion': android_version,
            'port': port,
            'systemPort': port + 10,
            'app': gv.PATH(gv.PACKAGE),
            "automationName": "UiAutomator2",
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            "noReset": True
        }
        log = Log()
        log.set_logger(device_name, run.get_path() + '\\' + 'client.log')
        log.i('platformName: %s', android['platformName'])
        log.i('platformVersion: %s', android_version)
        log.i('deviceName: %s', device_name)
        log.i('app: %s', android['app'])
        log.i('appium server port: %d\n', port)

        addr = "http://127.0.0.1:%s/wd/hub" % port
        driver = webdriver.Remote(addr, android)
        base_page = BasePage()
        mysql = SqlDb()
        mysql.start_db()
        base_page.set_db(mysql)

        # 驱动driver 设置
        base_page.set_driver(driver)
        login_status = LoginStatus()
        login_status.set_status(False)

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())
        print('start cases')
        run.run_httprunner(cases)
        print('end')
        driver.quit()
        return driver