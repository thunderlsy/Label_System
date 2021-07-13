'''
項目運行的配置文件，供項目搭建時變更
'''
import logging

class DefaultConfig(object):
    """默认配置"""
    SECRET_KEY = 'chris!@#$%^&*()'
    # 防止前端中文显示为ASCII
    JSON_AS_ASCII = False

    # SERVER_NAME = "0.0.0.0:5002"
    # SERVER_NAME = "127.0.0.1:5002"
    SERVER_NAME = "10.141.6.133:5002"
    # SERVER_NAME = "10.141.7.65:5002"


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    # 日誌配置
    LOG_LEVEL = logging.WARNING
    # 數據庫
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_USER = 'admin'
    MONGO_PWD = 'admin'
    MONGO_DB = 'label_system'


class ProductionConfig(DefaultConfig):
    DEBUG = False

    LOG_LEVEL = logging.WARNING


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

# 传入的参数是development获取开发模式对应的app对象
# 传入的参数是production获取线上模式对应的app对象
RUN_MODEL = 'development'

LOG_DIRECTORY = 'logs/log'

