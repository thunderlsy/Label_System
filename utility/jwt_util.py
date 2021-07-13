import jwt
from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """

    # 载荷--用户信息，token有效时长
    _payload = {'exp': expiry}

    # {"user_id": 1}
    # update 更新字典 结果：{'exp': expiry, "user_id": 1}
    _payload.update(payload)

    # 读取加密字符串
    if not secret:
        # app.config.from_object(xx)
        # 读取配置信息：current_app.config['JWT_SECRET']
        secret = current_app.config['SECRET_KEY']

    # 生成jwt——token
    token = jwt.encode(_payload, secret, algorithm='HS256')

    # token字符串
    # return token.decode()
    return token


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = current_app.config['SECRET_KEY']

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.PyJWTError:
        payload = None

    # 校验jwt-token，获取payload信息
    return payload
