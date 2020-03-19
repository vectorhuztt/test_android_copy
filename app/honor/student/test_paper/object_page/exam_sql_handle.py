import json

from app.honor.student.login.object_page.home_page import HomePage
from app.honor.student.test_paper.object_page.exam_sql import ExamSql
from conf.base_page import BasePage
from conf.decorator import teststep


class DataPage(BasePage):
    """数据操作类"""
    def __init__(self):
        self.mysql = ExamSql()
        self.home = HomePage()

    @teststep
    def delete_student_exam_record(self, stu_id):
        """删除学生试卷记录"""
        self.mysql.delete_all_exam_record(stu_id)
        self.mysql.delete_all_exam_wrong(stu_id)
        self.mysql.delete_student_all_exams(stu_id)

    @teststep
    def write_json_to_file(self, json_data):
        with open('app/honor/student/test_paper/test_data/data.json', 'w') as f:
            json.dump(json_data, f, ensure_ascii=False)

    @teststep
    def get_data_json_from_file(self):
        with open('app/honor/student/test_paper/test_data/data.json', 'r', encoding='gbk', errors='ignore') as f:
            try:
                data_json = json.load(f)
                print('记录答案:', data_json)
                return data_json
            except:
                return {}





