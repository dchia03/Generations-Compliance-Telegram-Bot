import unittest
from main.utils.logger import Logger
from main.database.roster import Roster, is_month, is_roster, is_year


class TestRoster(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
        self.roster_obj_1 = Roster()
        self.roster_obj_2 = Roster(
            roster={
                '1': ["Alice", "Bob"],
                '2': ["Charlie", "David"],
                '3': ["David", "Elvis"]
            }
        )

    def test_get_roster_str(self):
        roster_obj_1_str = self.roster_obj_1.get_roster_str()
        roster_obj_2_str = self.roster_obj_2.get_roster_str()
        self.log.info("Roster 1: " + roster_obj_1_str)
        self.log.info("Roster 2: " + roster_obj_2_str)
        assert roster_obj_1_str is not None
        assert roster_obj_2_str is not None

    def test_get_member_roster_dates_list(self):
        member_name = "David"
        res1 = self.roster_obj_1.get_member_roster_dates_list(member_name)
        res2 = self.roster_obj_2.get_member_roster_dates_list(member_name)
        assert len(res1) == 0
        assert len(res2) == 2

    def test_get_member_roster_dates_str(self):
        member_name = "David"
        res1 = self.roster_obj_1.get_member_roster_dates_str(member_name)
        res2 = self.roster_obj_2.get_member_roster_dates_str(member_name)
        self.log.info("Roster 1: " + res1)
        self.log.info("Roster 2: " + res2)
        assert res1 is not None
        assert res2 is not None

    def test_is_month(self):
        assert is_month("January")
        assert not is_month("David")

    def test_is_year(self):
        assert is_year(2019)
        assert not is_year("David")

    def test_is_roster(self):
        assert is_roster(self.roster_obj_2.get_datafield("Roster"))
        assert not is_roster({"test": "fail"})
        assert not is_roster("David")