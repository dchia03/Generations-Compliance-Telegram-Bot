import unittest

from main.database.member import Member, is_telegram_id, is_role
from main.utils.logger import Logger


class TestMember(unittest.TestCase):
    def setUp(self):
        self.log = Logger(__name__)

    def test_member(self):
        m = Member(telegram_id="1234")
        values = [
            "Test User Full Name", "Test Name", "01/01/2020", "91234567",
            "1.1", "John Smith", "No"
        ]
        for field, value in zip(Member.EDITABLE_FIELDS, values):
            assert m.set_datafield(field, value)

        self.log.info(m.get_member_str())

        for field, value in zip(Member.EDITABLE_FIELDS, values):
            assert m.get_datafield(field) == value

        update_values = [
            "Test_User_Full_Name", "Test_Name", "99/99/2020", "91234567890",
            1.1, "John_Smith", "FAIL"
        ]
        for field, value in zip(Member.EDITABLE_FIELDS, update_values):
            assert not m.update_datafield(field, value)

        m2 = Member(telegram_id="1234")
        for field, value in zip(Member.EDITABLE_FIELDS, values):
            assert m2.set_datafield(field, value)
        assert m2 == m

        m3_values = [
            "Test User Full Name", "Test Name Different", "01/01/2020", "91234567",
            "1.1", "John Smith", "No"
        ]
        m3 = Member(telegram_id="1234")
        for field, value in zip(Member.EDITABLE_FIELDS, m3_values):
            assert m3.set_datafield(field, value)
        assert m3 != m

        assert m != "NOT A MEMBER"

        self.log.info(str(m))
        self.log.info(repr(m))

        assert not is_telegram_id("123")
        assert is_telegram_id(123)
        assert is_role("Member")
        assert is_role("Ministry Head")
        assert is_role("Leader")
        assert not is_role("Not Role")

    def test_member_empty_field(self):
        m = Member(telegram_id="1234")
        for field in Member.EDITABLE_FIELDS:
            assert(m.get_datafield(field=field) is None)
        self.log.info(m.get_member_str())
