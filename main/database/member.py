import datetime as dt

from telegram import (
    ReplyKeyboardRemove
)

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
    return baptised == "Yes" or baptised == "No"


def is_role(role):
    return role == "Ministry Head" or role == "Leader" or role == "Member"


class Member(Document):
    NON_VIEWING_FIELDS = ["Telegram ID"]
    ALL_FIELDS_REPLY_MARKUP = {
        "Telegram ID": ReplyKeyboardRemove(),
        "Full Name": ReplyKeyboardRemove(),
        "Name": ReplyKeyboardRemove(),
        "DOB": ReplyKeyboardRemove(),
        "HP": ReplyKeyboardRemove(),
        "Cell Group": ReplyKeyboardRemove(),
        "Cell Leader": ReplyKeyboardRemove(),
        "Baptised": make_keyboard_reply_markup([["Yes", "No"]]),
        "Role": make_keyboard_reply_markup([["Member"]])
    }
    ALL_FIELDS_ENTRY_EGS = {
        "Telegram ID": None,
        "Full Name": "John Smith Wei Xiang",
        "Name": "John Smith",
        "DOB": "DD/MM/YYYY",
        "HP": "91234567",
        "Cell Group": "GY 1.1",
        "Cell Leader": "Matt Chen",
        "Baptised": "Yes or No",
        "Role": "Member"
    }
    EDITABLE_FIELDS = [
        "Full Name", "Name", "DOB", "HP",
        "Cell Group", "Cell Leader", "Baptised"
    ]

    def __init__(self, member_details=None, telegram_id=""):
        super().__init__(
            all_fields=[
                "Telegram ID", "Full Name", "Name", "DOB", "HP",
                "Cell Group", "Cell Leader", "Baptised", "Role"
            ],
            all_fields_data_type={
                "Telegram ID": str,
                "Full Name": str,
                "Name": str,
                "DOB": str,
                "HP": str,
                "Cell Group": str,
                "Cell Leader": str,
                "Baptised": str,
                "Role": str
            },
            all_fields_data_format={
                "Telegram ID": is_telegram_id,
                "Full Name": is_full_name,
                "Name": is_name,
                "DOB": is_dob,
                "HP": is_hp,
                "Cell Group": is_cell_group,
                "Cell Leader": is_cell_leader,
                "Baptised": is_baptised,
                "Role": is_role
            },
            non_editable_fields=["Telegram ID", "Role"],
            document_details=member_details
        )
        if member_details is None:
            self.get_document()["Role"] = "Member"
            self.get_document()["Telegram ID"] = telegram_id

    def __eq__(self, member):
        if isinstance(member, Member):
            return self.get_datafield("Name") == member.get_datafield("Name")
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
