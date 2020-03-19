import sys
sys.path.append('..')  # 上一级目录

from conf.drivers import Drivers
from conf.case_strategy import CaseStrategy


if __name__ == '__main__':
    # in future, cases_list may be used for testing strategy in multi devices
    Drivers().run_cases()
