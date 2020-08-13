import unittest

from main.entity.database import BlockOutDates
from main.entity.database import Member
from main.utils.logger import Logger
from main.utils.roster_maker import *


class TestRosterMaker(unittest.TestCase):
    def setUp(self):
        random.seed(1234)
        self.log = Logger(__name__)
        ids = [i for i in range(10)]
        random.shuffle(ids)
        self.all_members = [Member(telegram_id=i) for i in ids]
        for m in self.all_members:
            if int(m.get_datafield(FIELD_TELEGRAM_ID)) > 6:
                m.document_obj[FIELD_ROLE] = ROLE_LEADER
            else:
                m.document_obj[FIELD_ROLE] = ROLE_MEMBER
        self.block_out_dates = BlockOutDates(
            block_out_dates={str(k): [] for k in range(4)}
        )

    def test_split_leaders_and_members(self):
        self.log.info(self.all_members)
        leaders, members = split_leaders_and_members(self.all_members)
        for l in leaders:
            assert l.get_datafield("Role") != "Member"
        for m in members:
            assert m.get_datafield("Role") == "Member"
