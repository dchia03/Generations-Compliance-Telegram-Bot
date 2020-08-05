import unittest

from pymongo.database import Database as MongoDatabase

from main.entity.database import Database
from main.utils.logger import Logger


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
        self.mock_mongo_client_str = "mock_mongo_client_str"
        self.mock_database_name = "mock_database_name"

    def test_database_init(self):
        db = Database(self.mock_mongo_client_str, self.mock_database_name)
        self.log.info(db.get_database())
        self.log.info(db.get_database_name())
        self.assertEqual(db.get_database_name(), self.mock_database_name)
        self.assertTrue(isinstance(db.get_database(), MongoDatabase))
