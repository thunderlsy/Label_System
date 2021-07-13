import re
import time

from flask import request, g, jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from db.db_model import MongoInstance
from utility.random_split import split_list_above
from utility.decorators import login_required
from info.response_code import RET

from upload import upload_bp

upload_api = Api(upload_bp)


class Upload(Resource):
    method_decorators = [login_required]

    def get(self):
        users_db = MongoInstance()
        users_info = users_db.get_role_id1()
        label_users = []
        for i in users_info:
            label_users.append({"key": str(i.get('_id')), "label": i.get("name")})
        tagger_info = {"tagger": label_users}

        return jsonify(tagger_info)

    def post(self):
        '''
        获取身份为标注者的人员的名单
        '''
        project_db = MongoInstance()
        '''
        获取选中的负责标注的人
        
        
        创建项目，获取当前项目的文章名和description及创建时间并传入对应表单
        '''
        json_parser = RequestParser()

        json_parser.add_argument('name', required=True, location='form')
        json_parser.add_argument('description', required=True, location='form')
        json_parser.add_argument('label_users', required=True, location='form')
        args = json_parser.parse_args()

        name = args.name
        description = args.description
        update = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        create_id = g.user_id
        label_users = args.label_users
        # 测试user_id，后续代码合并后改为上述注释
        # create_id = "60b5a4117b2a0c68a51874b7"

        project_id = project_db.insert_project(name, description, update, create_id, label_users)

        '''
        预处理文本文件
        '''
        file = request.files['materials']  # 获取上传的文件,materials为上传文件名称，合并时再根据前端代码修改
        f = file.stream.read()
        f = f.decode('utf-8')

        outdata = f.replace('\t', '')
        outdata = str(outdata).replace(' ', '')# 去除制表符、换行符等符号
        outdata = str(outdata).replace('\n', '')
        outdata = str(outdata).replace('\r', '')

        sentences = self.cut(outdata)
        project_key = ["index", "project_id", "content"]
        project_value = [[index, project_id, sentence] for index, sentence in enumerate(sentences)]
        content_info_list = []
        for i in project_value:
            content_info_dict = dict(zip(project_key, i))
            content_info_list.append(content_info_dict)
        project_db.insert_content(content_info_list)

        len_sentences = len(sentences)
        label_list = label_users.split(",")
        allocation_list = split_list_above(range(len_sentences), user_list=label_list, group_num=len(label_list))
        # for key, values in allocation_list.items():
        #     for value in values:
        #         project_db.update_article_userid(value,str(project_id),key)
        project_db.update_article_userid(allocation_list, str(project_id), len_sentences)

    def delete(self):
        db = MongoInstance()

        json_parser = RequestParser()

        json_parser.add_argument('project_id', required=True, location='args')
        args = json_parser.parse_args()

        project_id = args.project_id
        db.delete_project_info(project_id)

        return jsonify(error=RET.OK, message='项目已删除')



    @staticmethod
    def cut(content):
        '''
        将文章切分为句子
        '''
        end_flag = ['。', '：', '；']  # 定义句子的结束符号
        content_len = len(content)
        sentences = []
        tmp_char = ''
        for idx, char in enumerate(content):
            tmp_char += char  # 拼接字符
            if (idx + 1) == content_len:  # 判断句子是否读完
                sentences.append(tmp_char)
                break

            if char in end_flag:  # 判断下一个字符是否为结束符号，如果是结束符号，切分句子
                next_idx = idx + 1
                if not content[next_idx] in end_flag:
                    sentences.append(tmp_char)

                    tmp_char = ''
        return sentences

upload_api.add_resource(Upload, '/', endpoint="upload")
