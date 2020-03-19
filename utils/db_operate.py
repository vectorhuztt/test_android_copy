#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
import pymysql

from conf.decorator import teststeps
from conf.log import Log
from conf.base_config import GetVariable as gv


class MyDBOperate:
    """数据库操作"""

    def __init__(self):
        self.db = None
        self.cursor = None
        self.logger = Log()

    @teststeps
    def connectDB(self):
        """连接数据库"""
        try:
            config = {
                'host': str(gv.DB_HOST),
                'user': gv.DB_USERNAME,
                'passwd': gv.DB_PASSWORD,
                'port': int(gv.DB_PORT),
                'db': gv.DB_DATABASE,
                'charset': gv.DB_CHARSET
            }
            # connect to DB
            self.db = pymysql.connect(config)
            # create cursor
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.e(str(ex))

    @teststeps
    def execute_sql(self, sql):
        """执行SQL语句"""
        self.connectDB()
        try:
            # executing sql
            self.cursor.execute(sql)
            # executing by committing to DB
            self.db.commit()
            self.close_db()
            return self.cursor
        except:
            # 发生错误时回滚
            self.db.rollback()
            print('❌❌❌ Error - 执行SQL语句发生错误，回滚数据库')

    @teststeps
    def get_one(self, sql):  # 根据解释/单词查询指定单词/解释
        result = 0
        try:
            self.execute_sql(sql)
            result = self.cursor.fetchone()
        except:
            print("❌❌❌ Error - unable to fetch data.json！！")
        self.db.close()
        return result

    @teststeps
    def get_all_word(self, sql):
        """获取所有数据"""

        results = 0
        try:
            self.execute_sql(sql)
            results = self.cursor.fetchall()
        except:
            print("❌❌❌ Error - unable to fetch all data.json！！")
        self.db.close()
        return results

    @teststeps
    def close_db(self):
        """关闭数据库"""
        self.db.close()
        print("Database closed!")
