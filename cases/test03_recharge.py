import unittest
import json

from lib.ddt import ddt, data
from scripts.handle_yaml import do_yaml
from scripts.handle_excel import HandleExcel
from scripts.handle_requests import HandleRequests
from scripts.handle_parameterize import HandleParams
from scripts.handle_mysql import HandleMysql
from scripts.handle_log import do_logs

@ddt
class Cases(unittest.TestCase):
    # 定义测试用例类
    # 读取excel用例数据
    excel = HandleExcel('recharge')
    cases = excel.read_datas()

    # 前置条件 创建请求对象添加公共请求头
    @classmethod
    def setUpClass(cls):
        cls.do_requests = HandleRequests()
        cls.do_requests.add_headers(do_yaml.read_yaml('api', 'version'))
        # 创建数据库处理对象
        cls.do_mysql = HandleMysql()

    # 后置条件 执行完用例后关闭请求
    @classmethod
    def tearDownClass(cls):
        cls.do_requests.close()
        cls.do_mysql.close()

    @data(*cases)
    def test_recharge(self, case):
        expected = case.expected
        # 取出data并进行参数化
        case_data = HandleParams.replace_params(case.data)
        # url
        url = do_yaml.read_yaml('api', 'url') + case.url

        # 充值前，去数据库获取充值前金额
        check_sql = case.check_sql
        if check_sql:
            check_sql = HandleParams.replace_params(check_sql)
            mysql_data = self.do_mysql.run_sql(check_sql)
            old_amount = round(float(mysql_data['leave_amount']), 2)  # 取出当前金额，保留两位小数

        # 发起请求
        res = self.do_requests.send(url=url,
                                    method=case.request_method,
                                    data=case_data)
        # 结果转为字典
        result = res.json()
        msg = case.title
        success_msg = do_yaml.read_yaml('msg', 'success_result')
        fail_msg = do_yaml.read_yaml('msg', 'fail_result')
        # 获取行号
        row = case.case_id + 1

        try:
            # assertEqual第三个参数为用例执行失败之后的提示信息
            self.assertEqual(expected, result['code'], msg=msg)
            # 充值成功之后再去数据库取当前金额对比
            if check_sql:
                new_amount = round(float(self.do_mysql.run_sql(check_sql)['leave_amount']), 2)
                recharge_amount = json.loads(case_data)['amount']
                actual_amount = round(new_amount - old_amount, 2)
                self.assertEqual(recharge_amount, actual_amount, msg=msg)
        except AssertionError as e:
            # 输出日志
            do_logs.info("{}用例执行有误".format(msg))
            # 写入用例执行结果
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'result_col'),
                                  value=fail_msg)
            do_logs.error('具体异常为{}'.format(e))
            raise e
        else:
            do_logs.info('{}用例执行通过'.format(msg))
            # 写入用例执行结果
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'result_col'),
                                  value=success_msg)
            # 执行用例通过后，判断返回报文中有没有token，有的话取出加到请求头中
            if 'token_info' in res.text:
                self.do_requests.add_headers({"Authorization": "Bearer " + \
                                                               result['data']['token_info']['token']})
        finally:
            # 将实际结果写入
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'actual_col'),
                                  value=res.text)


if __name__ == '__main__':
    test = Cases()



