import datetime as dt

from telegram import (
    ReplyKeyboardRemove
)

from main.common.constants import *
from main.entity.document import Document
from main.stores.helper_function_store import make_keyboard_reply_markup
from main.utils.logger import Logger

log = Logger(__name__)


def is_telegram_id(telegram_id):
    return type(telegram_id) == int


def is_name(name):
    for name_part in name.split(" "):
        if not name_part.strip().isalpha():
            return False
    return True


def is_full_name(full_name):
    return is_name(full_name)


def is_dob(dob):
    try:
        dt_format = "%d/%m/%Y"
        dt.datetime.strptime(dob, dt_format)
        return True
    except ValueError as e:
        log.error(e)
        return False


def is_hp(hp):
    return len(hp) == 8 and hp.isdigit()


def is_cell_group(cell_group):
    return type(cell_group) == str


def is_cell_leader(cell_leader):
    return is_name(cell_leader)


def is_baptised(baptised):
    return baptised == BAPTISED_YES or baptised == BAPTISED_NO


def is_role(role):
    return role == ROLE_MINISTRY_HEAD or role == ROLE_LEADER or role == ROLE_MEMBER


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
