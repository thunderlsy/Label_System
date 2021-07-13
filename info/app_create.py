from flask import Flask
from flask_cors import CORS
from info.app_config import config_dict, RUN_MODEL, LOG_DIRECTORY
from login import login_bp
from upload import upload_bp
from index import index_bp
from make import make_bp
from download import download_bp
from edit import label_edit_bp, relation_edit_bp, user_edit_bp
import logging
from logging.handlers import RotatingFileHandler


def setup_log(config):
    """

    :param config: 項目運行模式
    :return:
    """
    # 设置日志的的登记
    logging.basicConfig(level=config_dict[config].LOG_LEVEL)
    # 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
    file_log_handler = RotatingFileHandler(LOG_DIRECTORY, maxBytes=1024 * 1024 * 100, backupCount=100)
    # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
    # 为日志记录器设置记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaks app使用的）加载日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config):
    """
    创建Flask应用
    :param config: 配置对象
    :return: Flask应用
    """
    setup_log(config)
    the_app = Flask(__name__)
    CORS(the_app)
    config_class = config_dict[config]
    the_app.config.from_object(config_class)

    return the_app


app = create_app(RUN_MODEL)

from utility.middleware import jwt_authorization
app.before_request(jwt_authorization)

app.register_blueprint(login_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(index_bp)
app.register_blueprint(make_bp)
app.register_blueprint(label_edit_bp)
app.register_blueprint(relation_edit_bp)
app.register_blueprint(user_edit_bp)
app.register_blueprint(download_bp)
