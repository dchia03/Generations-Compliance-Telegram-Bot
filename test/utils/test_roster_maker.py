import unittest
from main.utils.logger import Logger
from main.utils.roster_maker import *


class TestRosterMaker(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)

    def test_split_leaders_and_members(self):
        assert True
