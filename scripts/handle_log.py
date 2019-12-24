import logging
import os

from scripts.handle_path import LOGS_DIR
from scripts.handle_yaml import do_yaml

class HandleLog:
    # 定义日志处理类
    @classmethod
    def create_logger(cls):
        # 创建日志收集器设置等级
        logger = logging.getLogger(do_yaml.read_yaml('log', 'log_name'))
        logger.setLevel(do_yaml.read_yaml('log', 'logger_level'))

        # 设置输出格式
        formatter = logging.Formatter(do_yaml.read_yaml('log', 'log_formatter'))

        # 创建输出到控制台的日志输出渠道对象，设置等级
        stream = logging.StreamHandler()
        stream.setLevel(do_yaml.read_yaml('log', 'stream_levle'))
        stream.setFormatter(formatter)

        # 将渠道对象加入到日志收集器
        logger.addHandler(stream)

        # 创建输出到文件的输出渠道对象，设置等级并加入到日志收集器
        filer = logging.FileHandler(os.path.join(LOGS_DIR, do_yaml.read_yaml('log', 'logfile_name')),
                                    encoding='utf8')
        filer.setLevel(do_yaml.read_yaml('log', 'logfile_level'))
        filer.setFormatter(formatter)
        logger.addHandler(filer)

        return logger


do_logs = HandleLog.create_logger()






