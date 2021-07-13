from flask import request, g

# 会引发循环导包问题
from utility.jwt_util import verify_jwt


"""
def my_decorator(func):
    
    def wrapper(*args, **kwargs):
        pass
    return wrapper

def demo1():
    pass

# 装饰器的使用方法1：
@my_decorator
def demo1():
    pass

# 装饰器使用方法2：
# 装饰器本质是函数：类似函数调用
# my_decorator(demo1)

"""


# 需求：每一次请求之前进行token校验，用户身份信息提取，保存到g对象
# 请求钩子装饰器使用 方案1
# @app.before_request

# 改造：app.before_request(jwt_authorization)
def jwt_authorization():
    # 设置默认值
    g.user_id = None
    g.role_id = None
    g.is_refresh = False
    # 1.请求头Header携带
    # {Authorization: "Bearer jwt_token"}
    header_token = request.headers.get("Authorization")

    if header_token is not None and header_token.startswith("Bearer "):
        # 2.提取前端发送的真实token值
        real_token = header_token[7:]
        # 2.1 token值的校验，和提取payload
        payload = verify_jwt(real_token)

        if payload is not None:

            # 提取用户信息,保存到g对象中
            g.user_id = payload.get("user_id")

            g.role_id = payload.get("role_id")

            # 注意：不设置默认值 None
            g.is_refresh = payload.get("is_refresh", False)


