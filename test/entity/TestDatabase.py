import unittest
from main.entity.Database import Database
import properties as props


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database(props.mongo_client_str, "Test")

    def test_db(self):
        assert(self.database.get_database() is not None)

    def test_db_name(self):
        assert(self.database.get_database_name() == "Test")
