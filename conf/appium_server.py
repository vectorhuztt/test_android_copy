# coding=utf-8
import os
import re
import subprocess


class AppiumServer:
    def __init__(self, port):
        self.port = str(port)

    def start_appium_server(self, run):
        self.release_port()
        bootstrap_port = str(int(self.port) + 1)
        cmd = "appium -a 127.0.0.1 -p {} -bp {} --no-reset".format(self.port, bootstrap_port)
        log_path = run.get_path() + '\\' + 'appium_server_port_{}.log'.format(self.port)
        subprocess.Popen(cmd, stdout=open(log_path, 'w'), stderr=subprocess.STDOUT, shell=True)

    def release_port(self):
        cmd = 'netstat -ano | findstr %s' % str(self.port)
        result = os.popen(cmd).read()

        if str(self.port) and 'LISTENING' in result:
            pid = re.findall(r'\d+', result.split('LISTENING')[-1])[0]
            cmd = 'taskkill -PID %s -f' % pid
            print(cmd)
            os.popen(cmd)
        else:
            print('port %s is available' % str(self.port))


