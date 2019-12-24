from scripts.handle_yaml import do_yaml, HandleYaml
from scripts.handle_path import USER_FILE_DIR
from scripts.handle_mysql import HandleMysql
from scripts.handle_requests import HandleRequests


# 直接定义用户初始化方法
def user_init():
    # 获取请求头
    headers = do_yaml.read_yaml('api', 'version')
    # 创建请求对象
    do_request = HandleRequests()
    # 添加公共请求头
    do_request.add_headers(headers)
    # url
    url = 'http://api.lemonban.com/futureloan/member/register'

    # 用户数据
    user_datas = [
        {'mobile_phone': '', 'pwd': '12345678', 'type': 0, 'reg_name': '管理员'},
        {'mobile_phone': '', 'pwd': '12345678', 'type': 1, 'reg_name': '借款人'},
        {'mobile_phone': '', 'pwd': '12345678', 'type': 1, 'reg_name': '投资人'}
    ]

    write_yaml = HandleYaml(USER_FILE_DIR)
    # 连接数据库
    do_mysql = HandleMysql()
    user_info = {}
    # 生成手机号并注册
    for user in user_datas:
        user['mobile_phone'] = do_mysql.create_not_existed_mobile()
        # 请求注册接口，返回数据转换成字典并存入字典
        res = do_request.send(url, data=user).json()
        # 获取用户id、密码等信息(区域名为昵称，选项名为data里的字段名以及密码)
        user_info['{}'.format(user['reg_name'])] = res['data']
        user_info['{}'.format(user['reg_name'])]['pwd'] = user['pwd']
    # 写入用户文件
    write_yaml.write_yaml(USER_FILE_DIR, user_info)
    # 断开数据库
    do_mysql.close()
    # 断开请求
    do_request.close()


if __name__ == '__main__':
    user_init()





