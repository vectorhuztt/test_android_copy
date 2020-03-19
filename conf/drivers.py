# coding=utf-8
from conf.case_strategy import CaseStrategy
from conf.devices import Devices
from conf.appium_server import *
from conf.run_cases import RunCases
import multiprocessing
from conf.base_config import GetVariable as gv


class Drivers:
    # @staticmethod
    # def start_process_sync(process):
    #     for x in process:
    #         x.start()
    #
    #     for x in process:
    #         x.join()

    @staticmethod
    def run_cases():
        devices_info = Devices().get_devices()
        if not len(devices_info):
            print('there is no device connected this PC')
        else:
            pass

        start_args_list = []
        port_list = []
        item_count = len(gv.CASE_INFO) if len(gv.CASE_INFO) < len(devices_info) else len(devices_info)

        for x in range(item_count):
            port = 4723 + 2*x
            appium_server = AppiumServer(port)
            port_list.append(port)
            device_name = list(devices_info.keys())[x]
            device_version = devices_info[device_name]
            run = RunCases(device_name)
            appium_server.start_appium_server(run)
            cs = CaseStrategy()
            cases = cs.collect_cases(index=x, suite=True)
            start_args_list.append((device_name, device_version, port, run, cases))

        pool = multiprocessing.Pool(item_count)
        for x in start_args_list:
            pool.apply_async(Devices().appium_desired, args=x)
        pool.close()
        pool.join()

        for x in port_list:
            appium_server = AppiumServer(x)
            appium_server.release_port()


