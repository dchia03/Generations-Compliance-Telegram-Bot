import datetime as dt

from main.constants.field_names import BAPTISED_YES, BAPTISED_NO, ROLE_MEMBER, ROLE_LEADER, ROLE_MINISTRY_HEAD, \
    SERVING_STATUS_ACTIVE, SERVING_STATUS_INACTIVE, \
    SERVING_STATUS_REMOVED, SERVING_STATUS_NEW_MEMBER, COUNTING_ROOM_STATUS_NIL, COUNTING_ROOM_STATUS_SUBMITTED, \
    COUNTING_ROOM_STATUS_REJECTED, COUNTING_ROOM_STATUS_APPROVED
from main.utils.logger import Logger

log = Logger(__name__)


def is_month(month):
    try:
        month_num = dt.datetime.strptime(month, '%B').month
        return 0 < month_num < 13
    except Exception as e:
        log.error(str(e))
        return False


def is_year(year):
    return type(year) == int


def is_block_out_dates(block_out_dates):
    if type(block_out_dates) == dict:
        for date in block_out_dates.keys():
            if not date.isdigit():
                return False
        return True
    else:
        return False


def is_unconfirmed(unconfirmed):
    if type(unconfirmed) != list:
        return False
    else:
        for name in unconfirmed:
            if type(name) != str:
                return False
        return True


def is_roster(roster):
    if type(roster) == dict:
        for date in roster.keys():
            if not date.isdigit():
                return False
        return True
    else:
        return False


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
    return baptised in [BAPTISED_YES, BAPTISED_NO]


def is_role(role):
    return role in [ROLE_MINISTRY_HEAD, ROLE_LEADER, ROLE_MEMBER]


def is_serving_status(serving_status):
    return serving_status in [SERVING_STATUS_ACTIVE, SERVING_STATUS_INACTIVE,
                              SERVING_STATUS_REMOVED, SERVING_STATUS_NEW_MEMBER]


def is_counting_room_approved(counting_room_approved):
    return counting_room_approved in [COUNTING_ROOM_STATUS_NIL, COUNTING_ROOM_STATUS_SUBMITTED,
                                      COUNTING_ROOM_STATUS_APPROVED, COUNTING_ROOM_STATUS_REJECTED]
