import unittest
from datetime import datetime
import os

from HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_yaml import do_yaml
from scripts.handle_path import CASES_DIR, REPORTS_DIR, USER_FILE_DIR
from scripts.handle_user import user_init

# 运行前先检测有无创建初始用户，如果无则自动创建
if not os.path.exists(USER_FILE_DIR):
    user_init()

# 创建测试套件
suite = unittest.defaultTestLoader.discover(CASES_DIR)

# 拼接生成报告名称，用时间戳
report_name = do_yaml.read_yaml('report', 'report_name') + '_' + \
              datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + '.html'

# 生成报告路径
report_path = os.path.join(REPORTS_DIR, report_name)

with open(report_path, 'wb') as fb:
    runner = HTMLTestRunner(stream=fb,
                            verbosity=2,
                            title=do_yaml.read_yaml('report', 'title'),
                            description=do_yaml.read_yaml('report', 'description'),
                            tester=do_yaml.read_yaml('report', 'tester')
                            )

    runner.run(suite)

