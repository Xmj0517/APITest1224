import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件的存放目录
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# 配置文件的路径
CONFIGS_FILE_DIR = os.path.join(CONFIGS_DIR, 'testconfigs.yaml')

# 日志文件存放目录
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# excel用例数据文件存放目录
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 初始用户数据文件路径
USER_FILE_DIR = os.path.join(CONFIGS_DIR, 'user_info.yaml')

# 用例程序文件存放目录
CASES_DIR = os.path.join(BASE_DIR, 'cases')

# 报告文件存放路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')



