from flask import g, current_app, jsonify
from functools import wraps
from info.response_code import RET


# 要求用户必须登录的装饰器
def login_required(func):
    def wrapper(*args, **kwargs):
        # 1.判断用户是否登录，如果登录，进入视图函数
        if g.user_id is not None and g.is_refresh is False:
            return func(*args, **kwargs)
        else:
            # 2.如果没有登录，401，用户权限认证失败
            # return {"message": "user authorization fail"}, 401
            return jsonify(error=RET.ROLEERR, errmsg="用户权限认证失败")

    return wrapper
