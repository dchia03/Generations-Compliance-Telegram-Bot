import random
import unittest

from main.constants.field_names import FIELD_NAME, FIELD_ROLE, ROLE_MEMBER, ROLE_LEADER
from main.entity.document.impl.block_out_dates import BlockOutDates
from main.entity.document.impl.member import Member
from main.entity.document.impl.roster import Roster
from main.utils.logger import Logger
from main.utils.roster_maker_2 import build_roster


class TestRosterMaker(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)
        self.members = [
            Member(member_details={FIELD_NAME: "Matthew", FIELD_ROLE: ROLE_MEMBER}),
            Member(member_details={FIELD_NAME: "Mark", FIELD_ROLE: ROLE_MEMBER}),
            Member(member_details={FIELD_NAME: "Luke", FIELD_ROLE: ROLE_LEADER}),
            Member(member_details={FIELD_NAME: "John", FIELD_ROLE: ROLE_MEMBER}),
            Member(member_details={FIELD_NAME: "Reuben", FIELD_ROLE: ROLE_MEMBER}),
            Member(member_details={FIELD_NAME: "David", FIELD_ROLE: ROLE_LEADER}),
            Member(member_details={FIELD_NAME: "Moses", FIELD_ROLE: ROLE_MEMBER}),
            Member(member_details={FIELD_NAME: "Joseph", FIELD_ROLE: ROLE_LEADER}),
            Member(member_details={FIELD_NAME: "Jacob", FIELD_ROLE: ROLE_MEMBER})
        ]
        self.prev_roster = Roster()

    def test_build_roster(self):
        self.block_out_dates = BlockOutDates(block_out_dates={
            "1": ["Joseph", "David", "Reuben"],
            "2": ["Matthew", "Moses", "Joseph", "Reuben"],
            "3": ["Matthew", "Mark", "Luke", "John", "David"],
            "4": []
        })
        # self.log.info(build_roster(self.members, self.block_out_dates, self.prev_roster).get_roster_str())

        for i in range(10):
            self.log.info(build_roster(self.members, self.block_out_dates, self.prev_roster).get_roster_str())

        # 1: Luke, Jacob, Matthew
        # 2: David, John, Mark
        # 3: Joseph, Reuben, Moses
        # 4: David, John, Mark

    def test_build_roster_no_leader(self):
        self.block_out_dates = BlockOutDates(block_out_dates={
            "1": ["Joseph", "David", "Reuben", "Luke"],
            "2": ["Matthew", "Moses", "Joseph", "Reuben", "Luke"],
            "3": ["Matthew", "Mark", "Luke", "John", "David"],
            "4": ["Luke"]
        })

        self.log.info(build_roster(self.members, self.block_out_dates, self.prev_roster))

    def test_build_roster_not_enough_members(self):
        self.block_out_dates = BlockOutDates(block_out_dates={
            "1": ["Joseph", "David", "Reuben", "Luke"],
            "2": ["Matthew", "Moses", "Joseph", "Reuben", "Luke"],
            "3": ["Matthew", "Mark", "Luke", "John", "David"],
            "4": ["Matthew", "Mark", "Luke", "John", "Reuben", "David", "Moses", "Joseph", "Jacob"]
        })

        self.log.info(build_roster(self.members, self.block_out_dates, self.prev_roster))

    def test_build_roster_2(self):
        self.block_out_dates = BlockOutDates(block_out_dates={
            "1": [],
            "2": [],
            "3": [],
            "4": []
        })
        for i in range(10):
            self.log.info(build_roster(self.members, self.block_out_dates, self.prev_roster).get_roster_str())

    def test_build_roster_3(self):
        self.block_out_dates = BlockOutDates(block_out_dates={
            "1": ["Mark", "Luke", "Reuben", "David", "Moses", "Jacob"],
            "2": ["Mark", "John", "Reuben", "David", "Moses"],
            "3": ["Matthew", "Luke", "Reuben", "Moses", "Joseph", "Jacob"],
            "4": ["Matthew", "Mark", "John", "Reuben", "Moses", "Joseph"]
        })

        self.log.info(build_roster(self.members, self.block_out_dates, self.prev_roster).get_roster_str())

    def test_random(self):
        ls = [
            ["a", 1],
            ["b", 1],
            ["c", 1],
            ["d", 2],
            ["e", 3],
            ["f", 3],
            ["g", 3],
            ["h", 4],
            ["i", 4],
            ["j", 4],
            ["k", 4]
        ]
        self.log.info(ls)
        random.shuffle(ls)
        self.log.info(ls)
        self.log.info(sorted(ls, key=lambda x: x[1]))
