from flask import request, jsonify, session, current_app, g
# from flask_cors import cross_origin
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from login import login_bp
from info.response_code import RET
from db.db_model import MongoInstance
from datetime import datetime, timedelta
from utility.jwt_util import generate_jwt
from utility.decorators import login_required

login_api = Api(login_bp)


class Login(Resource):
    method_decorators = {
        "get": [login_required]
        # "put": [login_required]
    }

    def _generate_tokens(self, user_id, role_id, with_refresh_token=True):
        """
        生成token 和refresh_token
        :param user_id: 用户id
        :return: token, refresh_token
        """
        # 颁发JWT

        # 两小时有效用户token
        # 1.构建payload数据
        payload = {
            "user_id": user_id,
            "role_id": role_id
        }

        # 2.设置2小时有效期
        # 当前的时间戳 + 2小时的时间间隔时间戳 = 具体的过期点的时间戳
        expiry_2h = datetime.utcnow() + timedelta(hours=2)
        # expiry_2h = datetime.utcnow() + timedelta(minutes=1)

        # 3.加密秘钥
        secrect_key = current_app.config["SECRET_KEY"]

        user_token = generate_jwt(payload=payload, expiry=expiry_2h, secret=secrect_key)

        # 14天有效的刷新token

        # 1.构建刷新token-payload数据
        refresh_payload = {
            "user_id": user_id,
            "role_id": role_id,
            # 标志该token是刷新token
            "is_refresh": True
        }

        # 2.设置14天有效过期时长
        expiry_14d = datetime.utcnow() + timedelta(days=14)

        # 3.加密秘钥
        secrect_key = current_app.config["SECRET_KEY"]

        refresh_token = generate_jwt(payload=refresh_payload, expiry=expiry_14d, secret=secrect_key)

        return user_token, refresh_token

    def get(self):

        return "g对象user_id: {}, g对象role_id: {}".format(g.user_id, g.role_id)

    # @cross_origin(supports_credentials=True)
    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('worknumber', required=True, location='json')
        json_parser.add_argument('password', required=True, location='json')
        args = json_parser.parse_args()

        worknumber = args.worknumber
        password = args.password
        if not all([worknumber, password]):
            return jsonify(error=RET.PARAMERR, errmsg="參數不足")

        try:
            db = MongoInstance()
            db_mongo = {
                "worknumber": worknumber,
                "password": password
            }
            user = db.get_user(db_mongo)
        except Exception as e:
            return jsonify(error=RET.DBERR, errmsg="查询用户对象异常")
        if not user:
            # 用户不存在
            return jsonify(error=RET.DBERR, errmsg="用户不存在")

        user_id_str = str(user['_id'])
        role_id = user.get('role_id')
        token, refresh_token = self._generate_tokens(user_id_str, role_id)
        return jsonify(error=RET.OK, token=token, refresh_token=refresh_token)

    def put(self):
        """
        刷新token的后端接口
        :return:
        """

        # 如何确定是刷新token？ user_id有值同时is_refresh为True

        # 1.提取worknumber
        user_id = g.user_id
        # 2.提取刷新token标志位
        is_refresh = g.is_refresh
        role_id = g.role_id

        # 3.如果是刷新token生成新的token值
        if user_id is not None and is_refresh is True:
            # 生成新的token值
            new_token, refresh_token = self._generate_tokens(user_id, role_id)

            # return {"new_token": new_token}
            return jsonify(error=RET.OK, token=new_token)
        else:
            # 代表刷新token过期了
            # 前端接受到403错误状态码，让用户重新登录
            # return {"message": "refresh token is invalid"}, 403
            return jsonify(error=RET.PARAMERR, message="用户刷新token已过期，请重新登陆")


login_api.add_resource(Login, '/', endpoint="Login")
