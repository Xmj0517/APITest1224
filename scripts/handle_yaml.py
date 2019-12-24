import yaml

# 导入配置文件目录
from scripts.handle_path import CONFIGS_FILE_DIR


class HandleYaml(object):
    '''
    定义处理yaml配置文件的类
    '''
    def __init__(self, filename):
        self.filename = filename

    # 读取数据方法
    def read_yaml(self, area, option):
        with open(self.filename, encoding='utf8') as file_1:
            res = yaml.full_load(file_1)
            return res[area][option]

    # 写入数据方法
    @staticmethod
    def write_yaml(filename, datas):
        with open(filename, 'w', encoding='utf8') as file_2:
            yaml.dump(datas, file_2, allow_unicode=True)


do_yaml = HandleYaml(CONFIGS_FILE_DIR)


if __name__ == '__main__':
    do_yaml = HandleYaml()
    print(do_yaml.read_yaml('mysql', 'host'))


