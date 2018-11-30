from pymongo import MongoClient

class Mymongo(object):
    instance = None

    def __init__(self):
        '''
        创建mongo实例
        '''
        info = {
            "url" : '118.25.38.240',
            "port" : 27017,
            'db' : 'spider_test',
            'user' : 'spider',
            'pass' : 'spider123',
            'table' : 'weipan',
        }
        self.client = MongoClient(info['url'], info['port'])
        # 选择使用的数据库
        db_auth = self.client[info['db']]
        # 验证登陆
        db_auth.authenticate(info['user'], info['pass'])
        self.db = self.client[info['db']]
        self.table = self.db[info['table']]

    def __del__(self):
        '''
        销毁时，断开链接
        :return:
        '''
        self.client.close()


    @classmethod
    def get_instance(cls):
        if Mymongo.instance:
            return Mymongo.instance
        else:
            Mymongo.instance = Mymongo()
            return Mymongo.instance