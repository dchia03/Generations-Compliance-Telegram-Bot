import unittest
from unittest.mock import patch, MagicMock

from mongomock import MongoClient

from main.utils.logger import Logger


class TestCollection(unittest.TestCase):
    @patch('main.entity.collection.Collection')
    def setUp(self, mock_collection):
        self.log = Logger(__name__)
        self.mock_database_name = "mock_database_name"
        self.mock_collection_name = "mock_collection_name"
        self.mock_mongo_client_str = "mock_mongo_client_str"
        mock_collection.database = MagicMock()
        mock_collection.database_name = self.mock_database_name
        mock_collection.collection_name = self.mock_collection_name
        temp_mongo_client = MongoClient(self.mock_mongo_client_str)
        self.mock_mongo_collection = temp_mongo_client\
            .get_database(self.mock_database_name)\
            .create_collection(self.mock_collection_name)
        self.mock_collection = mock_collection
        self.mock_collection_data = [
            {"field1": "value1"},
            {"field2": "value2"},
            {"field3": "value3"}
        ]
        self.populate_collection(self.mock_collection_data)
        mock_collection.c = self.mock_mongo_collection
        mock_collection.get_collection.return_value = self.mock_mongo_collection

    def populate_collection(self, data_list):
        for data in data_list:
            self.mock_mongo_collection.insert_one(data)

    def test_collection(self):
        print(self.mock_collection)
        print(self.mock_collection.get_collection_list())
