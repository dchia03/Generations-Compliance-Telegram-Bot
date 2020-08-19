from pymongo import MongoClient


class Database(object):

    def __init__(self, mongo_client_str, database_name):
        client = MongoClient(mongo_client_str)
        self.database_name = database_name
        self.db = client.get_database(database_name)

    def get_database(self):
        return self.db

    def get_database_name(self):
        return self.database_name
