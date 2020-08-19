from telegram import ReplyKeyboardRemove

from main.constants.field_names import *
from main.entity.document.base.document_base import Document
from main.entity.document.common.common_document_function_store import *
from main.stores.helper_function_store import make_keyboard_reply_markup
from main.utils.logger import Logger

log = Logger(__name__)


class Member(Document):
    NON_VIEWING_FIELDS = [FIELD_TELEGRAM_ID]
    ALL_FIELDS_REPLY_MARKUP = {
        FIELD_TELEGRAM_ID: ReplyKeyboardRemove(),
        FIELD_FULL_NAME: ReplyKeyboardRemove(),
        FIELD_NAME: ReplyKeyboardRemove(),
        FIELD_DOB: ReplyKeyboardRemove(),
        FIELD_HP: ReplyKeyboardRemove(),
        FIELD_CELL_GROUP: ReplyKeyboardRemove(),
        FIELD_CELL_LEADER: ReplyKeyboardRemove(),
        FIELD_BAPTISED: make_keyboard_reply_markup([[BAPTISED_YES, BAPTISED_NO]]),
        FIELD_ROLE: make_keyboard_reply_markup([[ROLE_MEMBER]])
    }
    ALL_FIELDS_ENTRY_EGS = {
        FIELD_TELEGRAM_ID: None,
        FIELD_FULL_NAME: "John Smith Wei Xiang",
        FIELD_NAME: "John Smith",
        FIELD_DOB: "DD/MM/YYYY",
        FIELD_HP: "91234567",
        FIELD_CELL_GROUP: "GY 1.1",
        FIELD_CELL_LEADER: "Matt Chen",
        FIELD_BAPTISED: "Yes or No",
        FIELD_ROLE: "Member"
    }
    EDITABLE_FIELDS = [
        FIELD_FULL_NAME, FIELD_NAME, FIELD_DOB, FIELD_HP,
        FIELD_CELL_GROUP, FIELD_CELL_LEADER, FIELD_BAPTISED
    ]

    def __init__(self, member_details=None, telegram_id=""):
        super().__init__(
            all_fields=[
                FIELD_TELEGRAM_ID, FIELD_FULL_NAME, FIELD_NAME, FIELD_DOB, FIELD_HP,
                FIELD_CELL_GROUP, FIELD_CELL_LEADER, FIELD_BAPTISED, FIELD_ROLE
            ],
            all_fields_data_type={
                FIELD_TELEGRAM_ID: str,
                FIELD_FULL_NAME: str,
                FIELD_NAME: str,
                FIELD_DOB: str,
                FIELD_HP: str,
                FIELD_CELL_GROUP: str,
                FIELD_CELL_LEADER: str,
                FIELD_BAPTISED: str,
                FIELD_ROLE: str
            },
            all_fields_data_format={
                FIELD_TELEGRAM_ID: is_telegram_id,
                FIELD_FULL_NAME: is_full_name,
                FIELD_NAME: is_name,
                FIELD_DOB: is_dob,
                FIELD_HP: is_hp,
                FIELD_CELL_GROUP: is_cell_group,
                FIELD_CELL_LEADER: is_cell_leader,
                FIELD_BAPTISED: is_baptised,
                FIELD_ROLE: is_role
            },
            non_editable_fields=[FIELD_TELEGRAM_ID, FIELD_ROLE],
            document_details=member_details
        )
        if member_details is None:
            self.get_document()[FIELD_ROLE] = ROLE_MEMBER
            self.get_document()[FIELD_TELEGRAM_ID] = telegram_id

    def __eq__(self, member):
        if isinstance(member, Member):
            return self.get_datafield(FIELD_NAME) == member.get_datafield(FIELD_NAME)
        return False

    def __str__(self):
        return str(self.get_document())

    def __repr__(self):
        return str(self.get_document())

    def is_empty(self):
        return self.get_telegram_id() is None or self.get_telegram_id() == ""

    def get_member_str(self):
        msg = "Member Details\n\n"
        is_empty_details = True
        for field in self.EDITABLE_FIELDS:
            is_empty_details &= self.get_document()[field] is None
        if not is_empty_details:
            for field in self.all_fields:
                if field not in self.NON_VIEWING_FIELDS and field != self.DOC_ID_FIELD:
                    msg += "{}: {}\n".format(field, self.get_datafield(field))
        else:
            msg += "*** No Records ***"
        msg += "\n"
        return msg

    def get_telegram_id(self):
        return self.get_datafield(FIELD_TELEGRAM_ID)

    def get_full_name(self):
        return self.get_datafield(FIELD_FULL_NAME)

    def get_name(self):
        return self.get_datafield(FIELD_NAME)

    def get_dob(self):
        return self.get_datafield(FIELD_DOB)

    def get_hp(self):
        return self.get_datafield(FIELD_HP)

    def get_cell_group(self):
        return self.get_datafield(FIELD_CELL_GROUP)

    def get_cell_leader(self):
        return self.get_datafield(FIELD_CELL_LEADER)

    def get_baptised(self):
        return self.get_datafield(FIELD_BAPTISED)

    def get_role(self):
        return self.get_datafield(FIELD_ROLE)
