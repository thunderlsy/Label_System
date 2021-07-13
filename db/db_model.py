from db.db_connect import MongoDBClient
# from db_connect import MongoDBClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import ast


class MongoInstance(MongoDBClient):

    def __init__(self):
        super().__init__()

    def get_all_projects(self):
        PROJECT_COLLECTIONS = 'project'

        return list(self.db[PROJECT_COLLECTIONS].find({}))

    def get_user(self, dict):
        USER_COLLECTIONS = 'users'
        return self.db[USER_COLLECTIONS].find_one(dict)
        # self.db[USER_COLLECTIONS].insert(dict)

    def get_role_id1(self):
        USERS_COLLECTIONS = 'users'
        return list(self.db[USERS_COLLECTIONS].find({"role_id": "1"}))

    def insert_project(self, name, description, update, create_id, label_users):
        PROJECT_COLLECTION = "project"
        project_info = {
            "name": name,
            "description": description,
            "update": update,
            "create_id": create_id,
            "label_users": label_users
        }
        insert_one_project_id = self.db[PROJECT_COLLECTION].insert_one(project_info)
        project_id = str(insert_one_project_id.inserted_id)
        return str(project_id)

    def update_article_userid(self, allocation, project_id, len_sentences):
        article_collections = 'article_info'
        rates_collections = 'rates'

        allocation_len = {}
        for key, value in allocation.items():
            self.db[article_collections].update_many({"index": {"$in": value}, "project_id": project_id},
                                                     {"$set": {"marker_userid": key}})
            # allocation_len.append({key: [0, len(value)]})
            allocation_len[key] = [0, len(value)]

        rates_init = {
            'project_id': project_id,
            'maker_rate': allocation_len,
            'inspector_rate': 0,
            # 'reviewer_rate': 0,
            'project_rate': len_sentences
        }
        rate_result = self.db[rates_collections].insert_one(rates_init)
        # rate_result.inserted_id

    def insert_content(self, content_dict):
        BEFORE_MARK_COLLECTION = 'article_info'
        return self.db[BEFORE_MARK_COLLECTION].insert_many(content_dict)

    def delete_project_info(self, project_id):
        project_collections = 'project'
        article_collections = 'article_info'
        label_collections = 'labels'
        relation_collections = 'relations'
        rates_collections = 'rates'
        project_id_info = {
            '_id': ObjectId(project_id)
        }
        project_dict = {
            'project_id': project_id
        }
        self.db[project_collections].delete_one(project_id_info)
        self.db[article_collections].delete_many(project_dict)
        self.db[label_collections].delete_many(project_dict)
        self.db[relation_collections].delete_many(project_dict)
        self.db[rates_collections].delete_one(project_dict)

    def insert_test_data(self, dict):
        USER_COLLECTIONS = 'users'
        # self.db[USER_COLLECTIONS].insert(dict)

    def get_create_project_info(self, user_id):
        PROJECT_COLLECTION = 'project'
        all_create_project = self.db[PROJECT_COLLECTION].find({"create_id": user_id})
        create_project_info = []
        for j in all_create_project:
            create_project_info.append(
                {"name": j.get("name"), "description": j.get("description"), "update": j.get("update"),
                 "project_id": str(j.get("_id"))})
        return create_project_info

        # return self.db[USER_COLLECTIONS].insert(dict)

    '''标注详情页查询进度'''

    def get_maker_rate(self, project_id, user_id):
        RATES_COLLECTION = 'rates'

        project_rate = self.db[RATES_COLLECTION].find_one({"project_id": project_id})
        all_maker_rate = project_rate.get("maker_rate", "")
        maker_rate = all_maker_rate.get(user_id, [None, None])
        return maker_rate

    def get_label_project_info(self, user_id):
        PROJECT_COLLECTION = 'project'
        RATES_COLLECTION = 'rates'
        all_project_info = self.db[PROJECT_COLLECTION].find({})

        label_project_info = []
        for k in all_project_info:
            label_users_id_str = k.get("label_users", "")
            label_users_list = label_users_id_str.split(",")
            if user_id in label_users_list:
                project_id = str(k.get("_id"))

                rates_info = self.db[RATES_COLLECTION].find_one({"project_id": project_id})
                all_maker_rate = rates_info.get("maker_rate", "")
                maker_rate = all_maker_rate.get(user_id, [None, None])
                maker_rate_percentage = str(int(maker_rate[0]/maker_rate[1]*100))

                label_project_info.append(
                    {"name": k.get("name"),
                     "description": k.get("description"),
                     "update": k.get("update"),
                     "project_id": project_id,
                     # "maker_rating": maker_rate[0],
                     "maker_rate": maker_rate_percentage}
                )
        return label_project_info

    '''一审详情页进度'''

    def get_inspector_rate(self, project_id):
        RATES_COLLECTION = 'rates'
        rates_info = self.db[RATES_COLLECTION].find_one({"project_id": project_id})
        inspector_rate = rates_info.get("inspector_rate", "")
        project_rate = rates_info.get("project_rate", "")
        return inspector_rate, project_rate

    def get_first_project_info(self):
        PROJECT_COLLECTION = 'project'
        RATES_COLLECTION = 'rates'
        all_project_info = self.db[PROJECT_COLLECTION].find({})

        '''
        {'_id': ObjectId('60bd70b0fbc334eb66ead0d3'), 'name': '2021_06_07', 'description': '早上测试文件', 'update': '2021-06-07 09:04:48', 'create_id': '60b9cd99891ee0397838b016', 'label_users': '60b5a4117b2a0c68a51874b7,60b724417b2a0c68a51874b9'}
        {'_id': ObjectId('60bd8ed743e1e87c68e4433b'), 'name': '4', 'description': '4', 'update': '2021-06-07 11:13:27', 'create_id': '60bd8ccb891ee0397838b019', 'label_users': '60b5a4117b2a0c68a51874b7,60b724417b2a0c68a51874b9,60b9cd99891ee0397838b016'}
        '''

        first_project_info = []
        for k in all_project_info:
            project_str = str(k.get("_id"))
            rates_info = self.db[RATES_COLLECTION].find_one({"project_id": project_str})
            inspector_rate = rates_info.get("inspector_rate", "")
            project_rate = rates_info.get("project_rate", "")

            maker_rate = str(int(inspector_rate / project_rate * 100))
            first_project_info.append(
                {"name": k.get("name"),
                 "description": k.get("description"),
                 "update": k.get("update"),
                 "project_id": project_str,
                 "maker_rate": maker_rate}
            )
            pass
        return first_project_info

    def update_article_mark(self, article_index, project_id, dict_labels, dict_relations, html_data):
        article_collections = 'article_info'
        dict_labels = ast.literal_eval(dict_labels)
        dict_relations = ast.literal_eval(dict_relations)
        article_index = int(article_index)
        self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
            "$set": {"marker_labels": dict_labels, "marker_relations": dict_relations, "html_data": html_data}})

    def update_make_rate(self, project_id, user_id):
        rate_collection = 'rates'

        '''更新进度'''
        condition = {"project_id": project_id}
        rate_info = self.db[rate_collection].find_one(condition)
        rate_info['maker_rate'][user_id][0] += 1
        result = self.db[rate_collection].update_one(condition, {'$set': rate_info})

    def update_inspect_rate(self, project_id):
        rate_collection = 'rates'

        '''更新进度'''
        condition = {"project_id": project_id}
        rate_info = self.db[rate_collection].find_one(condition)
        rate_info['inspector_rate'] += 1
        result = self.db[rate_collection].update_one(condition, {'$set': rate_info})

    def update_article_inspect(self, article_index, project_id, dict_labels, dict_relations, html_data):
        article_collections = 'article_info'
        article_index = int(article_index)
        mark = self.db[article_collections].find_one({"index": article_index, "project_id": project_id})
        marker_labels = mark["marker_labels"]
        marker_relations = mark["marker_relations"]
        dict_labels = ast.literal_eval(dict_labels)
        dict_relations = ast.literal_eval(dict_relations)
        mark_name = []
        inspect_name = []
        """
        判断一审和标注员标签是否相同       
        """
        if dict_labels == "[]":
            self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
                "$set": {"inspector_labels": dict_labels, "inspector_relations": dict_relations,
                         "html_data": html_data, "reviewer_labels": "[]"}})
        elif len(marker_labels) == len(dict_labels):
            for i in range(len(marker_labels)):
                mark_name.append(marker_labels[i]['name'])
                inspect_name.append(dict_labels[i]['name'])
            if mark_name == inspect_name:
                self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
                    "$set": {"inspector_labels": dict_labels, "inspector_relations": dict_relations,
                             "html_data": html_data, "reviewer_labels": dict_labels}})
            else:
                self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
                    "$set": {"inspector_labels": dict_labels, "inspector_relations": dict_relations,
                             "html_data": html_data}})
        else:
            self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
                "$set": {"inspector_labels": dict_labels, "inspector_relations": dict_relations,
                         "html_data": html_data}})

        mark_relation = []
        inspect_relation = []
        """
        判断一审和标注员选择的关系是否相同       
        """
        if len(marker_relations) == len(dict_relations):
            for i in range(len(marker_relations)):
                mark_relation.append(marker_relations[i]["value_first"])
                mark_relation.append(marker_relations[i]["value_last"])
                mark_relation.append(marker_relations[i]["relation"])
                inspect_relation.append(dict_relations[i]["value_first"])
                inspect_relation.append(dict_relations[i]["value_last"])
                inspect_relation.append(dict_relations[i]["relation"])
            if mark_relation == inspect_relation:
                self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
                    "$set": {"reviewer_relations": dict_relations}})

    def update_article_review(self, article_index, project_id, dict_labels, dict_relations, html_data):
        article_collections = 'article_info'
        article_index = int(article_index)
        dict_labels = ast.literal_eval(dict_labels)
        dict_relations = ast.literal_eval(dict_relations)
        self.db[article_collections].update_one({"index": article_index, "project_id": project_id}, {
            "$set": {"reviewer_labels": dict_labels, "reviewer_relations": dict_relations, "html_data": html_data}})

    def find_article(self, user_id, project_id):
        article_collections = 'article_info'
        article_content = self.db[article_collections].find_one(
            {"marker_userid": user_id, "project_id": project_id, "marker_labels": None})
        # article_content=self.db[article_collections].find_one({})
        return article_content

    def find_article_inspect(self, project_id):
        article_collections = 'article_info'
        article_content = self.db[article_collections].find_one(
            {"marker_labels": {"$ne": None}, "inspector_labels": None, "project_id": project_id})
        return article_content

    def find_article_review(self, project_id):
        article_collections = 'article_info'
        article_content = self.db[article_collections].find_one(
            {"inspector_labels": {"$ne": None}, "reviewer_labels": None, "project_id": project_id})
        return article_content

    def get_labels(self, project_id):
        '''
        查询项目标签
        :param project_id: 项目id
        :return: 该项目下所有标签
        '''
        label_collection = 'labels'
        find_dict = {
            'project_id': project_id
        }
        label_cursor = self.db[label_collection].find(find_dict)
        label_list = []
        for j in label_cursor:
            one_label_dict = {
                'label_id': str(j.get("_id")),
                'name': j.get("name"),
                'color': j.get("color", ""),
                'shortcut_key': j.get("shortcut_key", ""),
                'keycode': j.get("keycode", ""),
                'project_id': j.get("project_id")
            }
            label_list.append(one_label_dict)
        return label_list

    def add_label(self, name, color, shortcut_key, keycode, project_id):
        '''
        新增项目标签
        :param name: 标签名
        :param color: 标签颜色
        :param shortcut_key: 标签快捷键
        :param project_id: 项目id
        :return:
        '''
        label_collection = "labels"
        add_dict = {
            'name': name,
            'color': color,
            'shortcut_key': shortcut_key,
            'keycode': keycode,
            'project_id': project_id
        }
        self.db[label_collection].insert_one(add_dict)

    def delete_label(self, label_id):
        '''
        删除项目标签
        :param project_id: 标签id
        :return:
        '''
        label_collection = 'labels'

        delete_dict = {
            '_id': ObjectId(label_id)
        }
        self.db[label_collection].delete_one(delete_dict)

    def get_relation(self, project_id):
        '''
        查询关系列表
        :param project_id: 项目id
        :return: 该项目关系列表
        '''
        relation_collection = 'relations'

        find_dict = {
            'project_id': project_id
        }

        relation_cursor = self.db[relation_collection].find(find_dict)
        relation_list = []
        for k in relation_cursor:
            one_relation_dict = {
                'relation_id': str(k.get("_id")),
                'name': k.get("name", ""),
                "project_id": k.get("project_id", "")
            }
            relation_list.append(one_relation_dict)
        return relation_list

    def add_relation(self, name, project_id):
        '''
        新增关系
        :param name: 关系名
        :param project_id: 项目名
        :return: 该项目关系列表
        '''
        relation_collection = 'relations'

        add_dict = {
            'name': name,
            'project_id': project_id
        }

        self.db[relation_collection].insert_one(add_dict)

    def delete_relation(self, relation_id):
        '''
        删除关系
        :param relation_id: 关系id
        :return:
        '''
        relation_collection = 'relations'

        delete_dict = {
            '_id': ObjectId(relation_id)
        }
        self.db[relation_collection].delete_one(delete_dict)

    # def init_rates(self):
    #     pass
    def get_label_article_info(self, project_id):
        ARTICLE_COLLECTION = 'article_info'
        mongo_data_list = []
        documents = self.db[ARTICLE_COLLECTION].find({"project_id": project_id})
        for document in documents:
            mongo_data_dict = {}
            content = document.get("content")
            reviewer_labels = document.get("reviewer_labels")
            reviewer_relations = document.get("reviewer_relations")
            mongo_data_dict.update({"content": content})
            mongo_data_dict.update({"reviewer_labels": reviewer_labels})
            mongo_data_dict.update({"reviewer_relations": reviewer_relations})
            mongo_data_list.append(mongo_data_dict)
        return mongo_data_list

    def get_project_name(self, project_id):
        '''
        获取项目name
        :param project_id: 项目ID
        :return: 项目name
        '''
        project_collection = 'project'
        project_dict = {
            '_id': ObjectId(project_id)
        }
        project_info = self.db[project_collection].find_one(project_dict)
        project_name = project_info.get('name', '')
        return project_name

    def result_with_article(self, project_id):
        '''
        获取项目是否可以下载
        :param project_id: 项目ID
        :return: 可下载返回True 否则返回false
        '''
        article_collection = 'article_info'

        project_dict = {
            'reviewer_labels': None,
            'project_id': project_id
        }
        article_info = self.db[article_collection].find_one(project_dict)
        if article_info:
            return False
        else:
            return True

    def users_without_admin(self):
        '''
        获取所有除admin以外的账号信息
        :return:
        '''
        users_collection = "users"
        users_dict = {
            'role_id': {'$ne': "5"}
        }
        users_info = self.db[users_collection].find(users_dict)
        result = []

        for j in users_info:
            # role_id = j.get("role_id")
            user_info_dict = {
                'user_id': str(j.get("_id")),
                "name": j.get("name"),
                "password": j.get("password"),
                "worknumber": j.get("worknumber"),
                "role_id": j.get("role_id")
            }
            result.append(user_info_dict)
        return result

    def all_project_info(self):
        '''
        获取所有可编辑的项目信息
        :return:
        '''
        project_collection = 'project'
        users_collection = "users"
        rates_collection = "rates"

        project_info = self.db[project_collection].find()

        project_list = []
        for j in project_info:
            create_id = j.get("create_id")
            user_info = self.db[users_collection].find_one({"_id": ObjectId(create_id)})
            user_name = user_info.get("name")

            # 组织进度
            project_id = str(j.get("_id"))
            project_rate_info = self.db[rates_collection].find_one({"project_id": project_id})
            maker_rate = project_rate_info.get("maker_rate")
            label_rate = {}

            # maker_rate_percentage = str(int(maker_rate[0] / maker_rate[1] * 100))

            for k, p in maker_rate.items():
                label_user = self.db[users_collection].find_one({"_id": ObjectId(k)})
                label_name = label_user.get("name")
                # label_rate[label_name] = str(p[0]) + "/" + str(p[1])
                label_rate[label_name] = str(int(p[0] / p[1] * 100))

            # inspector_rate = str(project_rate_info.get("inspector_rate", "")) + "/" + str(
            #     project_rate_info.get("project_rate", ""))
            inspector_rate = project_rate_info.get("inspector_rate", "")
            project_rate = project_rate_info.get("project_rate", "")
            inspector_percentage = str(int(inspector_rate / project_rate * 100))

            project_dict = {
                "project_id": str(j.get("_id")),
                "name": j.get("name"),
                "description": j.get("description"),
                "update": j.get("update"),
                "create_user": user_name,
                "maker_rate": label_rate,
                "inspector_rate": inspector_percentage
            }
            project_list.append(project_dict)

        return project_list

    def get_worknumber_repeat(self, worknumber):
        user_collection = "users"

        user_info = self.db[user_collection].find_one({"worknumber": worknumber})

        if not user_info:
            return False
        else:
            return True

    def add_user(self, worknumber, password, name, role_id):
        user_collection = "users"
        user_dict = {
            "worknumber": worknumber,
            "password": password,
            "name": name,
            "role_id": role_id
        }

        insert_result = self.db[user_collection].insert_one(user_dict)
        return insert_result.inserted_id

    def delete_user(self, user_id):
        user_collection = "users"
        self.db[user_collection].delete_one({"_id": ObjectId(user_id)})

    # ==============================================================================
    # TODO:密码加密
    def checkout_pw(self):
        check_dict = {"worknumber": "F7691717", "password": "lishuyi"}
        USER_COLLECTIONS = 'users'

    @staticmethod
    def check_password(hash, password):
        return check_password_hash(hash, password)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def test(self):

        input_data = {"0": [1, 6, 5, 7, 9], "1": [2, 3, 4, 8]}
        for key, value in input_data.items():
            self.db.test.update_many({"index": {"$in": value}}, {"$set": {"marker_userid": key}})


if __name__ == '__main__':
    a = MongoInstance()

    # result = a.result_with_article("60c9ac85f0a1b9d34bedb279")
    # print(result)
    result = a.get_worknumber_repeat("4613")
    # print(result)
    if not result:
        print(False)
    else:
        print(True)


    # print(a.get_all_projects())
    # a.update_article_mark(article_index=0,project_id="60bd70b0fbc334eb66ead0d3",dict_labels="test",dict_relations="test",html_data="test")
    # b = a.get_all_projects()
    # for i in b:
    #     print(i)

    # <__main__.MongoInstance object at 0x108d19350>
    # print(b)

    # print(a.get_label_project_info("1"))
    # b = a.get_label_project_info("1")
    # for i in b:
    #     print(i)
    # pass
