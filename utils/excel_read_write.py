#!/usr/bin/env python
# code:UTF-8  
# @Author  : SUN FEIFEI
from xlrd import open_workbook
from xlutils.copy import copy
from conf.base_page import BasePage
from conf.decorator import teststeps
from conf.base_config import GetVariable as ge


class ExcelUtil(BasePage):
    """结果统计excel表格操作"""
    def __init__(self, encoding='utf-8'):
        # must specify the encoding of the input data, utf-8 default.
        self.encoding = encoding
        self.sheets = {}

    @teststeps
    def data_read(self, homework, games):
        """读取Excel表格"""
        print(homework, games)
        open_excel = open_workbook(ge.EXCEL_PATH)  # 因为需要每次读取最新数据，故不能放入init方法
        table = open_excel.sheet_by_name(homework)
        row_num = table.nrows  # 获取总行数

        value = []
        count = []
        length = []
        key = '_'.join([homework, games])  # key值
        for i in range(row_num):  # print by rows
            values = table.row_values(i)
            if values[0] == key:
                count.append(values[1])  # 星星

                if values[len(values) - 1] != '':  # 以下为：统计作对的题的个数
                    length.append(len(values))
                else:
                    for k in range(2, len(values)):
                        if values[k] == '':
                            length.append(k)
                            break

                if len(values) > 2:  # 如果做对过题，则进行读取
                    for j in range(2, length[0]):
                        value.append(values[j])
                elif len(values) == 2:
                    print('No data')
                break
        return value, int(count[0])

    @teststeps
    def data_write(self, star, homework, games, value):
        """写入Excel表格"""
        data = open_workbook(ge.EXCEL_PATH)
        wb = copy(data)

        index = []
        sheet_name = []
        for sheet in data.sheets():
            sheet_name.append(sheet.name)  # 所有sheet的名称
        if homework in sheet_name:
            for i in range(len(sheet_name)):  # 如果该sheet存在，则获取index
                if sheet_name[i] == homework:
                    index.append(i)
                    break
        else:  # 如果不存在，则添加sheet页
            self.create_sheet(homework, wb)
            index.append(len(sheet_name)-1)

        ws = wb.get_sheet(homework)  # 获取sheet对象，通过sheet_by_index()获取的sheet对象没有write()方法
        table = data.sheets()[index[0]]  # open the sheet
        keys = table.col_values(0)  # 获取第一列 - key值
        row_num = table.nrows  # 获取总行数

        key = '_'.join([homework, games])  # key值
        if key in keys:
            print('有该key:')
            length = []
            for k in range(row_num):  # print by rows
                if keys[k] == key:
                    values = table.row_values(k)
                    if values[len(values) - 1] != '':
                        length.append(len(values))
                    else:
                        for j in range(3, len(values)):
                            if values[j] == '':
                                length.append(j)
                                break
                    print('写入的内容:', star, value)
                    ws.write(k, 1, int(star))  # 星星
                    ws.write(k, int(length[0]), value)
        else:
            # 写入数据
            print('还没有该key:')
            print('写入的内容:', key, star, value)
            ws.write(row_num, 0, key)
            ws.write(row_num, 1, int(star))  # 星星
            ws.write(row_num, 2, value)
        wb.save(ge.EXCEL_PATH)  # 保存文件

    @teststeps
    def excel_operate(self, rate, game_status, questions, homework_title, game_title, button):
        """积分核实 参数：题数,正确率，正确题目，大题名称， 查看/再练按钮 """
        count = 0
        print('excel_operate:', game_status, button)
        if game_status == '未开始' and button != '错题再练按钮':  # 小游戏第一次做
            print('小游戏第一次做：')
            if len(questions) != 0:
                # len(question) 积分
                for j in range(len(questions)):
                    self.data_write(rate, homework_title, game_title, questions[j])
            print('==================================================')
            return questions, len(questions), rate

        else:  # 非第一次做
            question = []
            db_data = self.data_read(homework_title, game_title)
            if type(db_data[0]) != 'NoneType':
                for i in range(len(questions)):
                    if questions[i] in db_data[0]:
                        print('重复答对：', questions[i])
                    else:
                        count += 1
                        question.append(questions[i])
                print('又答对：%s题，重复答对:%s题.' % (count, len(questions) - count))

                star = db_data[1]  # 上一题星星数
                if type(db_data[1]) != 'NoneType':
                    if len(questions) != 0:
                        for k in range(len(question)):
                            self.data_write(rate, homework_title, game_title, question[k])

                        question = db_data[0] + question
                print('==================================================')
                return question, count, star

    # 创建sheet
    @teststeps
    def create_sheet(self, sheet_name, wb):
        """Create new sheet
        """
        if sheet_name in self.sheets:
            sheet_index = self.sheets[sheet_name]['index'] + 1
        else:
            print('添加sheet页:')
            sheet_index = 0
            self.sheets[sheet_name] = {'header': []}

        self.sheets[sheet_name]['index'] = sheet_index
        self.sheets[sheet_name]['sheet'] = wb.add_sheet('%s%s' % (sheet_name, sheet_index if sheet_index else ''), cell_overwrite_ok=True)  # 利用保存时同名覆盖达到修改excel文件的目的,注意未被修改的内容保持不变)
        self.sheets[sheet_name]['rows'] = 1
