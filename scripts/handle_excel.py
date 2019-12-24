import os
import openpyxl

from scripts.handle_path import DATAS_DIR
from scripts.handle_yaml import do_yaml


class CaseData:
    pass


class HandleExcel(object):
    # 初始化文件名和表单名
    def __init__(self, sheet_name, filename=None):
        if filename is None:
            self.filename = os.path.join(DATAS_DIR, do_yaml.read_yaml('excel', 'cases_path'))
        else:
            self.filename = filename
        self.sheet_name = sheet_name

    # 打开表单
    def open(self):
        self.wb = openpyxl.load_workbook(self.filename)
        self.sh = self.wb[self.sheet_name]

    # 读取数据
    def read_datas(self):
        self.open()
        # 获取数据,转成列表
        rows = list(self.sh.rows)
        # 取title，放入列表
        titles = [t.value for t in rows[0]]
        cases_data = []
        for j in rows[1:]:
            datas = [i.value for i in j]
            case = CaseData()
            for k in zip(titles, datas):
                setattr(case, k[0], k[1])
            cases_data.append(case)
        self.wb.close()
        return cases_data

    # 写入数据
    def write_data(self, row, column, value):
        self.open()
        self.sh.cell(row=row, column=column, value=value)
        self.wb.save(self.filename)
        self.wb.close()


if __name__ == '__main__':
    do_excel = HandleExcel('register')
    cases = do_excel.read_datas()
    print(cases[0].title)







