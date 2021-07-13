from db.db_connect import MongoDBClient


class InitMongoData(MongoDBClient):

    def __init__(self):

        super().__init__()
        CONFIG = 'config'
        self.config = self.db[CONFIG]


    def insert_tablehead_to_config(self):
        '''
        插入當前路徑的 config.csv 數據到 label_system 下的 config collection
        :return: None
        '''
        import pandas as pd

        # all_table_heads = [
        #     {"description": "項目表",
        #     "field_list": []}
        # ]
        data = pd.read_csv('./config.csv')

        for index, row in data.T.to_dict().items():

            self.config.insert_one(row)

        # return insert_action

    def get_all_config_file(self):

        return self.config.find({})




if __name__ == '__main__':
    a = InitMongoData()
    a.insert_tablehead_to_config()
    # print(list(a.get_all_config_file()))