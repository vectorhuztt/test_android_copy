import time
from HTMLTestReportCN2 import DirAndFiles
from functools import wraps
from selenium.common.exceptions import WebDriverException

from conf.base_page import BasePage
from conf.report_path import ReportPath
from conf.log import Log

flag = 'IMAGE:'
log = Log()


def screenshot(error_type):
    report_path = ReportPath().get_path()
    driver = BasePage().get_driver()
    img_name = DirAndFiles(report_path).get_screenshot(driver, error_type)
    print('screen_shot[' + error_type + "--" + img_name + ']screen_shot\n')
    return img_name


def teststep(func: object) -> object:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('\t--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            return ret
        except WebDriverException as e:
            log.e('WebDriverException, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'WebDriverException', 'Error')

            if flag in str(e):
                raise WebDriverException(e)
            else:
                raise WebDriverException(flag + screenshot('Error'))
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Error')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + screenshot('Error'))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + screenshot('Error'))

    return wrapper


def teststeps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('  --> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.i('  <-- %s, %s', func.__qualname__, 'Success')
            return ret
        except WebDriverException as e:
            log.e('WebDriverException, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'WebDriverException', 'Error')

            if flag in str(e):
                raise WebDriverException(e)
            else:
                raise WebDriverException(flag + screenshot('Error'))
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Error')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + screenshot('Error'))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + screenshot('Error'))

    return wrapper


def _wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.i('<-- %s, %s\n', func.__qualname__, 'Success')
            return ret
        except WebDriverException as e:
            log.e('WebDriverException, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'WebDriverException', 'Error')

            if flag in str(e):
                raise WebDriverException(e)
            else:
                raise WebDriverException(flag + screenshot('Error'))
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + screenshot('Error'))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + screenshot('Error'))

    return wrapper


def testcase(func):
    return _wrapper(func)


def setup(func):
    return _wrapper(func)


def teardown(func):
    return _wrapper(func)


def setupclass(func):
    return _wrapper(func)


def teardownclass(func):
    return _wrapper(func)
