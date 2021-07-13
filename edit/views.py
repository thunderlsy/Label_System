from flask import jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from db.db_model import MongoInstance
from utility.decorators import login_required
from info.response_code import RET

from edit import label_edit_bp, relation_edit_bp, user_edit_bp

label_api = Api(label_edit_bp)
relation_api = Api(relation_edit_bp)
user_api = Api(user_edit_bp)


class Labeledit(Resource):
    method_decorators = [login_required]
    db = MongoInstance()

    def get(self):
        json_parser = RequestParser()
        json_parser.add_argument('project_id', required=True, location='args')
        args = json_parser.parse_args()

        project_id = args.project_id
        label_list = self.db.get_labels(project_id)

        if not label_list:
            return jsonify(error=RET.OK, message="已查询标签", label_list='')

        return jsonify(error=RET.OK, message="已查询标签", label_list=label_list)

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('label_name', required=True, location='json')
        json_parser.add_argument('label_color', required=True, location='json')
        json_parser.add_argument('label_shortcut_key', required=True, location='json')
        json_parser.add_argument('keycode', required=True, location='json')
        json_parser.add_argument('project_id', required=True, location='json')
        args = json_parser.parse_args()

        label_name = args.label_name
        label_color = args.label_color
        label_shortcut_key = args.label_shortcut_key
        keycode = args.keycode
        project_id = args.project_id

        self.db.add_label(label_name, label_color, label_shortcut_key, keycode, project_id)

        return jsonify(error=RET.OK, message='标签已添加')

    def delete(self):
        json_parser = RequestParser()
        json_parser.add_argument('label_id', required=True, location='args')
        args = json_parser.parse_args()

        label_id = args.label_id
        self.db.delete_label(label_id)

        return jsonify(error=RET.OK, message='标签已删除')


class Relationedit(Resource):
    method_decorators = [login_required]
    db = MongoInstance()

    def get(self):

        json_parser = RequestParser()
        json_parser.add_argument('project_id', required=True, location='args')
        args = json_parser.parse_args()

        project_id = args.project_id

        relation_list = self.db.get_relation(project_id)
        if not relation_list:
            return jsonify(error=RET.OK, message='关系已查询', relation_list='')

        return jsonify(error=RET.OK, message='关系已查询', relation_list=relation_list)


    def post(self):

        json_parser = RequestParser()
        json_parser.add_argument('relation_name', required=True, location='json')
        json_parser.add_argument('project_id', required=True, location='json')
        args = json_parser.parse_args()

        relation_name = args.relation_name
        project_id = args.project_id

        self.db.add_relation(relation_name, project_id)

        return jsonify(error=RET.OK, message='关系已添加')

    def delete(self):
        json_parser = RequestParser()
        json_parser.add_argument('relation_id', required=True, location='args')
        args = json_parser.parse_args()

        relation_id = args.relation_id
        self.db.delete_relation(relation_id)

        return jsonify(error=RET.OK, message='标签已删除')


class Useredit(Resource):
    method_decorators = [login_required]
    db = MongoInstance()

    def post(self):
        json_parser = RequestParser()
        json_parser.add_argument('worknumber', required=True, location='json')
        json_parser.add_argument('password', required=True, location='json')
        json_parser.add_argument('name', required=True, location='json')
        json_parser.add_argument('role_id', required=True, location='json')

        args = json_parser.parse_args()

        worknumber = args.worknumber
        password = args.password
        name = args.name
        role_id = args.role_id

        if not all([worknumber, password, name, role_id]):
            return jsonify(error=RET.DATAERR, message='数据错误，请正确填写')

        number_repeat = self.db.get_worknumber_repeat(worknumber)
        if number_repeat:
            return jsonify(error=RET.DATAEXIST, message='用户名已被注册')

        insert_id = self.db.add_user(worknumber, password, name, role_id)
        print("添加UID: {}".format(insert_id))
        return jsonify(error=RET.OK, message='注册用户成功')

    def delete(self):
        json_parser = RequestParser()
        json_parser.add_argument('user_id', required=True, location='args')

        args = json_parser.parse_args()

        user_id = args.user_id

        self.db.delete_user(user_id)
        return jsonify(error=RET.OK, message='删除用户成功')


label_api.add_resource(Labeledit, '/', endpoint="labeledit")
relation_api.add_resource(Relationedit, '/', endpoint="relationedit")
user_api.add_resource(Useredit, '/', endpoint="useredit")
