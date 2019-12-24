import json
import requests


class HandleRequests:
    """
    处理请求
    """
    def __init__(self):
        # 创建Session会话对象
        self.one_session = requests.Session()

    def add_headers(self, headers):
        """
        添加公共请求头
        :param headers:要添加的请求头数据，字典类型
        :return:
        """
        # Session会话对象中的headers相当于一个字典
        # 可以将待添加的请求头字典与self.one_session.headers中的请求头(类似字典)进行合并覆盖
        self.one_session.headers.update(headers)

    def send(self, url, method="post", data=None, is_json=True, **kwargs):
        """
        发起请求
        :param url: url地址
        :param method: 请求方法, 通常为get、post、put、delete、patch
        :param data: 传递的参数, 可以传字典、json格式的字符串、字典类型的字符串, 默认为None
        :param is_json: 是否以json的形式来传递参数, 如果为True, 则以json形式来传, 如果为False则以www-form形式来传, 默认为True
        :param kwargs: 可变参数, 可以接收关键字参数, 如headers、params、files等
        :return: None 或者 Response对象
        """
        # data可以为如下三种类型：
        # data = {"name": '可优', 'gender': True}       # 字典类型
        # data = '{"name": "可优", "gender": true}'     # json格式的字符串
        # data = "{'name': '优优', 'gender': True}"     # 字典类型的字符串

        if isinstance(data, str):  # 判断data类型，是字符串则返回True，否则False
            try:
                # 若是json字符串，先使用loads方法转化为字典
                data = json.loads(data)
            except Exception as e: # 如果不是json字符串则会抛出异常，使用eval函数转化
                data = eval(data)

        # 将method转为小写
        method = method.lower()
        if method == "get":  # 如果为get请求方法，那么data默认传给params参数，使用查询字符串参数
            res = self.one_session.request(method, url, params=data, **kwargs)
        elif method in ("post", "put", "delete", "patch"):  # 如果为这四种方式中的一种
            if is_json:  # 如果is_json为True，则使用json方式传递参数
                res = self.one_session.request(method, url, json=data, **kwargs)
            else:  # 如果is_json为False，则用www—form表单形式，给data传参
                res = self.one_session.request(method, url, data=data, **kwargs)
        else:
            res = None
            print("不支持{}方法".format(method))
        return res

    def close(self):
        # 调用关闭方法，释放资源，还能继续发起请求
        self.one_session.close()


if __name__ == '__main__':
    # url
    url_register = "http://api.lemonban.com/futureloan/member/register"
    url_login = "http://api.lemonban.com/futureloan/member/login"
    url_recharge = "http://api.lemonban.com/futureloan/member/recharge"

    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 KeYou",
        "X-Lemonban-Media-Type": "lemonban.v2"
    }

    # 数据
    datas = {
        "mobile_phone": "18344446679",
        "pwd": "12345678",
    }

    # 注册
    request_obj = HandleRequests()
    # 添加公共请求头
    request_obj.add_headers(headers)
    # register_res = request_obj.send(url_register, "post", data=datas, headers=headers)
    # print(register_res.json())

    # 登录
    login_res = request_obj.send(url_login, data=datas)
    # 取member_id
    login_res = login_res.json()
    member_id = login_res['data']['id']
    # 取token
    token = login_res['data']['token_info']['token']

    # 充值的数据
    datas_recharge = {
        "member_id": member_id,
        "amount": 800
    }

    # 充值接口添加token信息到请求头
    headers_add = {
        "Authorization": "Bearer " + token
    }

    request_obj.add_headers(headers_add)

    # 执行充值
    recharge_res = request_obj.send(url_recharge, data=datas_recharge)
    print(recharge_res.json())
    request_obj.close()



