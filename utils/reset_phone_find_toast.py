import time
import urllib3
# from pprint import pprint
from conf.decorator import teststeps
from conf.base_config import GetVariable as gv


@teststeps
def verify_find(phone, var='editPhone'):
    """action_type:register(用户注册) | resetPassword(忘记密码) | editPhone(修改手机) | quitClass(退出班级)"""
    time.sleep(2)
    http = urllib3.PoolManager()

    if gv.TEST_VERSION == 'test':
        r = http\
            .request('GET', "http://test.vanthink-core-api.vanthink.cn/tool/testEngineerGetCaptcha?"
                            "phone=%s&action_type=%s" % (phone, var))
    else:
        r = http\
            .request('GET', "https://dev.vanthink-core-api.vanthink.cn/master/tool/testEngineerGetCaptcha?"
                            "phone=%s&action_type=%s" % (phone, var))

    value = r._body.decode('utf-8')
    return value

