#  @Author : Vector
#  @Email  : vectorztt@163.com
#  @Time   : 2019/7/2 15:08
# -----------------------------------------
import sys

import pymysql
from conf.base_config import GetVariable as gv


class SqlDb:

    @classmethod
    def start_db(cls):
        """启动数据库"""
        cls.db = pymysql.connect(gv.HOST, gv.USER_NAME, gv.PASSWORD, gv.DB)
        cls.cursor = cls.db.cursor()
        print('启动数据库')

    def close_db(self):
        print('关闭数据库')
        self.db.close()

    def execute_sql_return_result(self, sql):
        result = 0
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.db.commit()
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.db.rollback()
        return result

    def execute_sql_only(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.db.rollback()