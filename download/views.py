import io
import json
import re
import time

from flask import request, g, jsonify, make_response
from flask_restful import Resource, Api
from openpyxl import Workbook
from flask_restful.reqparse import RequestParser
from db.db_model import MongoInstance
from utility.random_split import split_list_above
from utility.decorators import login_required
from info.response_code import RET
from openpyxl.writer.excel import save_virtual_workbook
from utility.str_Q_to_B import strQ2B
from io import BytesIO
import datetime

from download import download_bp

download_api = Api(download_bp)

'''下载'''


class Download(Resource):
    method_decorators = [login_required]

    def get(self):
        article_db = MongoInstance()
        json_parser = RequestParser()

        json_parser.add_argument('project_id', required=True, location='args')

        args = json_parser.parse_args()

        project_id = args.project_id

        result = article_db.result_with_article(project_id)
        if not result:
            return jsonify(error=RET.OK, message='项目未二审完毕')

        mongoDB_data = article_db.get_label_article_info(project_id)
        outwb = Workbook()
        outws = outwb.worksheets[0]
        # 遍历外层列表
        for new_dict in mongoDB_data:

            content = new_dict.get('content', '')
            reviewer_labels = new_dict.get('reviewer_labels', '')
            reviewer_relations = new_dict.get('reviewer_relations', '')
            B_str = ""
            C_str = ""
            for i in reviewer_labels:
                B_str = B_str + str(i) + ","
            B_str = B_str[:-1]
            for i in reviewer_relations:
                C_str = C_str + str(i) + ","
            C_str = C_str[:-1]
            row = [content, B_str, C_str]
            outws.append(row)

        # output = io.BytesIO()
        # outwb.save(filename=output)
        # output.seek(0)
        # resp = make_response(output.read())
        # resp.headers["Content-Disposition"] = 'attachment; filename=xxxx.xlsx'
        # resp.headers['Content-Type'] = 'application/x-xlsx'
        # return resp

        excel_data = save_virtual_workbook(outwb)
        project_name = article_db.get_project_name(project_id)
        from urllib.parse import quote
        from flask import send_file

        # 导出字节流的方式
        filename = quote((strQ2B(project_name) + ".xlsx").encode('utf-8'))
        response = send_file(BytesIO(excel_data),
                             as_attachment=True,
                             attachment_filename=filename,
                             mimetype='application/vnd.ms-excel')
        response.headers["Content-Disposition"] = "attachment; filename=" + filename
        response.headers['Content-Type'] = 'application/x-xlsx'
        response.headers['filename'] = filename
        response.headers["Access-Control-Expose-Headers"] = 'filename'
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


download_api.add_resource(Download, '/', endpoint="download")
