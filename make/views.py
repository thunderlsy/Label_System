import json

from flask import request, g, current_app, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from db.db_model import MongoInstance
from utility.decorators import login_required
from info.response_code import RET
import ast
from make import make_bp

make_api = Api(make_bp)
db = MongoInstance()


class SaveInfo(Resource):
    method_decorators = [login_required]

    def post(self):
        """
        保存标注员的标注信息
        {"article_id":1,"relation"[{"relation":"sd"}],"sign":[{"sign":1,"start":2,"end":3}],"html_data":"html_data"}
        """
        json_parser = RequestParser()
        json_parser.add_argument('index', required=True, location='json')
        json_parser.add_argument('project_id', required=True, location='json')
        json_parser.add_argument('sign', required=True, location='json')
        json_parser.add_argument('relation', required=True, location='json')
        json_parser.add_argument('html_data', required=True, location='json')

        args = json_parser.parse_args()

        article_index = args.index
        project_id = args.project_id
        sign_data = args.sign
        relation_data = args.relation
        html_data = args.html_data

        user_id = g.user_id
        role_id = g.role_id

        if role_id == "1":
            db.update_article_mark(article_index, project_id, sign_data, relation_data, html_data)
            db.update_make_rate(project_id, user_id)
            return jsonify(error=RET.OK, message="标注员保存成功")
        elif role_id == "2":
            db.update_article_inspect(article_index, project_id, sign_data, relation_data, html_data)
            db.update_inspect_rate(project_id)
            return jsonify(error=RET.OK, message="一审判断过")
        elif role_id == "3":
            db.update_article_review(article_index, project_id, sign_data, relation_data, html_data)
            return jsonify(error=RET.OK, message="二审判断过")


class GetInfo(Resource):
    method_decorators = [login_required]

    def post(self):
        """
        根据当前登陆者的身份获取文章内容
        """
        json_parser = RequestParser()
        json_parser.add_argument('project_id', required=True, location='json')
        args = json_parser.parse_args()

        project_id = args.project_id

        user_id = g.user_id
        role_id = g.role_id
        if role_id == "1":
            article = db.find_article(user_id, project_id)
            get_maker_rate = db.get_maker_rate(project_id, user_id)
            rate_str = str(get_maker_rate[0]) + "/" + str(get_maker_rate[1])
            article_content = {}
            if article is None:
                article_content["state"] = True
                return jsonify(article_content)
            else:
                index = article["index"]
                content = article["content"]
                article_content["index"] = index
                article_content["content"] = content
                article_content["project_id"] = project_id
                article_content["state"] = False
                article_content["maker_rate"] = rate_str
                return jsonify(article_content)
        elif role_id == "2":
            article = db.find_article_inspect(project_id)
            inspector_rate, project_rate = db.get_inspector_rate(project_id)
            rate_str = str(inspector_rate) + "/" + str(project_rate)
            if article is None:
                article_state = {}
                article_state["state"] = True
                return jsonify(article_state)
            else:
                article["state"] = False
                id = article["_id"]
                article["_id"] = str(id)
                label = article["marker_labels"]
                article["marker_labels"] = label
                relation = article["marker_relations"]
                article["marker_relations"] = relation
                article["maker_rate"] = rate_str
                return jsonify(article)
        elif role_id == "3":
            article = db.find_article_review(project_id)
            if article is None:
                article_state = {}
                article_state["state"] = True
                return jsonify(article_state)
            else:
                article["state"] = False
                id = article["_id"]
                article["_id"] = str(id)
                label = article["inspector_labels"]
                article["marker_labels"] = label
                relation = article["inspector_relations"]
                article["marker_relations"] = relation
                return jsonify(article)


make_api.add_resource(SaveInfo, '/saveinfo/', endpoint="save_info")
make_api.add_resource(GetInfo, '/getinfo/', endpoint="get_info")
