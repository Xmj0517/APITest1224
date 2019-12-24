import unittest
import json

from lib.ddt import ddt, data
from scripts.handle_yaml import do_yaml
from scripts.handle_excel import HandleExcel
from scripts.handle_requests import HandleRequests
from scripts.handle_parameterize import HandleParams
from scripts.handle_log import do_logs

@ddt
class Cases(unittest.TestCase):
    # 定义测试用例类
    # 读取excel用例数据
    excel = HandleExcel('login')
    cases = excel.read_datas()

    # 前置条件 创建请求对象添加公共请求头
    @classmethod
    def setUpClass(cls):
        cls.do_requests = HandleRequests()
        cls.do_requests.add_headers(do_yaml.read_yaml('api', 'version'))

    # 后置条件 执行完用例后关闭请求
    @classmethod
    def tearDownClass(cls):
        cls.do_requests.close()

    @data(*cases)
    def test_login(self, case):
        # 多字段断言，将期望写成json，然后取出转化成字典
        expected = json.loads(case.expected, encoding='utf8')
        # 取出data并进行参数化
        case_data = HandleParams.replace_params(case.data)
        # url
        url = do_yaml.read_yaml('api', 'url') + case.url

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
            self.assertEqual(expected['code'], result['code'], msg=msg)
            self.assertEqual(expected['msg'], result['msg'], msg=msg)
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
        finally:
            # 将实际结果写入
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'actual_col'),
                                  value=res.text)


if __name__ == '__main__':
    test1 = Cases()



