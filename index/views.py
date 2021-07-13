from flask import request, g, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from db.db_model import MongoInstance
from utility.decorators import login_required

from index import index_bp

index_api = Api(index_bp)


class Index(Resource):
    method_decorators = [login_required]

    def get(self):
        users_db = MongoInstance()
        user_id = g.user_id
        user_role = g.role_id

        # 标注者首页
        if user_role == "1":
            label_project_info = users_db.get_label_project_info(user_id)
            return_dict = {"project_info": label_project_info, "edit_role": False, "user_role": user_role}
            return jsonify(return_dict)

        # 一审
        elif user_role == "2":
            first_instance_info = users_db.get_first_project_info()
            return_dict = {"project_info": first_instance_info, "edit_role": False, "user_role": user_role}
            return jsonify(return_dict)

        # 二审
        elif user_role == "3":
            first_instance_info = users_db.get_first_project_info()
            return_dict = {"project_info": first_instance_info, "edit_role": False, "user_role": user_role}
            return jsonify(return_dict)

        # 项目创建者首页
        elif user_role == "4":
            create_project_info = users_db.get_create_project_info(user_id)
            return_dict = {"project_info": create_project_info, "edit_role": True, "user_role": user_role}
            return return_dict

        elif user_role == "5":
            users_without_admin = users_db.users_without_admin()
            all_project_info = users_db.all_project_info()
            return_dict = {"project_info": all_project_info, "users_info": users_without_admin, "edit_role": True, "user_role": user_role}
            return jsonify(return_dict)


index_api.add_resource(Index, '/', endpoint="index")
