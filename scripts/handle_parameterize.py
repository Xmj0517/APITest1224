import re

from scripts.handle_mysql import HandleMysql
from scripts.handle_path import USER_FILE_DIR
from scripts.handle_yaml import do_yaml, HandleYaml

class HandleParams:
    """
    参数化类
    """
    # 不存在的参数替换字符
    not_existed_phone = r'{not_existed_phone}'  # 不存在的手机号
    not_existed_user_id = r'{not_existed_user_id}'  # 不存在的用户id
    not_existed_loan_id = r'{not_existed_loan_id}'  # 不存在的标id

    # 投资人参数
    invest_existed_phone = r"{invest_existed_phone}"  # 投资人手机号
    invest_user_pwd = r"{invest_user_pwd}"  # 投资人密码
    invest_user_id = r"{invest_user_id}"  # 投资人id

    # 借款人参数
    borrow_existed_phone = r'{borrow_existed_phone}'  # 借款人的手机号
    borrow_user_pwd = r'{borrow_user_pwd}'  # 借款人的密码
    borrow_user_id = r'{borrow_user_id}'  # 借款人的id

    # 管理员参数
    admin_existed_phone = r'{admin_existed_phone}'  # 管理员的手机号
    admin_user_pwd = r'{admin_user_pwd}'  # 管理员的密码

    # 其他参数
    loan_id_pattern = r'{loan_id}'  # 标id

    # 需要读取配置文件中的用户信息
    read_user_yaml = HandleYaml(USER_FILE_DIR)

    @classmethod
    def not_existed_replace(cls, data):
        """
        不存在的参数替换
        :param data:待替换的字符串
        :return:
        """
        # 创建数据库连接对象
        cls.do_mysql = HandleMysql()
        # 替换不存在的手机号
        if cls.not_existed_phone in data:
            data = re.sub(cls.not_existed_phone, \
                          cls.do_mysql.create_not_existed_mobile(), data)

        # 替换不存在的用户id
        if cls.not_existed_user_id in data:
            # 数据库中取出最大的id值加1
            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
            max_id = cls.do_mysql.run_sql(sql)
            data = re.sub(cls.not_existed_user_id, str(max_id['id'] + 1), data)

        # 替换不存在的标id
        if cls.not_existed_loan_id in data:
            # 数据库中取出最大的标id值加1
            sql = "SELECT id FROM loan ORDER BY id DESC LIMIT 0,1;"
            max_id = cls.do_mysql.run_sql(sql)
            data = re.sub(cls.not_existed_loan_id, str(max_id['id'] + 1), data)

        cls.do_mysql.close()
        return data

    @classmethod
    def invest_replace(cls, data):
        """
        投资人参数的替换 直接在配置文件中取数据
        :param data: 待替换的字符串
        :return:
        """
        # 替换投资用户手机号
        if cls.invest_existed_phone in data:
            data = re.sub(cls.invest_existed_phone, \
                          cls.read_user_yaml.read_yaml('投资人', 'mobile_phone'), data)

        # 替换投资用户密码
        if cls.invest_user_pwd in data:
            data = re.sub(cls.invest_user_pwd, \
                          cls.read_user_yaml.read_yaml('投资人', 'pwd'), data)

        # 替换投资用户密码
        if cls.invest_user_id in data:
            data = re.sub(cls.invest_user_id, \
                          str(cls.read_user_yaml.read_yaml('投资人', 'id')), data)
        return data

    @classmethod
    def borrow_replace(cls, data):
        """
        借款人参数的替换 直接在配置文件中取数据
        :param data: 待替换的数据
        :return:
        """
        # 替换借款用户手机号
        if cls.borrow_existed_phone in data:
            data = re.sub(cls.borrow_existed_phone, \
                          cls.read_user_yaml.read_yaml('借款人', 'mobile_phone'), data)

        # 替换借款用户密码
        if cls.borrow_user_pwd in data:
            data = re.sub(cls.borrow_user_pwd, \
                          cls.read_user_yaml.read_yaml('借款人', 'pwd'), data)

        # 替换借款用户密码
        if cls.borrow_user_id in data:
            data = re.sub(cls.borrow_user_id, \
                          str(cls.read_user_yaml.read_yaml('借款人', 'id')), data)
        return data

    @classmethod
    def admin_replace(cls, data):
        """
        管理员参数的替换 直接在配置文件中取数据
        :param data: 待替换的数据
        :return:
        """
        # 替换借管理用户手机号
        if cls.admin_existed_phone in data:
            data = re.sub(cls.admin_existed_phone, \
                          cls.read_user_yaml.read_yaml('管理员', 'mobile_phone'), data)

        # 替换管理用户密码
        if cls.admin_user_pwd in data:
            data = re.sub(cls.admin_user_pwd, \
                          cls.read_user_yaml.read_yaml('管理员', 'pwd'), data)
        return data

    # 其他替换
    @classmethod
    def other_replace(cls, data):
        if cls.loan_id_pattern in data:
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)
        return data

    @classmethod
    def replace_params(cls, data):
        data = cls.not_existed_replace(data)
        data = cls.invest_replace(data)
        data = cls.borrow_replace(data)
        data = cls.admin_replace(data)
        data = cls.other_replace(data)
        return data


if __name__ == '__main__':
    one_str = '{"mobile_phone": "{not_existed_phone}", "pwd": "12345678", "type": 1, "reg_name": "Xmj"}'
    two_str = '{"mobile_phone": "{admin_existed_phone}", "pwd": "{invest_user_pwd}", "type": 1, "reg_name": "Xmj"}'
    print(HandleParams.replace_params(two_str))

