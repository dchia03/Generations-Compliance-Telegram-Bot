from main.constants.database_names import ADMINISTRATION_COLLECTION
from main.constants.field_names import FIELD_ROLE, ROLE_MEMBER, ROLE_MINISTRY_HEAD, FIELD_TELEGRAM_ID, FIELD_NAME
from main.entity.collection.base.collection_base import Collection
from main.entity.database.impl.main_database import db
from main.entity.document.impl.member import Member
from main.utils.logger import Logger


class AdminCollection(Collection):
    def __init__(self, database, collection_name):
        super().__init__(database, collection_name)
        self.log = Logger(__name__)

    def has_telegram_id(self, telegram_id):
        return self.contains_document(filter={
            FIELD_TELEGRAM_ID: str(telegram_id)
        })

    def is_member_role(self, telegram_id):
        return self.has_field_value_in_document(
            filter={
                FIELD_TELEGRAM_ID: str(telegram_id)
            },
            field=FIELD_ROLE, value=ROLE_MEMBER
        )

    def is_ministry_head_role(self, telegram_id):
        return self.has_field_value_in_document(
            filter={
                FIELD_TELEGRAM_ID: str(telegram_id)
            },
            field=FIELD_ROLE, value=ROLE_MINISTRY_HEAD
        )

    def get_ministry_head(self):
        return Member(
            member_details=self.get_document(
                filter={FIELD_ROLE: ROLE_MINISTRY_HEAD}
            )
        )

    def has_member(self, telegram_id):
        return self.contains_document(
            filter={
                FIELD_TELEGRAM_ID: str(telegram_id)
            }
        )

    def get_member(self, telegram_id):
        member_details = self.get_document(filter={FIELD_TELEGRAM_ID: str(telegram_id)})
        if member_details is None:
            return None
        else:
            return Member(member_details=member_details)

    def get_member_from_name(self, name):
        member_details = self.get_document(filter={FIELD_NAME: str(name)})
        if member_details is None:
            return None
        else:
            return Member(member_details=member_details)

    def get_all_members(self):
        return [Member(member_details=member_details) for member_details in self.get_collection_list()]

    def get_all_leaders(self):
        return [m for m in self.get_all_members() if m.is_leader() or m.is_ministry_head()]

    def get_all_members_name(self):
        return [m.get_name() for m in self.get_all_members()]


admin_collection = AdminCollection(
    database=db,
    collection_name=ADMINISTRATION_COLLECTION
)
