import datetime as dt

from main.common.constants import *
from main.entity.document import Document
from main.utils.logger import Logger

logger = Logger(__name__)


def is_month(month):
    try:
        dt.datetime.strptime(month, '%B').month
        return True
    except Exception as e:
        logger.warn(str(e))
        return False


def is_year(year):
    return type(year) == int


def is_roster(roster):
    if type(roster) == dict:
        for date in roster.keys():
            if not date.isdigit():
                return False
        return True
    else:
        return False


class Roster(Document):
    log = Logger(__name__)

    def __init__(self, roster_details=None, month="January", year=2019, roster=None):
        super().__init__(
            all_fields=[
                FIELD_MONTH, FIELD_YEAR, FIELD_ROSTER
            ],
            all_fields_data_type={
                FIELD_MONTH: str,
                FIELD_YEAR: int,
                FIELD_ROSTER: dict,
            },
            all_fields_data_format={
                FIELD_MONTH: is_month,
                FIELD_YEAR: is_year,
                FIELD_ROSTER: is_roster,
            },
            non_editable_fields=[],
            document_details=roster_details
        )
        if roster is None:
            roster = {}
        if roster_details is None:
            self.set_datafield(field=FIELD_MONTH, data=month)
            self.set_datafield(field=FIELD_YEAR, data=year)
            self.set_datafield(field=FIELD_ROSTER, data=roster)

    def get_roster_str(self):
        msg = "*** No Records ***"
        is_empty_details = True
        for field in self.all_fields:
            is_empty_details &= self.document_obj[field] is None
        if not is_empty_details:
            msg = "Roster for {} {}\n\n".format(self.document_obj[FIELD_MONTH], self.document_obj[FIELD_YEAR])
            for date in sorted(self.document_obj[FIELD_ROSTER].keys(), key=lambda x: int(x)):
                msg += "{}: ".format(date)
                if len(self.document_obj[FIELD_ROSTER][date]) > 0:
                    msg += "{}".format(self.document_obj[FIELD_ROSTER][date][0])
                    for name_pos in range(1, len(self.document_obj[FIELD_ROSTER][date])):
                        msg += ", {}".format(self.document_obj[FIELD_ROSTER][date][name_pos])
                msg += "\n"
        msg += "\n"
        return msg

    def get_member_roster_dates_list(self, member_name):
        res = []
        for date in sorted(self.document_obj[FIELD_ROSTER].keys(), key=lambda x: int(x)):
            if member_name in self.document_obj[FIELD_ROSTER][date]:
                res.append(date)
        return res

    def get_member_roster_dates_str(self, member_name):
        member_roster_dates_list = self.get_member_roster_dates_list(member_name)
        msg = "Roster for {} in {} {}\n\n".format(member_name, self.document_obj[FIELD_MONTH], self.document_obj[FIELD_YEAR])
        msg += "Dates Serving: "
        if len(member_roster_dates_list) > 0:
            msg += "{}".format(member_roster_dates_list[0])
            for date_pos in range(1, len(member_roster_dates_list)):
                msg += ", {}".format(member_roster_dates_list[date_pos])
        msg += "\n"
        return msg
