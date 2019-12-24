import pymysql
import random

from scripts.handle_yaml import do_yaml


# 定义处理数据库操作的类对象
class HandleMysql:
    def __init__(self):
        # 建立连接
        self.connect = pymysql.connect(host=do_yaml.read_yaml('mysql', 'host'),
                                       user=do_yaml.read_yaml('mysql', 'user'),
                                       password=do_yaml.read_yaml('mysql', 'password'),
                                       db=do_yaml.read_yaml('mysql', 'db'),
                                       port=do_yaml.read_yaml('mysql', 'port'),
                                       charset='utf8',
                                       cursorclass=pymysql.cursors.DictCursor  # 设置游标类型，使返回为字典格式
                                       )
        # 创建游标对象
        self.cuosor = self.connect.cursor()

    # 关闭连接方法
    def close(self):
        self.cuosor.close()
        self.connect.close()

    # 执行sql语句方法
    def run_sql(self, sql, args=None, is_more=False):
        self.cuosor.execute(sql, args)
        self.connect.commit()
        if is_more:
            return self.cuosor.fetchall()
        else:
            return self.cuosor.fetchone()

    @staticmethod
    def create_mobile():
        # 随机生成手机号
        return '156' + ''.join(random.sample('1234567890', 8))

    def is_existed(self, mobile_num):
        """
        判断生成的手机号是否已经在数据库中存在
        :param mobile_num:待判断的手机号码
        :return:存在则返回True，不存在则返回False
        """
        sql = do_yaml.read_yaml('mysql', 'select_user_sql')
        if self.run_sql(sql, args=[mobile_num]):
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """
        随机生成一个数据库中不存在的手机号
        :return:
        """
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed(one_mobile):
                break
        return one_mobile



if __name__ == '__main__':
    do_mysql = HandleMysql()
    res = do_mysql.run_sql("SELECT id FROM loan ORDER BY id DESC LIMIT 0,1;")
    print(res)
    do_mysql.close()
