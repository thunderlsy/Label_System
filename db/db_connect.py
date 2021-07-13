from pymongo import MongoClient
import os

class MongoDBClient(object):
    # 饿汉式 单例模式
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MongoDBClient, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        # uri='mongodb://账号:密码@128.777.244.19:27017/admin'
        # self.mgdb=MongoClient(uri, connect=False, maxPoolSize=2000)
        from info.app_config import config_dict, RUN_MODEL
        mongo_dict = config_dict[RUN_MODEL]
        local_host = os.getenv('MONGO_HOST', mongo_dict.MONGO_HOST)
        local_port = os.getenv('MONGO_PORT', mongo_dict.MONGO_PORT)
        local_client = MongoClient(local_host, local_port, connect=False, maxPoolSize=2000)

        db_user = os.getenv('MONGO_USER', mongo_dict.MONGO_USER)
        password = os.getenv('MONGO_PWD', mongo_dict.MONGO_PWD)
        db = local_client.admin  # 注意:# 先连接系统默认数据库admin
        db.authenticate(db_user, password, mechanism='SCRAM-SHA-1')
        # self.online_client = client
        this_db = os.getenv('MONGO_DB', mongo_dict.MONGO_DB)
        self.db = local_client[this_db]



if __name__ == '__main__':

    test = MongoDBClient()
