#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/10/21 16:52
# -----------------------------------------
import sys

from conf.decorator import teststep, screenshot


class ExpectingTest:

    def __init__(self, test, result):
        self.test = test
        self.result = result
        self.errors = []

    def _fail(self, failure):
        try:
            raise failure
        except:
            screenshot('Fail')
            self.errors.append(sys.exc_info())

    def get_error(self):
        return self.errors

    def except_error(self, msg):
        self._fail(self.test.failureException(
            '{0}\n{1}  line:{2}'.format(msg, str(sys._getframe().f_back.f_code.co_filename), str(sys._getframe().f_back.f_lineno))))